
# import os
# from dotenv import load_dotenv
# load_dotenv()
# from langchain_google_genai import ChatGoogleGenerativeAI
# from browser_use import Agent
# import asyncio

# async def main():
#     task = input("Enter your task: ")  
#     llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest")
#     agent = Agent(llm=llm, task=task)
#     result = await agent.run()
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())
    
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from playwright.async_api import async_playwright
import asyncio

async def main():
    task = input("Enter your task ")
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest")
    
    agent = Agent(llm=llm, task=task)
    

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        context = await browser.new_context(record_video_dir="videos/") 
        
        page = await context.new_page()
        

        if "Navigate" in task:
            url = task.split("to ")[-1] if "to " in task else "https://example.com"
            await page.goto(url)
            print(f"Navigated to {url}")
        
        if "click" in task:

            button_text = task.split("click ")[-1] if "click " in task else "button"
            await page.click(f"text={button_text}")
            print(f"Clicked button with text: {button_text}")
        
        if "scroll" in task:
            await page.mouse.wheel(0, 1000)  
            print("Scrolled down by 1000 pixels")
        
        if "extract content" in task:
            content = await page.text_content("h1")  # Extracting content from the first h1 tag
            result = []
            result.append(content)
            print(f"Extracted content: {content}")
        

        if "scroll to" in task:
            text_to_scroll = task.split("scroll to ")[-1]
            element = await page.locator(f"text={text_to_scroll}").element_handle()
            await element.scroll_into_view_if_needed()
            print(f"Scrolled to text: {text_to_scroll}")


        result = await agent.run()  
        print(result)
        await asyncio.sleep(10)
        # await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
