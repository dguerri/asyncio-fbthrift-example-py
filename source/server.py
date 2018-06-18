#!/usr/bin/env python3

import asyncio
import os
import sys
import ssl

from thrift.server.TAsyncioServer import ThriftAsyncServerFactory

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen-py")
)
from mytest import TestService


class TestServiceHandler(TestService.Iface):
    def __init__(self):
        super(TestServiceHandler, self).__init__()
        self.log = {}

    def add(self, n1, n2):
        print("add(%d, %d)" % (n1, n2))
        return n1 + n2


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    certfile = "/root/ssl-stuff/server.pem"
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=certfile, keyfile=certfile)
    context.load_verify_locations(cafile="/root/ssl-stuff/rootca.pem")

    handler = TestServiceHandler()
    server = loop.run_until_complete(
        ThriftAsyncServerFactory(handler, loop=loop, port=29292, ssl=context)
    )

    print("Starting server...")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.close()
        sys.exit(1)

    sys.exit(0)
