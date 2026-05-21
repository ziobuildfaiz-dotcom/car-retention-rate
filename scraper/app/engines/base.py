"""Abstract base class for all site-specific scrapers."""

import random
import time
from abc import ABC, abstractmethod

import httpx


class BaseScraper(ABC):
    base_url: str = ""
    site_name: str = "base"

    def __init__(self, proxy: str | None = None):
        self.client = httpx.Client(
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            },
            follow_redirects=True,
        )
        if proxy:
            self.client.proxies = {"http://": proxy, "https://": proxy}

    def rate_limit(self):
        delay = random.uniform(3, 8)
        time.sleep(delay)

    @abstractmethod
    def scrape_brands(self) -> list[dict]:
        ...

    @abstractmethod
    def scrape_series(self, brand_url: str) -> list[dict]:
        ...

    @abstractmethod
    def scrape_retention(self, model_url: str) -> dict:
        ...
