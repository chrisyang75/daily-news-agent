import os
import asyncio
import telegram

# 깃허브 금고(Secrets)에서 정보를 가져옵니다
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    
    # 이 부분에 제가 매일 생성해드리는 리포트 내용을 넣습니다
    report_text = """
*📅 2026.02.01 리포트: Display & TGV*
- [중국] BOE 청두 B16 라인 가동률 35% 달성
- [TGV] 필옵틱스 차세대 드릴링 장비 삼성전기 입고 개시
- 👉 [기사 확인하기](https://www.kdia.org/bbs/bbsView.jsp?mgrId=40&bbsId=16895)
    """
    
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(send_daily_report())
