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
