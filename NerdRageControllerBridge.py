import asyncio
import serial_asyncio
import json
import argparse
import autobahn.asyncio.wamp
import os

class NerdRageControllerSerialProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
    
    def data_received(self, data):
        
        async def laser_enabled():
            pass

        print('data received', repr(data))
        
        if (data == 'laser enabled'):
            asyncio.create_task(laser_enabled)

    def connection_lost(self, data):
        #TODO
        pass

class NerdRageControllerBridgeWampSession(autobahn.asyncio.wamp.ApplicationSession):

    async def onJoin(self, details):

        async def enable_laser():
            print('enabled laser')

        async def disable_laser():
            print('disabled laser')

        async def fire_laser():
            print('firing laser')

        async def stop_laser():
            print('stopping laser')
        
        procedures = {
            'nl.matthijsbos.nerdrage.enable_laser': enable_laser,
            'nl.matthijsbos.nerdrage.disable_laser': disable_laser,
            'nl.matthijsbos.nerdrage.fire_laser': fire_laser,
            'nl.matthijsbos.nerdrage.stop_laser': stop_laser
        }
        
        # Register all procedures in router
        for procedure_name, procedure_handler in procedures.items():
            await self.register(procedure_handler, procedure_name)
            print(f'Registered procedure {procedure_name}')

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

    serial_coro = serial_asyncio.create_serial_connection(loop, NerdRageControllerSerialProtocol, args.port, baudrate=115200)
    loop.run_until_complete(serial_coro)

    runner = autobahn.asyncio.wamp.ApplicationRunner(args.address, args.realm)
    wamp_session_coro = runner.run(NerdRageControllerBridgeWampSession, start_loop=False)
    loop.run_until_complete(wamp_session_coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        loop.close()