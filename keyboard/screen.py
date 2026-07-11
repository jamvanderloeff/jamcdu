import asyncio
from websockets.asyncio.client import connect
import pygame
import logging
import json
import fnmatch
import io




host = "10.1.1.90:8787"
sizex = 640
sizey = 560

async def main():
    async with connect("ws://10.1.1.90:8787/ws?name=demo&appKey=demo&connectionType=viewer") as ws:
        print("connected")
        welcome = json.loads(await(ws.recv()))
        if welcome['type'] == "welcome":
            print("welcome received")
            #print(welcome)
            
            fragments = []
            
            for profile in welcome['configs'][0]['profiles']:
                if fnmatch.fnmatch(welcome['state']['aircraft'], profile['aircraftPattern']):
                    fragments.append(profile['fragments'])
            print(fragments)        
            firstfragment = fragments[0][0]
            subscribereq = { 'type': "subscribe.panel",
                             'panelId': fragments[0][0]['panelId']
            }
            await ws.send(json.dumps(subscribereq))
            pygame.init()
            screen = pygame.display.set_mode((sizex,sizey), pygame.FULLSCREEN)
            async for message in ws:
                if isinstance(message, str):
                    pass
                    # print(json.loads(message))
                else:
                    print("binary recieved")
                    #print(type(message[0]))
                    surface = decodebinary(message)
                    
                    crop = pygame.Rect(firstfragment['x'], firstfragment['y'], firstfragment['width'], firstfragment['height'])
                    cropped = pygame.transform.smoothscale(surface.subsurface(crop), (sizex, sizey))
                    screen.blit(cropped, (30, 20))
                    pygame.display.flip()
              
            
            
            
    
def decodebinary(message):
    panelIdLen = message[0];
    panelId = message[1:1+panelIdLen].decode('utf-8')
    frameNumber = int.from_bytes(message[1 + panelIdLen:1 + panelIdLen+4], byteorder='little');
    # w = buf.readUInt16LE(1 + panelIdLen + 4);
    # h = buf.readUInt16LE(1 + panelIdLen + 6);
    # jpeg = buf.subarray(1 + panelIdLen + 16);
    imagestream = io.BytesIO(message[1 + panelIdLen + 16:])
    surface = pygame.image.load(imagestream, "JPG").convert()
    return surface

if __name__ == "__main__":
    asyncio.run(main())