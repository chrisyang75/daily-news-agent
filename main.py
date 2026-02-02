import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_real_news(keyword):
    # '관련도순'으로 실제 보도된 기사를 정밀 검색합니다.
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_items = soup.select(".news_wrap")[:2] # 섹션당 가장 확실한 기사 2개씩 추출
        
        results = []
        for item in news_items:
            title_tag = item.select_one(".news_tit")
            title = title_tag.get('title')
            link = title_tag.get('href')
            # 기사 요약 및 사진 포함 여부 확인
            dsc = item.select_one(".news_dsc").text[:120] + "..."
            results.append(f"📍 *{title}*\n{dsc}\n👉 [실제 현장 사진 및 기사 보기]({link})")
        return results
    except Exception as e:
        return [f"❌ 뉴스 수집 중 오류 발생: {e}"]

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    today = datetime.now().strftime('%Y.%m.%d')
    
    # 1. 디스플레이 시장 및 중국 경쟁사 (BOE, CSOT)
    display_news = get_real_news("BOE CSOT OLED 8.6세대 투자 가동 현황")
    # 2. 반도체 TGV 및 유리 기판 밸류체인 (삼성전기, SKC, LG이노텍)
    tech_news = get_real_news("반도체 유리기판 TGV 삼성전기 SKC 앱솔릭스 LG이노텍")
    
    report_text = f"📢 *{today} 양재훈 대표님 산업 브리핑*\n\n"
    
    report_text += "📊 *디스플레이/중국 시장 동향*\n"
    report_text += "\n\n".join(display_news) if display_news else "- 최신 기사가 없습니다."
    
    report_text += "\n\n🔬 *반도체 TGV/유리기판 밸류체인*\n"
    report_text += "\n\n".join(tech_news) if tech_news else "- 최신 기술 소식이 없습니다."
    
    report_text += "\n\n_※ 내일부터는 매일 아침 9시 정각에 최신 기사 링크와 함께 전송됩니다._"
    
    # disable_web_page_preview=False로 설정하여 기사 사진이 자동으로 뜨게 합니다.
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown', disable_web_page_preview=False)

if __name__ == "__main__":
    asyncio.run(send_daily_report())
