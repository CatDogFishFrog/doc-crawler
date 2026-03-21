from ragcrawl import CrawlerConfig, CrawlJob

config = CrawlerConfig(
    seeds=["https://docs.python.org/3/"],
    output={"root_dir": "./python_docs", "mode": "multi"},
    max_depth=6,
    max_pages=2000,
    markdown_config={
        "exclude_tags": ["nav", "footer", "aside"],  # прибирає зайве
        "min_words": 50
    },
    filters={"include": [r"/3/"], "exclude": [r"\.zip$", r"/search"]}
)

job = CrawlJob(config)
result = job.run()  # автоматично збереже все в папках