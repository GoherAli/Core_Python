
import argparse
import random
import itertools as it
import os
import time

import asyncio

async def makeitem(size: int = 5)-> str:
    return os.urandom(size).hex()

async def randsleep(a: int = 1, b: int = 5, caller=None)->None:
    delay = random.randint(0,10)
    if caller:
        print (f'{caller} sleeping for {delay} seconds')
    asyncio.sleep(delay)


async def Produce(name: int , q: asyncio.Queue)->None:
    prod_factor = random.randint(1,10)
    for _ in it.repeat(None, prod_factor):
        await randsleep(caller = f'Producer {name}')
        prod_time = time.perf_counter()
        item = await makeitem()
        await q.put((item, prod_time))
        print (f'Producer{name} --->{item} AT TIME:{prod_time}')
               
               
async def Consume(name: int , q: asyncio.Queue)->None:
    while True:
        await randsleep(caller = f'Consumer{name}')
        cons_time = time.perf_counter()
        item, at_time = await q.get()
        print (f'Consumer {name} <------{item} AT TIME:{cons_time}')
        q.task_done()
               


async def main(nprod: int, ncon: int):
    
    q = asyncio.Queue()
    producers = [asyncio.create_task(Produce(n,q)) for n in range(nprod)]
    consumers = [asyncio.create_task(Consume(n,q)) for n in range(ncon)]

    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()
                 




if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--nprod', type=int, default = 5)
    parser.add_argument('-c', '--ncon' , type=int , default = 10)
    arguments = parser.parse_args()

    start = time.perf_counter()

    asyncio.run(main(arguments.nprod, arguments.ncon))
    time.sleep(1)
    elapsed = time.perf_counter() - start
    print (f'Execution Time {elapsed} seconds.')
    
