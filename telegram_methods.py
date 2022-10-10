import time
import json
import urllib.parse
import requests
import re
import os
import logging
import sys
import aiohttp
import asyncio

TOKEN = "5584161509:AAFwAx4FNR_hSJNArQulRQ1alba-CjjLszA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

limit = asyncio.Semaphore(20)  # Чтобы не словить secondary rate limit
time_sleep = 0.01


async def async_get_json_from_url(url: str, data=None):
    async with limit:
        if limit.locked():
            await asyncio.sleep(time_sleep)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                return await response.json()


def is_file_exist(path: str) -> bool:
    return os.path.isfile(path)


def get_url(url: str):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url: str):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js = get_json_from_url(url)
    return js


async def async_send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    await async_get_json_from_url(url)


async def async_send_photo(photo, chat_id, text=None, reply_markup=None, ):
    url = f"{URL}sendPhoto?chat_id={chat_id}"
    with open(photo, 'rb') as file:
        if text:
            text = urllib.parse.quote_plus(text)
            url += f'&caption={text}'
        if reply_markup:
            url += f"&reply_markup={reply_markup}"
        await async_get_json_from_url(url, {'photo': file})


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def get_latest_request_id():
    updates = get_updates()["result"]
    url = URL + "getUpdates?timeout=100"
    return updates[-1]["update_id"] + 1


# def send_message(text, chat_id, reply_markup=None):
#     text = urllib.parse.quote_plus(text)
#     url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
#     if reply_markup:
#         url += f"&reply_markup={reply_markup}"
#     get_url(url)
#
#
# def send_photo(photo, chat_id, text=None, reply_markup=None, ):
#     url = f"{URL}sendPhoto?chat_id={chat_id}"
#     files = {'photo': open(photo, 'rb')}
#     if text:
#         text = urllib.parse.quote_plus(text)
#         url += f'&caption={text}'
#     if reply_markup:
#         url += f"&reply_markup={reply_markup}"
#     requests.post(url, files=files)