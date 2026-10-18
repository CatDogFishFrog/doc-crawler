import asyncio
import os
import sys
import argparse
import requests
import re
import time
from urllib.parse import urljoin, urlparse
from typing import Set, List, Optional
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class UniversalDocCrawler:
    def __init__(self, start_url: str, output_dir: str, css_selector: str = None):
        parsed = urlparse(start_url)
        path = parsed.path
        if not path.endswith("/") and "." in os.path.basename(path):
            path = os.path.dirname(path)
        
        self.base_url = f"{parsed.scheme}://{parsed.netloc}{path.rstrip('/')}/"
        self.start_url = start_url
        self.output_dir = output_dir
        self.css_selector = css_selector
        self.visited_urls: Set[str] = set()
        self.queue: List[str] = [self.start_url]
        
        # HTTP Session for fallback or simple sites
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Universal noise pattern for sidebars, navs, footers, cookies, etc.
        self.noise_patterns = re.compile(r'sidebar|nav|menu|toc|navigation|aside|footer|header|header-wrapper|footer-wrapper|optanon|onetrust|cookie', re.I)
        
        os.makedirs(self.output_dir, exist_ok=True)

    def is_internal(self, url: str) -> bool:
        return url.startswith(self.base_url)

    def url_to_path(self, url: str) -> str:
        parsed = urlparse(url)
        base_parsed = urlparse(self.base_url)
        base_path = base_parsed.path
        relative_path = parsed.path
        
        if relative_path.startswith(base_path):
            relative_path = relative_path[len(base_path):]
        
        relative_path = relative_path.lstrip("/")
        
        if not relative_path:
            filename = "index.md"
        elif relative_path.endswith("/"):
            filename = os.path.join(relative_path, "index.md")
        else:
            if relative_path.endswith(".html"):
                filename = relative_path[:-5] + ".md"
            elif not "." in os.path.basename(relative_path):
                filename = relative_path + ".md"
            else:
                filename = relative_path
            
        return os.path.join(self.output_dir, filename)

    async def fetch_fallback(self, url: str) -> Optional[str]:
        """Simple HTTP fallback if browser-based fetch fails (e.g. Cloudflare)."""
        def _fetch(u):
            try:
                # Try simple GET
                resp = self.session.get(u, timeout=20)
                if resp.status_code == 404 and not u.endswith(".html") and not "." in u.split("/")[-1]:
                    # Proactive .html retry for sphinx/unity style links
                    resp = self.session.get(u + ".html", timeout=20)
                resp.raise_for_status()
                return resp.text
            except:
                return None
        
        return await asyncio.to_thread(_fetch, url)

    def clean_html(self, html: str) -> str:
        """Universal noise removal using heuristics (regex on classes/ids)."""
        soup = BeautifulSoup(html, 'lxml')
        
        # 1. Remove obvious tag-based noise
        for tag_name in ['nav', 'aside', 'footer', 'header', 'script', 'style']:
            for t in soup.find_all(tag_name):
                t.decompose()
        
        # 2. Heuristic removal of sidebars, menus, etc.
        for element in list(soup.find_all(True)):
            if not element.name: continue
            
            classes = element.get('class', [])
            if isinstance(classes, list): classes = " ".join(classes)
            element_id = element.get('id', '')
            
            # If class or ID matches noise patterns...
            if (classes and self.noise_patterns.search(classes)) or (element_id and self.noise_patterns.search(element_id)):
                # ...but UNLESS it looks like main content
                whitelist = r'main|article|body|content|doc-content|content-block'
                if self.css_selector:
                    whitelist += "|" + re.escape(self.css_selector.strip('.'))
                
                if not re.search(whitelist, classes + element_id, re.I):
                    element.decompose()
        
        # 3. Targeted extraction if selector provided, else find main-ish area
        main_content = None
        selectors = [self.css_selector] if self.css_selector else []
        selectors.extend(['div[role="main"]', 'main', 'article', '.content', '#content', '.body'])
        
        for sel in selectors:
            if not sel: continue
            found = soup.select_one(sel)
            if found:
                main_content = found
                break
        
        if not main_content:
            main_content = soup.body if soup.body else soup
            
        return str(main_content)

    async def crawl(self):
        md_gen = DefaultMarkdownGenerator()
        
        # Browser setup for link discovery on JS-heavy sites (Unity)
        browser_config = BrowserConfig(headless=True, enable_stealth=True)
        # We increase wait_for to ensure dynamic sidebars load
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS, 
            magic=True,
            wait_for="js:() => document.querySelectorAll('a').length > 50" # Wait for links to populate
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            while self.queue:
                url = self.queue.pop(0)
                norm_url = url.split('#')[0].rstrip('/')
                if norm_url in self.visited_urls: continue
                
                print(f"Crawling: {url}")
                self.visited_urls.add(norm_url)
                
                # 1. Try Browser Fetch (for JS links/discovery)
                result = await crawler.arun(url, config=run_config)
                
                html_to_process = None
                discovered_links = []
                
                if result.success:
                    print(f"  Browser Success. Discovered links: {len(result.links.get('internal', []))}")
                    html_to_process = result.html
                    # Collect internal links from the rendered DOM
                    for link in result.links.get('internal', []):
                        discovered_links.append(link['href'])
                else:
                    print(f"  Browser blocked or failed: {result.error_message}. Trying Fallback...")
                    # 2. Fallback to Requests (for Cloudflare-blocked or simple sites)
                    html_to_process = await self.fetch_fallback(url)
                    if html_to_process:
                        # Extract links from static HTML manually
                        s = BeautifulSoup(html_to_process, 'lxml')
                        for a in s.find_all('a', href=True):
                            discovered_links.append(urljoin(url, a['href']).split('#')[0])
                
                if not html_to_process:
                    print(f"  Failed to fetch: {url}")
                    continue
                
                # 3. Queue discovered links
                for l in discovered_links:
                    l_norm = l.rstrip('/')
                    if self.is_internal(l) and l_norm not in self.visited_urls and l not in self.queue:
                        self.queue.append(l)

                # 4. Clean and convert to Markdown
                cleaned_html = self.clean_html(html_to_process)
                markdown_result = md_gen.generate_markdown(cleaned_html)
                content = markdown_result.raw_markdown if hasattr(markdown_result, 'raw_markdown') else str(markdown_result)
                
                # 5. Save
                save_path = self.url_to_path(url)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(f"  Saved to {save_path}. Size: {len(content)}")
                # Small delay to keep it polite
                await asyncio.sleep(0.5)

async def main():
    parser = argparse.ArgumentParser(description="Ultimate Universal Doc Crawler")
    parser.add_argument("--url", required=True, help="Seed URL")
    parser.add_argument("--output", default="docs_export", help="Output dir")
    parser.add_argument("--selector", help="Optional main content selector")
    args = parser.parse_args()
    
    crawler = UniversalDocCrawler(args.url, args.output, args.selector)
    await crawler.crawl()

if __name__ == "__main__":
    asyncio.run(main())
