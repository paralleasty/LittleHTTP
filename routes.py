#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    header = 'HTTP/1.1 {} {}\r\n\Content-Type: text/html\r\n'
    body = template('index.html')
    re = header + '\r\n' + body
    return re.encode(encoding='utf-8')


route_dict = {
        '/': route_index,
        }
