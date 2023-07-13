import logging
import asyncio
import aiohttp
from typing import List, NamedTuple, Awaitable, Optional
from ..services import ChatGPT, AmazonWebServices, Email, User
from aiofauna import WebSocketResponse, asyncify
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Page(NamedTuple):
    title: str
    url: str
    content: str

class SiteMapTool:
    def __init__(self, namespace: str, logger: logging.Logger, ref:Optional[str]=None, websocket: Optional[WebSocketResponse]=None, max_connections: int = 1000):
        self.urls: List[str] = []
        self.pages: int = 0
        self.semaphore = asyncio.Semaphore(max_connections)
        self.logger = logger
        self.websocket = websocket
        self.gpt = ChatGPT(namespace=namespace)
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=max_connections))
        if ref:
            self.ref = ref
            self.aws = AmazonWebServices()
            

    async def fetch_loc(self, url: str):
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, features="xml")
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.logger.error("Failed to fetch %s: %s", url, str(e))
                return self.urls
            except Exception as e:
                self.logger.error("Failed to parse %s: %s", url, str(e))
                return self.urls
            sitemaps = soup.find_all("sitemap")
            if sitemaps:
                await asyncio.gather(
                    *[self.fetch_loc(sitemap.find("loc").text) for sitemap in sitemaps]
                )
                self.logger.info("Found %s nested sitemaps", len(sitemaps)) 
            else:
                self.urls.extend([loc.text for loc in soup.find_all("loc")])
                if len(self.urls) > 0:
                    self.logger.info("Found %s urls", len(self.urls))
            return self.urls

    async def fetch_sitemap(self, url: str):
        sitemap_url = url if url.endswith(".xml") else f"{url}/sitemap.xml"
        self.logger.info(f"Fetching sitemap from {sitemap_url}")
        return await self.fetch_loc(sitemap_url)

    async def fetch_page(self, url: str):
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, features="lxml")
                    title, content = soup.title.text, soup.body.text.strip()
                    page = Page(title=title, url=url, content=content)
                    self.logger.info("Fetched %s", page.title)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                page = Page(title=url, url=url, content="")
                self.logger.error("Failed to fetch %s: %s", page.title, str(e))
            except Exception as e:
                page = Page(title=url, url=url, content="")
                self.logger.error("Failed to process %s: %s", page.title, str(e))
            finally:
                self.pages += 1
                self.logger.info(f"Added {page} to pages")
                progress = (self.pages / len(self.urls))
                self.logger.info("%s%%", progress * 100)
                await self.gpt.insert(text="\n".join([page.title, page.url, page.content]))
                if self.websocket:
                    await self.websocket.send_json({"progress": progress * 100})

    async def run(self, u: str):
        urls = await self.fetch_sitemap(u)
        for url in urls:
            await self.fetch_page(url)
        self.logger.info("Finished fetching %s pages", self.pages)
        if self.ref:
            html = f"""
                <h1>Finished crawling {u}</h1>
                <p>Found {len(self.urls)} urls</p>
                <p>Processed {self.pages} pages</p>
            """
            print("Sending email to", self.ref)
            user = await User.get(self.ref)
            assert isinstance(user, User)
            verified_emails = await self.aws.list_verified_emails()
            verified = user.email in verified_emails
            if not verified:
                await self.aws.verify_email(Email(to=user.email))
                while not verified:
                    verified = user.email in await self.aws.list_verified_emails()
                    await asyncio.sleep(3)
            await self.aws.send_email(Email(to=user.email, subject=f"Finished downloading {u}", html=html))
            self.logger.info("Sent email to %s", user.email)
        await self.cleanup()
    async def cleanup(self):
        await self.session.close()