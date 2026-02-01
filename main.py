import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 설정 정보
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news(keyword):
    """네이버에서 키워드로 최신 뉴스를 검색해 제목과 링크를 가져옵니다."""
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    news_list = []
    items = soup.select(".news_tit")[:3]  # 상위 3개 뉴스만 가져옴
    for item in items:
        title = item.get('title')
        link = item.get('href')
        news_list.append(f"- {title}\n  👉 [기사보기]({link})")
    return news_list

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    today = datetime.now().strftime('%Y.%m.%d')
    
    # 키워드별 뉴스 수집
    display_news = get_news("디스플레이 BOE")
    tgv_news = get_news("반도체 TGV 유리기판")
    
    report_text = f"📅 *{today} AI 산업 자동 리포트*\n\n"
    
    report_text += "📺 *디스플레이/BOE 관련*\n"
    report_text += "\n".join(display_news) if display_news else "- 관련 뉴스를 찾지 못했습니다."
    
    report_text += "\n\n🔬 *TGV/유리기판 관련*\n"
    report_text += "\n".join(tgv_news) if tgv_news else "- 관련 뉴스를 찾지 못했습니다."
    
    report_text += "\n\n_※ 본 리포트는 AI가 매일 아침 자동으로 수집합니다._"
    
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == "__main__":
    asyncio.run(send_daily_report())
