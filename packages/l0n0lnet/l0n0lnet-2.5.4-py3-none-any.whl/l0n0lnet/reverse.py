from l0n0lnet.tcp import base_client, base_server
from l0n0lnet.tcp import session_read_size, close_tcp, client_read_size
from l0n0lnet.stream_parser import stream_parser
from l0n0lnet.utils import call_after
from l0n0lnet.tcp import get_ip_port, connect_to, set_cb, send_message
from struct import pack, unpack
from copy import deepcopy
from random import randint
from enum import IntEnum
import time


class proxy_cmd(IntEnum):
    connect = 1
    close = 2
    data = 3
    heart = 4


def pack_proxy_msg(cmd: int, data: bytes = None):
    if data is not None:
        return pack("!II", cmd, len(data)) + data
    return pack("!II", cmd, 0)


def unpack_proxy_header(data):
    return unpack("!II", data)


class reverse_server(base_server):
    def __init__(self, ip: bytes, port: int, keys: list):
        super().__init__(ip, port)
        self.session_data = {}
        self.parsers = []
        self.servers = {}

        for key in keys:
            parser = stream_parser()
            parser.set_password(key)
            self.parsers.append(parser)

        call_after(1000, self.on_heart, 1000)

    def on_heart(self):
        for session_id, session_data in self.session_data.items():
            heart = session_data["heart"]
            heart += 1
            if heart >= 10:
                close_tcp(session_id)
            session_data["heart"] = heart

    def on_session_connected(self, session_id):
        # 创建会话数据
        self.session_data[session_id] = {"state": "get_info", "heart": 0}

        # 读取2个字节的加密索引 (密钥索引(2), 端口(2), 对应的代理服务器会话ID(4)[0表示控制会话])
        session_read_size(session_id, 2 + 2 + 4)

    def on_session_disconnected(self, session_id):
        # 获取会话数据
        session_data = self.session_data.get(session_id)
        if not session_data:
            close_tcp(session_id)
            return

        server: reverse_server_server = self.servers.get(session_data["port"])
        if server:
            if session_data["server_session_id"] == 0:
                # 关闭会话对应的该服务器
                server.close()
            else:
                # 关闭相应的会话
                server.on_remote_session_disconnected(
                    session_data["server_session_id"])

        # 删除会话数据
        del self.session_data[session_id]

    def on_session_read(self, session_id, data, size):
        # 获取会话数据
        session_data = self.session_data.get(session_id)
        if not session_data:
            close_tcp(session_id)
            return

        # 重置心跳
        session_data["heart"] = 0

        # 获取连接信息
        if session_data["state"] == "get_info":
            index, port, server_session_id = unpack("!HHI", data)
            # 校验索引是否超出范围
            if index >= len(self.parsers):
                close_tcp(session_id)
                return

            # 获取混淆器
            parser = self.parsers[index]

            # 为会话匹配加密parser
            session_data["parser"] = parser

            # 如果是控制流
            if server_session_id == 0:
                # 如果服务已开启，关闭它
                server: reverse_server_server = self.servers.get(port)
                if server:
                    server.close()

                # 创建对外服务器
                self.servers[port] = reverse_server_server(
                    self, session_id, port, parser)
            else:
                # 获取对应的服务器
                server: reverse_server_server = self.servers.get(port)
                if not server:
                    close_tcp(session_id)
                    return

                # 注册会话
                server.set_remote_session(
                    server_session_id, session_id, parser)

            # 缓存会话数据
            session_data["server_session_id"] = server_session_id
            session_data["port"] = port

            # 进入包头读取
            session_data["state"] = "get_header"
            session_read_size(session_id, 8)
        elif session_data["state"] == "get_header":
            # 分析包头数据
            cmd, data_len = unpack_proxy_header(data)
            # 心跳包
            if cmd == proxy_cmd.heart:
                return
            # 进入数据获取状态
            session_data["cmd"] = cmd
            session_data["state"] = "get_data"
            session_read_size(session_id, data_len)
        elif session_data["state"] == "get_data":
            server_session_id = session_data["server_session_id"]
            # 暂时没有控制指令
            if server_session_id == 0:
                return

            # 获取对外服务器
            server: reverse_server_server = self.servers.get(
                session_data["port"])
            if not server:
                close_tcp(session_id)
                return

            # 传送数据
            session_data["parser"].decrypt(data)
            server.send_msg(server_session_id, data)

            # 读取包头
            session_data["state"] = "get_header"
            session_read_size(session_id, 8)


class reverse_server_server(base_server):
    def __init__(self, owner: reverse_server, control_session_id: int, port: int, parser: stream_parser):
        super().__init__(b'0.0.0.0', port)
        self.owner = owner
        self.control_session_id = control_session_id
        self.control_parser = parser
        self.local_owner_session = {}
        self.msg_cache = {}

    def set_remote_session(self, local_session_id, owner_session_id, parser):
        self.local_owner_session[local_session_id] = {
            "owner_session_id": owner_session_id,
            "parser": parser
        }

        # 发送缓存的数据
        cache_msgs = self.msg_cache.get(local_session_id)
        if cache_msgs and len(cache_msgs) > 0:
            for msg in cache_msgs:
                data = msg['data']
                parser.encrypt(data)
                self.owner.send_msg(
                    owner_session_id, pack_proxy_msg(msg['cmd'], data))
            del self.msg_cache[local_session_id]

    def send_msg_to_real_server(self, session_id: int, cmd: int, data: bytes = None):
        # 控制指令直接发送
        if cmd != proxy_cmd.data:
            self.control_parser.encrypt(data)
            data = pack_proxy_msg(cmd, data)
            self.owner.send_msg(self.control_session_id, data)
            return

        # 如果没有对应的远端链接，缓存数据
        owner_session_data = self.local_owner_session.get(session_id)
        if not owner_session_data:
            if self.msg_cache.get(session_id):
                self.msg_cache[session_id].append({
                    "cmd": cmd,
                    "data": data
                })
            else:
                self.msg_cache[session_id] = [
                    {
                        "cmd": cmd,
                        "data": data
                    }
                ]
            return

        # 打包包头
        if data:
            owner_session_data['parser'].encrypt(data)
        data = pack_proxy_msg(cmd, data)

        # 发送到远端链接
        self.owner.send_msg(owner_session_data['owner_session_id'], data)

    def on_session_connected(self, session_id):
        # 向真实服务器开一个会话
        self.send_msg_to_real_server(
            self.control_session_id, proxy_cmd.connect, pack("!I", session_id))

    def on_session_disconnected(self, session_id):
        # 向真实服务器关闭一个会话
        self.send_msg_to_real_server(
            self.control_session_id, proxy_cmd.close, pack("!I", session_id))

    def on_session_read(self, session_id, data, size):
        # 将数据传送给真实服务器
        self.send_msg_to_real_server(session_id, proxy_cmd.data, data)

    def on_remote_session_disconnected(self, session_id):
        close_tcp(session_id)


class reverse_client(base_client):
    def __init__(self, ip: bytes, port: int, keys: list, remote_port: int, tip: bytes, tport: int):
        self.server_ip = ip
        self.server_port = port
        self.remote_port = remote_port
        self.tip = tip
        self.tport = tport
        self.parsers = []
        self.msg_cache = {}
        self.keys = keys

        for key in keys:
            parser = stream_parser()
            parser.set_password(key)
            self.parsers.append(parser)

        # 连接目标
        self.reconnect()

        # 开启timer
        call_after(1000, self.update, 1000)

    def update(self):
        if not self.connected:
            return

        # 发送心跳
        self.send_message_to_remote_server(proxy_cmd.heart)

    def reconnect(self):
        # 重置连接状态
        self.connected = False

        # 关闭已有的连接
        if hasattr(self, "clients"):
            clients: dict = getattr(self, "clients")
            if clients:
                for client in clients.values():
                    client.close()

        # 连接服务器
        super().__init__(self.server_ip, self.server_port)

        # 随机密钥索引
        self.parser_index = randint(0, len(self.parsers) - 1)

        # 创建混淆器
        self.parser = self.parsers[self.parser_index]

        # 清空缓存
        self.clients = {}
        self.cur_cmd = 0

        # 读取数据
        self.state = "get_header"
        client_read_size(self.id, 8)

    def on_connected(self):
        # 设置连接状态
        self.connected = True

        # 发送密钥和端口
        self.send_msg(pack("!HHI", self.parser_index, self.remote_port, 0))

    def on_connect_failed(self):
        # 重新连接服务器
        call_after(1000, self.reconnect)
        print("Connect to Server Failed! Reconnect in 1 second.")

    def on_disconnected(self):
        # 设置连接状态
        self.connected = False

        # 重新连接服务器
        call_after(1000, self.reconnect)
        print("DisConnect from server! Reconnect in 1 second.")

    def on_read(self, data, size):
        # 读取包头
        if self.state == "get_header":
            # 解析包头，获取命令
            self.cur_cmd, data_len = unpack_proxy_header(data)

            # 查看是否还有数据
            if data_len <= 0:
                return

            # 获取数据
            self.state = "get_data"
            client_read_size(self.id, data_len)
        # 将数据传送给本地客户端
        elif self.state == "get_data":
            # 解密数据
            self.parser.decrypt(data)

            # 创建连接
            if self.cur_cmd == proxy_cmd.connect:
                remote_session_id = unpack("!I", data)[0]
                self.clients[remote_session_id] = reverse_client_client(
                    self, remote_session_id)
            # 关闭连接
            elif self.cur_cmd == proxy_cmd.close:
                remote_session_id = unpack("!I", data)[0]
                client = self.clients.get(remote_session_id)
                if not client:
                    return
                client.close()
            # 无效指令
            else:
                print("Get ivalid command!")

            # 继续读取包头
            self.state = "get_header"
            client_read_size(self.id, 8)

    def send_message_to_remote_server(self, cmd, data=None):
        # 加密数据
        if data:
            self.parser.encrypt(data)

        # 打包包头
        msg_data = pack_proxy_msg(cmd, data)

        # 发送数据
        self.send_msg(msg_data)


class reverse_client_client(base_client):
    def __init__(self, owner: reverse_client, remote_session_id: int):
        # 缓存数据
        self.owner = owner
        self.remote_session_id = remote_session_id
        self.cache = b""
        self.connected = False
        self.ip = owner.tip
        self.port = owner.tport

        # 连接到被代理服务器
        super().__init__(owner.tip, owner.tport)
        self.start_trans_client()

    def start_trans_client(self):
        # 随机密钥索引
        self.parser_index = randint(0, len(self.owner.parsers) - 1)
        self.parser = self.owner.parsers[self.parser_index]

        # 缓存数据
        self.tran_connected = False
        self.remote_send_cache = b''

        # 连接到代理服务器用于传输数据
        self.remote_name = f"reverse_client_client_{self.remote_session_id}"
        self.remote_client_id = connect_to(
            self.remote_name, self.owner.server_ip, self.owner.server_port)
        set_cb(self.remote_name, "on_connected", self.on_trans_connected)
        set_cb(self.remote_name, "on_connect_failed",
               self.on_trans_connect_failed)
        set_cb(self.remote_name, "on_disconnected", self.on_trans_disconnected)
        set_cb(self.remote_name, "on_read", self.on_trans_read)

        # 初始读取状态
        self.remote_state = "get_header"
        client_read_size(self.remote_client_id, 8)

    def send_remote_cmd(self, cmd, data: bytes = None):
        if data:
            self.parser.encrypt(data)
        data = pack_proxy_msg(cmd, data)
        self.send_remote_msg(data)

    def send_remote_msg(self, data):
        if len(data) <= 0:
            return
        if not self.tran_connected:
            self.remote_send_cache += data
            return
        send_message(self.remote_client_id, data)

    def on_connected(self):
        print(
            f"Connected to local {self.ip}:{self.port} remote_session_id = {self.remote_session_id}")

        # 设置连接成功
        self.connected = True

        # 发送缓存数据
        self.send_msg(self.cache)

        # 清空缓存
        self.cache = b""

    def on_connect_failed(self):
        print(f"Failed connect to {self.ip}:{self.port} "
              f"remote_session_id = {self.remote_session_id}")
        # 告知远端服务器关闭连接
        self.send_remote_cmd(
            proxy_cmd.close, pack("!I", self.remote_session_id))

    def on_disconnected(self):
        print(f"Disconnected from {self.ip}:{self.port} "
              f"remote_session_id = {self.remote_session_id}")

        # 设置连接状态
        self.connected = False

        # 关闭传输链接
        close_tcp(self.remote_client_id)

    def on_read(self, data, size):
        self.send_remote_cmd(proxy_cmd.data, data)

    def on_trans_connected(self):
        # 设置连接状态
        self.tran_connected = True

        # 发送密钥和端口
        self.send_remote_msg(pack("!HHI", self.parser_index,
                                  self.owner.remote_port,
                                  self.remote_session_id))

        # 发送缓存数据
        self.send_remote_msg(self.remote_send_cache)
        self.remote_send_cache = b''

    def on_trans_connect_failed(self):
        call_after(1000, self.start_trans_client)

    def on_trans_disconnected(self):
        self.tran_connected = False
        # 关闭对目标服务的链接
        self.close()

    def on_trans_read(self, data, size):
        if self.remote_state == "get_header":
            self.remote_cmd, data_len = unpack_proxy_header(data)
            self.remote_state = "get_data"
            client_read_size(self.remote_client_id, data_len)
        elif self.remote_state == "get_data":
            if self.remote_cmd == proxy_cmd.data:
                self.parser.decrypt(data)
                self.send_msg(data)
            self.remote_state = "get_header"
            client_read_size(self.remote_client_id, 8)
