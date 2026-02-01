import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news(keyword):
    # sort=0으로 변경하여 '관련도순'으로 검색 (주말에도 기사가 잘 잡힙니다)
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_list = []
        items = soup.select(".news_tit")[:3]
        
        for item in items:
            title = item.get('title')
            link = item.get('href')
            news_list.append(f"- {title}\n  👉 [기사보기]({link})")
        return news_list
    except:
        return []

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    today = datetime.now().strftime('%Y.%m.%d')
    
    # 키워드를 조금 더 포괄적으로 넓혔습니다
    display_news = get_news("디스플레이 OLED BOE")
    tgv_news = get_news("반도체 TGV 유리 기판 필옵틱스")
    
    report_text = f"📅 *{today} AI 산업 자동 리포트*\n\n"
    
    report_text += "📺 *디스플레이 관련 뉴스*\n"
    report_text += "\n".join(display_news) if display_news else "- 현재 시각 관련 뉴스가 없습니다."
    
    report_text += "\n\n🔬 *TGV/유리기판 관련 뉴스*\n"
    report_text += "\n".join(tgv_news) if tgv_news else "- 현재 시각 관련 뉴스가 없습니다."
    
    report_text += "\n\n_※ 검색 범위를 넓혀 주말 뉴스까지 포함했습니다._"
    
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == "__main__":
    asyncio.run(send_daily_report())
