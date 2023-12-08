#!/usr/bin/env python
# from __future__ import print_function

import json
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer

from kvstorage import KVStorage

global _g_kvstorage


def is_str(value):
    b = True
    if not isinstance(value, str):
        b = False
    return b


def is_list_of_string(value):
    b = True
    # Check if value is a list
    if not isinstance(value, list):
        b = False
    # Check if all items in the list are strings
    if not all(isinstance(item, str) for item in value):
        b = False
    return b


class KVRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path.startswith("/keys")):
            try:
                key = self.path[5:]
                value = _g_kvstorage.get(key)

                if value == None:
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                json_value = json.dumps(value)
                self.wfile.write(json_value.encode('utf-8'))
            except Exception:
                self.send_response(500)
                self.end_headers()
        elif (self.path == "/admin/status"):
            status = str(_g_kvstorage.getStatus())
            print("status: ", status)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(status.encode('utf-8'))
        else:
            self.send_response(405)
            self.end_headers()

    def do_POST(self):
        try:
            if (self.path.startswith("/keys")):
                key = self.path[5:]
                print("key: ", key)
                input_str = self.rfile.read(int(self.headers.get('content-length'))).decode('utf-8')
                input_json = json.loads(input_str)
                request_type = input_json["type"]
                request_value = input_json["value"]
                if request_type == "PUT":
                    if is_list_of_string(request_value):
                        _g_kvstorage.put(key, request_value)
                    else:
                        self.send_response(400)
                        self.send_header("Content-Type", "text/plain")
                        self.end_headers()
                        self.wfile.write("The request value is not valid".encode('utf-8'))
                        return
                elif request_type == "APPEND":
                    if is_str(request_value):
                        _g_kvstorage.append(key, request_value)
                    else:
                        self.send_response(400)
                        self.send_header("Content-Type", "text/plain")
                        self.end_headers()
                        self.wfile.write("The request value is not valid".encode('utf-8'))
                        return
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write("The request type is not correct".encode('utf-8'))
                    return
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(405)
                self.end_headers()

        except Exception as err:
            print("Error: ", err)
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write("The request is not valid".encode("utf-8"))


def main():
    if len(sys.argv) < 5:
        print('Usage: %s http_port dump_file.bin selfHost:port partner1Host:port partner2Host:port ...' % sys.argv[0])
        sys.exit(-1)

    httpPort = int(sys.argv[1])
    print("http port: ", httpPort)
    selfAddr = sys.argv[2]
    print("selfAddr: ", selfAddr)
    partners = sys.argv[3:]
    print("partners: ", partners)
    global _g_kvstorage
    _g_kvstorage = KVStorage(selfAddr, partners)
    httpServer = HTTPServer(('', httpPort), KVRequestHandler)
    httpServer.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
