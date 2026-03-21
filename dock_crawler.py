import asyncio
import os
import sys
import argparse
import requests
import time
from urllib.parse import urljoin, urlparse
from typing import Set, List
from bs4 import BeautifulSoup
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class DocCrawler:
    def __init__(self, start_url: str, output_dir: str, css_selector: str = None):
        parsed = urlparse(start_url)
        # Use the directory of the start URL as base_url
        path = parsed.path
        if not path.endswith("/"):
            path = os.path.dirname(path)
        
        self.base_url = f"{parsed.scheme}://{parsed.netloc}{path.rstrip('/')}/"
        self.start_url = start_url
        self.output_dir = output_dir
        self.css_selector = css_selector
        self.visited_urls: Set[str] = set()
        self.queue: List[str] = [self.start_url]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        })
        
        os.makedirs(self.output_dir, exist_ok=True)

    def is_internal(self, url: str) -> bool:
        """Check if URL is within the base URL scope."""
        return url.startswith(self.base_url)

    def url_to_path(self, url: str) -> str:
        """Map URL to a local file system path."""
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

    async def fetch_page(self, url: str) -> str:
        """Fetch page content using requests in a thread."""
        def _fetch():
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        
        try:
            return await asyncio.to_thread(_fetch)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl(self):
        # Generator for converting extracted HTML to markdown
        md_generator = DefaultMarkdownGenerator()

        while self.queue:
            current_url = self.queue.pop(0)
            norm_url = current_url.rstrip("/")
            if norm_url in self.visited_urls:
                continue
            
            print(f"Crawling: {current_url}")
            self.visited_urls.add(norm_url)
            
            # Polite delay
            await asyncio.sleep(1)
            
            html_content = await self.fetch_page(current_url)
            if not html_content:
                continue
            
            soup = BeautifulSoup(html_content, 'lxml')
            
            # 1. Link discovery on the FULL page (before cleaning)
            added_count = 0
            for link in soup.find_all('a', href=True):
                link_url = link['href']
                full_url = urljoin(current_url, link_url).split("#")[0].split("?")[0].rstrip("/")
                
                if self.is_internal(full_url) and full_url not in self.visited_urls:
                    if full_url not in self.queue:
                        self.queue.append(full_url)
                        added_count += 1
            
            print(f"Found links. Added {added_count} new to queue. Queue size: {len(self.queue)}")

            # 2. Content extraction and cleaning
            # Explicitly remove noise elements mentioned by user and common ones
            noise_selectors = [
                '.wy-side-scroll', 'nav', 'footer', 'aside', 
                '.headerlink', '.sourcelink', 'script', 'style',
                '.rst-footer-buttons', '.rst-content-bottom'
            ]
            for ns in noise_selectors:
                for noise in soup.select(ns):
                    noise.decompose()

            # Targeted extraction of main content
            final_html = None
            selectors_to_try = []
            if self.css_selector:
                selectors_to_try.append(self.css_selector)
            
            # Universal doc selectors (Sphinx specific first, then generic)
            selectors_to_try.extend(['div[role="main"]', 'main', 'article', '#content', '.content'])

            for selector in selectors_to_try:
                target = soup.select_one(selector)
                if target:
                    final_html = str(target)
                    print(f"Extracted content using selector: {selector}")
                    break
            
            if not final_html:
                # Fallback to body content if no main area found
                final_html = str(soup.body) if soup.body else str(soup)
                print("Warning: No main content selector found. Using body.")

            # 3. Convert cleaned HTML to Markdown using Crawl4AI engine
            try:
                # Directly using the markdown generator on the HTML string
                # crawl4ai's generator expects a string for generate_markdown
                from crawl4ai.markdown_generation_strategy import MarkdownGenerationResult
                result = md_generator.generate_markdown(final_html)
                final_content = result.raw_markdown if hasattr(result, 'raw_markdown') else str(result)
                
                print(f"Success! Markdown length: {len(final_content)}")
                
                # Save markdown content
                local_path = self.url_to_path(current_url)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(final_content)
            except Exception as e:
                print(f"Error generating markdown for {current_url}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Hybrid Documentation to Markdown Crawler (Requests + Crawl4AI)")
    parser.add_argument("--url", required=True, help="Base URL of the documentation")
    parser.add_argument("--output", default="docs_export", help="Output directory name")
    parser.add_argument("--selector", help="CSS selector for the main content (optional)")
    
    args = parser.parse_args()
    
    crawler = DocCrawler(args.url, args.output, args.selector)
    await crawler.crawl()

if __name__ == "__main__":
    asyncio.run(main())
