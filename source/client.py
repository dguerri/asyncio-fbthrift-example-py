#!/usr/bin/env python3

import asyncio
import os
import sys
import ssl

from thrift.server.TAsyncioServer import ThriftClientProtocolFactory

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen-py")
)
from mytest import TestService


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    certfile = "/root/ssl-stuff/client.pem"
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=certfile, keyfile=certfile)
    context.load_verify_locations(cafile="/root/ssl-stuff/rootca.pem")

    connection = loop.create_connection(
        ThriftClientProtocolFactory(TestService.Client, loop=loop),
        host="localhost",
        port=29292,
        ssl=context,
    )
    _, protocol = loop.run_until_complete(connection)
    result = loop.run_until_complete(protocol.client.add(5, 2))
    print(f"Add: {result}")

    loop.close()
    protocol.close()

    sys.exit(0)
