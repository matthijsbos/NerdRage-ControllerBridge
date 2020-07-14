import asyncio
import serial_asyncio
import json
import argparse
import autobahn.asyncio.wamp
import os
import nerdrage_controller_bridge

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Serial bridge for NerdRage Controller')
    parser.add_argument('--address', metavar='WAMP_SERVER_ADDRESS', default=os.getenv("NERDRAGE_WAMP_SERVER_ADDRESS"))
    parser.add_argument('--realm', metavar='WAMP_REALM', default=os.getenv("NERDRAGE_WAMP_REALM"))
    parser.add_argument('--port', metavar='SERIAL_PORT', default=os.getenv("NERDRAGE_SERIAL_PORT"))

    args = parser.parse_args()
    print(f'WAMP server address: {args.address}')
    print(f'WAMP realm:          {args.realm}')
    print(f'Serial port:         {args.port}')

    loop = asyncio.get_event_loop()

    serial_coro = serial_asyncio.create_serial_connection(loop, nerdrage_controller_bridge.NerdRageControllerSerialProtocol, args.port, baudrate=115200)
    loop.run_until_complete(serial_coro)

    runner = autobahn.asyncio.wamp.ApplicationRunner(args.address, args.realm)
    wamp_session_coro = runner.run(nerdrage_controller_bridge.NerdRageControllerBridgeWampSession, start_loop=False)
    loop.run_until_complete(wamp_session_coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        loop.close()