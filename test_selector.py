import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def test():
    from crawl4ai.content_filter_strategy import PruningContentFilter
    from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed")
    )
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://api.arcade.academy/en/stable/programming_guide/sound.html", config=run_config)
        print(f"Success: {result.success}")
        if result.success:
            print(f"Markdown length: {len(result.markdown)}")
            print(f"Found {len(result.links.get('internal', []))} internal links")
            with open("test_output.md", "w", encoding="utf-8") as f:
                f.write(result.markdown if isinstance(result.markdown, str) else result.markdown.raw_markdown)

if __name__ == "__main__":
    asyncio.run(test())
