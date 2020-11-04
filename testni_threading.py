import threading
import time
import asyncio

y = 0
x = 0
async def func_1():
    while True:
        await asyncio.sleep(3)
        print("hello")

async def func_2():
    while True:
        await asyncio.sleep(5)
        print("hi")

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(func_1())
    asyncio.ensure_future(func_2())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing loop...")
    loop.close()




