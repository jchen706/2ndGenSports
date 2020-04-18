import asyncio
import pyppeteer
from pyppeteer import launch

async def get_browser():
    print("browser")
    return await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,args=['--no-sandbox'])

async def get_page(url):
    print('here get page')
    browser = await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,args=['--no-sandbox'])
    print('here get page1')
    page = await browser.newPage()
    print('here get page2')
    await page.goto(url)
    print('here get page3')
    #content = await page.evaluate('document.body', force_expr=True)
    html = await page.content()
    print('here get page4')
    await browser.close()
    print('return')
    return html

def get_url_async(url):
    print('render')
    try:
            result = asyncio.get_event_loop().run_until_complete(get_page('https://byucougars.com/roster/m-basketball/'))
    except Exception as err1:
            print(err1.message())
    print(result)
    return result