import asyncio
import argparse
import sys
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List, Optional

import httpx
from bs4 import BeautifulSoup
import trafilatura

# Примусово встановлюємо UTF-8 для виводу в консоль Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

class SiteProcessor:
    def __init__(self, base_url: str):
        parsed = urlparse(base_url)
        self.base_domain: str = parsed.netloc
        # Базовий шлях для обмеження краулінгу
        path = parsed.path
        if path.endswith(".html"):
            # Якщо вказано конкретний файл, базовим шляхом вважаємо його папку
            self.base_path = os.path.dirname(path).rstrip("/") + "/"
        else:
            self.base_path = path if path.endswith("/") else path + "/"
            
        self.base_url: str = base_url
        self.seen_urls: Set[str] = set()
        self.tree_data: Dict[str, List[str]] = {}
        
        # Директорія для MD файлів (домен поруч зі скриптом)
        self.root_dir: Path = Path(self.base_domain)

    def is_internal(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc != self.base_domain:
            return False
        
        # Дозволяємо все, що знаходиться всередині або нижче базового шляху
        return parsed.path.startswith(self.base_path)

    def clean_url(self, url: str) -> str:
        parsed = urlparse(url)
        # Видаляємо фрагменти та query
        path = parsed.path
        if not path: path = "/"
        # Зберігаємо URL як є, прибираємо лише лишні пробіли
        return f"{parsed.scheme}://{parsed.netloc}{path}"

    async def crawl(self, current_url: str, client: Optional[httpx.AsyncClient] = None, max_depth: int = 5, current_depth: int = 0):
        if current_depth > max_depth:
            return
        
        url = self.clean_url(current_url)
        if url in self.seen_urls:
            return
        
        self.seen_urls.add(url)
        print(f"[{current_depth}] Crawling: {url}...")
        
        try:
            # Trafilatura fetch_url набагато стабільніша на цьому сайті
            html_content = trafilatura.fetch_url(url)
            if not html_content:
                # Спробуємо з index.html, якщо це була папка
                if url.endswith("/"):
                    alt_url = url + "index.html"
                    print(f"  Trying alternate: {alt_url}")
                    html_content = trafilatura.fetch_url(alt_url)
                
                if not html_content:
                    print(f"  Warning: Failed to fetch {url}")
                    return

            soup = BeautifulSoup(html_content, "lxml")
            links_to_crawl = []
            for a in soup.find_all("a", href=True):
                full_url = urljoin(url, a["href"])
                if self.is_internal(full_url):
                    clean_link = self.clean_url(full_url)
                    if clean_link not in self.seen_urls and clean_link != url:
                        if clean_link not in links_to_crawl:
                            links_to_crawl.append(clean_link)
            
            if links_to_crawl:
                self.tree_data[url] = links_to_crawl
                for link in links_to_crawl:
                    # Рекурсія без httpx тепер простіша
                    await self.crawl(link, None, max_depth, current_depth + 1)
            
        except Exception as e:
            print(f"Error crawling {url}: {e}", file=sys.stderr)

    def display_tree(self):
        print(f"\nSite Tree for {self.base_url}:")
        # Сортуємо по довжині шляху, щоб дерево виглядало логічно
        sorted_urls = sorted(list(self.seen_urls), key=lambda x: (x.count("/"), x))
        for url in sorted_urls:
            rel_path = url.replace(self.base_url, "")
            if not rel_path:
                rel_path = "/"
            depth = rel_path.count("/")
            indent = "  " * depth
            print(f"{indent}└── {rel_path if rel_path != '/' else self.base_url}")

    def get_source_url(self, url: str) -> Optional[str]:
        # Перетворюємо HTML URL у посилання на .rst.txt у папці _sources
        parsed = urlparse(url)
        path = parsed.path
        
        if not path.endswith(".html"):
            if not path.endswith("/"): path += "/"
            path += "index.html"
            
        # Для ReadTheDocs/Sphinx типий шлях: /en/stable/path/to/page.html
        # Має стати: /en/stable/_sources/path/to/page.rst.txt
        parts = path.strip("/").split("/")
        if len(parts) >= 2:
            # Припускаємо, що перші два елементи - це мова та версія (наприклад, en/stable)
            lang, version = parts[0], parts[1]
            rest = "/".join(parts[2:])
            source_path = f"/{lang}/{version}/_sources/{rest.replace('.html', '.rst.txt')}"
        else:
            source_path = f"/_sources/{path.replace('.html', '.rst.txt')}"
            
        source_path = source_path.replace("//", "/")
        return f"{parsed.scheme}://{parsed.netloc}{source_path}"

    async def save_to_markdown(self, url: str):
        try:
            # Пріоритет: RST.txt
            source_url = self.get_source_url(url)
            content = None
            
            if source_url:
                print(f"  Fetching RST source: {source_url}...")
                content = trafilatura.fetch_url(source_url)
                if content:
                    print(f"  RST source found for {url}")
            
            if not content:
                # Палбек на HTML
                print(f"  Falling back to HTML for {url}...")
                html_raw = trafilatura.fetch_url(url)
                if html_raw:
                    content = trafilatura.extract(html_raw, output_format="markdown", include_links=True, include_images=True)

            if not content:
                print(f"  Failed to get content for {url}")
                return

            # Шлях до файлу (визначаємо по URL)
            parsed = urlparse(url)
            p = parsed.path.strip("/")
            if not p or url == self.base_url:
                file_path = self.root_dir / "index.md"
            else:
                # Зберігаємо структуру папок
                file_path = self.root_dir / f"{p}.md"
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {url}\n\n")
                f.write(content)
            
            print(f"Saved: {file_path}")
            
        except Exception as e:
            print(f"Error saving {url}: {e}", file=sys.stderr)

    async def process(self, modes: List[str]):
        print(f"Processing {self.base_url}...")
        await self.crawl(self.base_url)
        
        if "tree" in modes:
            self.display_tree()
            
        if "md" in modes:
            print(f"\nExporting to Markdown in directory: {self.root_dir}")
            for url in self.seen_urls:
                await self.save_to_markdown(url)

async def main():
    parser = argparse.ArgumentParser(description="Site Tree & MD Extractor")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--tree", action="store_true", help="Display site tree")
    parser.add_argument("--md", action="store_true", help="Extract content to Markdown files")
    
    args = parser.parse_args()
    
    modes = []
    if args.tree: modes.append("tree")
    if args.md: modes.append("md")
    
    if not modes:
        print("Please specify --tree or --md")
        return

    processor = SiteProcessor(args.url)
    await processor.process(modes)

if __name__ == "__main__":
    asyncio.run(main())
