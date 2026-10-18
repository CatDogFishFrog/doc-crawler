# ──────────────────────────────────────────────────────────────
# Основні налаштування проєкту
# ──────────────────────────────────────────────────────────────

BOT_NAME = "site_tree_crawler"

SPIDER_MODULES = ["site_tree_crawler.spiders"]
NEWSPIDER_MODULE = "site_tree_crawler.spiders"

# ──────────────────────────────────────────────────────────────
# Ідентифікація та етика
# ──────────────────────────────────────────────────────────────

ROBOTSTXT_OBEY = True
ROBOTSTXT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# ──────────────────────────────────────────────────────────────
# Playwright (браузерний рендеринг) — обов'язкові налаштування
# ──────────────────────────────────────────────────────────────

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 45000          # 45 секунд — оптимально для Unity
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 60000,
    "args": ["--disable-gpu", "--no-sandbox"]          # прискорення на Windows
}

PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 8                   # скільки вкладок одночасно в одному браузері

# ──────────────────────────────────────────────────────────────
# Швидкість і обмеження навантаження
# ──────────────────────────────────────────────────────────────

CONCURRENT_REQUESTS = 12                               # головний важіль прискорення
CONCURRENT_REQUESTS_PER_DOMAIN = 6                     # не більше 6 одночасно до unity3d.com

DOWNLOAD_DELAY = 0.3                                   # базова затримка
RANDOMIZE_DOWNLOAD_DELAY = True                        # додає випадковість ±50%, виглядає природніше

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 8.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0                  # ціль — 4 запити одночасно в середньому
AUTOTHROTTLE_DEBUG = False                             # True тільки для дебагу

DEPTH_LIMIT = 8                                        # для ScriptReference вистачить 5–6, але безпечно

# ──────────────────────────────────────────────────────────────
# Логування та моніторинг
# ──────────────────────────────────────────────────────────────

LOG_LEVEL = "INFO"                                     # або "DEBUG" якщо хочеш бачити кожен лінк
LOGSTATS_INTERVAL = 30                                 # статистика кожні 30 секунд

# ──────────────────────────────────────────────────────────────
# Інше (кеш, кодування тощо)
# ──────────────────────────────────────────────────────────────

FEED_EXPORT_ENCODING = "utf-8"
HTTPCACHE_ENABLED = True                               # кеш відповідей — прискорить повторні запуски
HTTPCACHE_EXPIRATION_SECS = 86400                      # 24 години
HTTPCACHE_DIR = ".scrapy_httpcache"