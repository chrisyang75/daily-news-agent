import os
import asyncio
import telegram
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def get_news(query):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    # 한글 검색어 인코딩을 추가하여 수집 정확도를 높였습니다.
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded_query}&sort=1"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_list = []
        
        # .news_tit 선택자 내의 '텍스트'를 직접 가져오도록 수정했습니다.
        items = soup.select(".news_tit")
        if not items:
            return ["• 현재 수집된 최신 뉴스가 없습니다."]

        for item in items[:3]:
            # item.get('title')은 비어있는 경우가 많으므로 get_text()를 권장합니다.
            title = item.get_text().strip().replace('<', '&lt;').replace('>', '&gt;')
            link = item.get('href')
            # <br> 대신 텔레그램 표준 줄바꿈 \n을 사용합니다.
            news_list.append(f"<b>• {title}</b>\n<a href='{link}'>👉 기사 보기</a>")
        return news_list
    except Exception as e:
        return [f"• 수집 오류 발생: {str(e)}"]

async def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 대표님의 관심사를 반영한 키워드로 뉴스 수집
    display_news = get_news("BOE 8.6세대 OLED 가동")
    tgv_news = get_news("삼성전기 유리기판 TGV 사업화")
    
    msg = f"📅 <b>{today} 양재훈 대표님 산업 브리핑</b>\n\n"
    msg += "<b>[디스플레이/중국 동향]</b>\n" + "\n".join(display_news) + "\n\n"
    msg += "<b>[반도체 TGV/유리기판]</b>\n" + "\n".join(tgv_news)
    
    # HTML 모드 전송 (disable_web_page_preview로 메시지를 깔끔하게 유지)
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='HTML', disable_web_page_preview=True)

if __name__ == "__main__":
    asyncio.run(main())
