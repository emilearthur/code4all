import datetime 
import asyncio 

import httpx
import bs4 
from colorama import Fore 


global loop

async def get_html(episode_number:int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f"https://talkpython.fm/{episode_number}"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status() 

        return resp.text


def get_title(html: str, episode_number:int) -> str:
    print(Fore.CYAN + f"Getting Title for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


def main():
    t0 = datetime.datetime.now()

    global loop 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range())

    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec.")


async def get_title_range_old():
    for n in range(270, 280):
        html = await get_html(n)
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


async def get_title_range():
    tasks = []
    for n in range(270,280):
        tasks.append((n, loop.create_task(get_html(n))))

    for n, task in tasks:
        html = await task
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == "__main__":
    main()