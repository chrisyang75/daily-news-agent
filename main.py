import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news_list(keywords):
    """여러 키워드를 순차적으로 검색해 결과를 합칩니다."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    news_results = []
    
    for query in keywords:
        url = f"https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=1" # 최신순 정렬
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select(".news_tit")[:3] # 키워드당 상위 3개 추출
            
            for item in items:
                title = item.get('title')
                link = item.get('href')
                # 중복 뉴스 제거
                if not any(title in res for res in news_results):
                    news_results.append(f"📍 {title}\n🔗 기사링크: {link}")
        except:
            continue
            
    return news_results[:5] # 섹션당 최대 5개로 제한

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    today = datetime.now().strftime('%Y.%m.%d')
    
    # [수정] 너무 긴 문장 대신, 핵심 단어 조합으로 검색어를 분리했습니다.
    display_keywords = ["BOE 8.6세대 OLED", "CSOT 디스플레이 투자", "IT용 OLED 양산"]
    tgv_keywords = ["반도체 유리기판 TGV", "삼성전기 유리기판", "SKC 앱솔릭스", "LG이노텍 TGV"]
    
    display_news = get_news_list(display_keywords)
    tgv_news = get_news_list(tgv_keywords)
    
    report_text = f"🚀 *{today} 양재훈 대표님 산업 브리핑*\n\n"
    
    report_text += "📊 *디스플레이/중국 시장 동향*\n"
    report_text += "\n\n".join(display_news) if display_news else "- 관련 최신 뉴스를 찾지 못했습니다."
    
    report_text += "\n\n🔬 *반도체 TGV/유리기판 밸류체인*\n"
    report_text += "\n\n".join(tgv_news) if tgv_news else "- 관련 최신 뉴스를 찾지 못했습니다."
    
    report_text += "\n\n_※ 검색어를 세분화하여 수집력을 강화했습니다._"
    
    # 사진 미리보기를 위해 disable_web_page_preview를 False로 둡니다.
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown', disable_web_page_preview=False)

if __name__ == "__main__":
    asyncio.run(send_daily_report())
