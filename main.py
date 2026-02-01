import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news(keyword):
    # '관련도순' 검색으로 주말에도 알찬 정보를 가져옵니다.
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
    
    # 대표님의 관심사를 반영한 확장 키워드 세트
    # 1. 디스플레이 시장 전반 및 중국 경쟁사 (CSOT, BOE 등)
    market_news = get_news("디스플레이 시장 전망 OLED CSOT BOE 전략")
    # 2. 핵심 기술 (TGV 및 유리기판)
    tech_news = get_news("반도체 유리기판 TGV 공정 기술")
    
    report_text = f"📅 *{today} 산업 마켓 브리핑*\n\n"
    
    report_text += "📊 *디스플레이 시장 및 경쟁사 동향*\n"
    report_text += "\n".join(market_news) if market_news else "- 최신 시장 분석 뉴스가 없습니다."
    
    report_text += "\n\n🔬 *차세대 TGV 및 소부장 기술*\n"
    report_text += "\n".join(tech_news) if tech_news else "- 관련 기술 뉴스를 찾지 못했습니다."
    
    report_text += "\n\n_※ 대표님의 전문 분야인 디스플레이와 TGV를 중심으로 시장을 넓게 분석했습니다._"
    
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == "__main__":
    asyncio.run(send_daily_report())
