import trafilatura
import httpx
import asyncio

async def test():
    url = "https://api.arcade.academy/en/stable/programming_guide/sprites/spritelists.html"
    source_url = "https://api.arcade.academy/en/stable/_sources/programming_guide/sprites/spritelists.rst.txt"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Testing HTML with httpx: {url}")
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        r = await client.get(url)
        print(f"  Status: {r.status_code}")

    print(f"Testing RST with trafilatura.fetch_url: {source_url}")
    res = trafilatura.fetch_url(source_url)
    if res:
        print(f"  Success! Length: {len(res)}")
    else:
        print("  Failed to fetch RST")

if __name__ == "__main__":
    asyncio.run(test())
