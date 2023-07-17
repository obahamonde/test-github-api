import asyncio

from aiofauna import *
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from openai_function_call import openai_function, openai_schema


class SearchResult(BaseModel):
    title: str = Field(...)
    url: str = Field(...)


BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/90.0.4430.212 Chrome/90.0.4430.212 Safari/537.36"
}


@openai_function
async def search_google(text: str) -> List[SearchResult]:
    """
    Search for a text in Google results.

    This function will be used to search for the answer of the user's question. if it is not found in the knowledge base.

    For the sake of not hallucinating, this function will be used to search for the answer of the user's question. if it is not found in the knowledge base.

    """
    async with ClientSession(headers=BROWSER_HEADERS) as session:
        async with session.get(
            f"https://www.google.com/search?q={text}", headers=BROWSER_HEADERS
        ) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            results = soup.find_all("div", attrs={"class": "g"})
            return [
                SearchResult(
                    title=result.find("h3").text, url=result.find("a").get("href")
                )
                for result in results
            ]
