import os
import asyncio
import telegram

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

async def send_daily_report():
    bot = telegram.Bot(token=BOT_TOKEN)
    
    report_text = """
*📅 2026.02.01 산업 데일리 리포트*

---
*## PART 1. 디스플레이(Display) 뉴스*
*1. [중국] BOE 청두 B16 라인 가동 및 출하 성공*
- 예상보다 5개월 앞당겨 운영 단계 진입
- [현장 사진 및 기사 확인](https://www.kdia.org/bbs/bbsView.jsp?mgrId=40&bbsId=16895)

---
*## PART 2. 반도체 TGV 및 유리 기판 뉴스*
*1. [삼성] 필옵틱스·켐트로닉스 TGV 밸류체인 강화*
- 레이저 타공 및 식각 공정 수율 확보 총력
- [기술 상세 사진 및 기사 확인](https://biz.chosun.com/it-science/ict/2026/01/16/UCZ63LS4DNGE7FPUJLSQUK7KBE/)
"""
    
    await bot.send_message(chat_id=CHAT_ID, text=report_text, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(send_daily_report())
