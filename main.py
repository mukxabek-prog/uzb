import urllib.parse
import aiohttp

async def generate_video_pollinations(prompt: str):
    # Promptni URL formatiga o'tkazish
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Pollinations bepul API manzili
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&seed=42"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_bytes = await response.read()
                with open("output.jpg", "wb") as f:
                    f.write(image_bytes)
                return "output.jpg"
    return None
