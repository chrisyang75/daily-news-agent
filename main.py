import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news(query):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    url = f"https://search.naver.com/search.naver?where=news&query={query}&sort=1"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    news_list = []
    for item in soup.select(".news_tit")[:3]:
        title = item.get('title').replace('<', '&lt;').replace('>', '&gt;')
        link = item.get('href')
        news_list.append(f"<b>• {title}</b><br><a href='{link}'>👉 기사 및 사진 보기</a>")
    return news_list

async def main():
    bot = telegram.Bot(BOT_TOKEN)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 키워드를 더 간결하게 조정하여 수집률을 높였습니다.
    display_news = get_news("BOE 8.6세대 OLED 투자")
    tgv_news = get_news("유리기판 TGV 삼성전기 SKC")
    
    msg = f"📅 <b>{today} 양재훈 대표님 산업 브리핑</b>\n\n"
    msg += "<b>[디스플레이/중국 동향]</b>\n" + "\n".join(display_news) + "\n\n"
    msg += "<b>[반도체 TGV/유리기판]</b>\n" + "\n".join(tgv_news)
    
    # HTML 모드로 전송 (마크다운보다 훨씬 안정적입니다)
    await bot.send_message(chat_id=CHAT_ID, text=msg.replace('<br>', '\n'), parse_mode='HTML')

if __name__ == "__main__":
    asyncio.run(main())
