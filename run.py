import argparse
import asyncio

import aiohttp

import route_calculator as rc


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='calculate route info from SDC logs'
    )
    parser.add_argument('-u', '--url',
                        help='data source Url',
                        required=True)
    return parser


async def _fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch(url: str):
    async with aiohttp.ClientSession() as session:
        txt = await _fetch(session, url)
        return txt


async def do_stuff():
    parser = create_parser()
    args = parser.parse_args()
    url = args.url
    raw_data = await fetch(url)
    data = raw_data.strip()
    rows = data.split('\n')
    routes = rc.route_calculator(rows)
    [print(r.serialize()) for r in routes]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_stuff())

