#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from routes import route_dict, route_index
from urllib.parse import unquote
# from urllib.parse import urlsplit, unquote, parse_qsl


# 定义一个类来保存请求
class Request:
    '''Container for data related to HTTP request.'''
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.headers = {}
        self.body = ''

    def form(self):
        '''
        把body解析为一个字典并返回
        body格式： a=b&c=d&id=3
        '''
        args = self.body.split('&')
        parms = {}
        for arg in args:
            k, v = args.split('=')
            parms[unquote(k)] = unquote(v)
        return parms


request = Request()


def parsed_path(path):
    '''将path, query分离'''
    if '?' in path:
        path, query_strings = path.split('?', 1)
        args = query_strings.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query
    else:
        return path, {}


def not_found(request):
    e = b'HTTP/1.1 404 Not Found\r\n\r\n<h1>Not Found</h1>'
    return e


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    # 路由字典
    mapper = {
            '/': route_index,
        }
    mapper.update(route_dict)
    response = mapper.get(path, not_found)
    return response(request)


def run(host, port):
    # sock是一个socket的实例
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse a local socket in TIME_WAIT state, without waiting
    # for its natural timeout to expire
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    with socket.socket() as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind()接受一个tuple
        sock.bind((host, port))

        while True:
            # 服务器监听
            sock.listen(5)
            print('Listening at', sock.getsockname())
            # 当有client连接, sock.accpet()返回2个值
            # conn是新的套接字对象， address是客户端套接字地址
            conn, addr = sock.accept()
            # getsockname()返回套接字自己的地址
            print('  Socket name:', conn.getsockname())
            # getpeername()返回连接套接字的远程地址
            print('  Socket peer:', conn.getpeername())
            r = conn.recv(1024).decode('utf-8')
            print('Ip and request, {}\n{}'.format(addr, r))
            # response = b'<h1>Hello World!</h1>'
            # HTTP REQUEST: GET /xx HTTP/1/1
            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            # 发送响应
            conn.sendall(response)
            conn.close()


if __name__ == '__main__':
    run('', 8000)
