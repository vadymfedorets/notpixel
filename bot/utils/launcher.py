import asyncio
import argparse
import glob
import os
from itertools import cycle
from random import randint
from typing import Any
from better_proxy import Proxy
from pyrogram import Client

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions
from bot.utils.accounts import Accounts



art_work = """

888b    888          888    8888888b.  d8b                   888 
8888b   888          888    888   Y88b Y8P                   888 
88888b  888          888    888    888                       888 
888Y88b 888  .d88b.  888888 888   d88P 888 888  888  .d88b.  888 
888 Y88b888 d88""88b 888    8888888P"  888 `Y8bd8P' d8P  Y8b 888 
888  Y88888 888  888 888    888        888   X88K   88888888 888 
888   Y8888 Y88..88P Y88b.  888        888 .d8""8b. Y8b.     888 
888    Y888  "Y88P"   "Y888 888        888 888  888  "Y8888  888 
                                                                 
                                                                 by Surinity                                    
"""

version = "      proxy.txt edition"

start_text = """                                             
Select an action:

    1. Run bot
    2. Create session
    
"""

global tg_clients


def get_session_names() -> list[str]:
    session_names = sorted(glob.glob("sessions/*.session"))
    session_names = [
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    ]

    return session_names


def get_proxies() -> list[Proxy]:
    if settings.USE_PROXY_FROM_FILE:
        with open(file="bot/config/proxies.txt", encoding="utf-8-sig") as file:
            proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file]
    else:
        proxies = []

    return proxies


async def get_tg_clients() -> list[Client]:
    global tg_clients

    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    if not settings.API_ID or not settings.API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    tg_clients = [
        Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            workdir="sessions/",
            plugins=dict(root="bot/plugins"),
        )
        for session_name in session_names
    ]

    return tg_clients


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    logger.info(f"Detected {len(get_session_names())} sessions | {len(get_proxies())} proxies")

    action = parser.parse_args().action

    if not action:
        print('\033[1m' + '\033[92m' + art_work + '\033[0m')
        print('\033[1m' + '\033[93m' + version + '\033[0m')

        if settings.AUTO_TASK:
            logger.warning("Auto Task is enabled, it is dangerous functional")

        print(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ["1", "2"]:
                logger.warning("Action must be 1 or 2")
            else:
                action = int(action)
                break

    if action == 1:
        tg_clients = await get_tg_clients()

        await run_tasks(tg_clients=tg_clients)

    elif action == 2:
        await register_sessions()




async def run_tasks(tg_clients: list[Client]):
    proxies = get_proxies()
    proxies_cycle = cycle(proxies) if proxies else None
    tasks = [
        asyncio.create_task(
            run_tapper(
                tg_client=tg_client,
                proxy=next(proxies_cycle) if proxies_cycle else None,
            )
        )
        for tg_client in tg_clients
    ]

    await asyncio.gather(*tasks)