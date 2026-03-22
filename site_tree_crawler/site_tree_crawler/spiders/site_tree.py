import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

class SiteTreeSpider(scrapy.Spider):
    name = "site_tree"

    def __init__(self, start_url=None, **kwargs):
        super().__init__(**kwargs)
        if not start_url:
            raise ValueError("scrapy crawl site_tree -a start_url=...")
        
        self.start_urls = [start_url]
        parsed = urlparse(start_url)
        self.domain = parsed.netloc
        self.allowed_domains = [self.domain]
        
        # Динамічне обмеження тільки на початковий шлях (універсально!)
        base_path = parsed.path.rstrip('/')
        self.allow_regex = (
            r'^https?://' + 
            re.escape(self.domain) + 
            re.escape(base_path) + 
            r'(/.*)?$'
        )
        
        self.tree = defaultdict(list)

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,          # ← ВКЛЮЧАЄМО JS-РЕНДЕРИНГ
                "playwright_page_methods": [],  # можна додати wait_for_selector пізніше
                "parent": None,
                "depth": 0
            }
        )

    def parse(self, response):
        current_url = response.url
        parent = response.meta.get("parent")
        depth = response.meta.get("depth", 0)

        if parent:
            self.tree[parent].append(current_url)

        extractor = LinkExtractor(
            allow=[self.allow_regex],
            allow_domains=[self.domain],
            unique=True,
        )
        for link in extractor.extract_links(response):  # ← тепер на РЕНДЕРЕНОМУ HTML!
            if link.url != current_url:
                yield scrapy.Request(
                    link.url,
                    callback=self.parse,
                    meta={
                        "playwright": True,   # кожна сторінка теж рендериться
                        "parent": current_url,
                        "depth": depth + 1
                    }
                )

    def closed(self, reason):
        root_url = self.start_urls[0]
        root_elem = ET.Element("site_tree", {"root": root_url})

        def build_xml(url: str, parent_elem: ET.Element):
            page = ET.SubElement(parent_elem, "page", {"url": url})
            for child in sorted(self.tree.get(url, [])):
                build_xml(child, page)

        build_xml(root_url, root_elem)

        xml_str = ET.tostring(root_elem, encoding="unicode")
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

        filename = f"site_tree_unity_scriptreference_full.xml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        self.logger.info(
            f"✅ ДЕРЕВО ЗБЕРЕЖЕНО: {filename} "
            f"({len(self.tree) + 1} сторінок — ПОВНЕ, з JS-рендерингом!)"
        )