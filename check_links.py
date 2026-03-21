import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://api.arcade.academy/en/stable/programming_guide/sprites/spritelists.html"
html = trafilatura.fetch_url(url)
if html:
    print(f"HTML length: {len(html)}")
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a", href=True)
    print(f"Found {len(links)} links")
    for a in links[:10]:
        print(f"  {a['href']} -> {urljoin(url, a['href'])}")
else:
    print("Failed to fetch HTML")
