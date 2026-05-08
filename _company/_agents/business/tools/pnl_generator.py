import json
import os
import sys
from datetime import datetime

# Windows 콘솔 출력 시 이모지 깨짐 방지
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import pandas as pd
except ImportError:
    print("[Error] pandas 패키지가 설치되지 않았습니다. venv 환경에서 실행 중인지 확인하세요.")
    sys.exit(1)

def generate_pnl_report():
    """
    revenue_pull.py 와 analytics_pull.py가 생성한 JSON 데이터를 병합하여
    마크다운 형태의 P&L(손익계산서) 보고서를 작성합니다.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    rev_file = os.path.join(data_dir, "revenue.json")
    ana_file = os.path.join(data_dir, "analytics.json")
    
    if not os.path.exists(rev_file) or not os.path.exists(ana_file):
        print("[System] 데이터 파일이 부족합니다. revenue_pull.py 와 analytics_pull.py 를 먼저 실행하세요.")
        return None
        
    with open(rev_file, "r", encoding="utf-8") as f:
        rev_data = json.load(f)
    with open(ana_file, "r", encoding="utf-8") as f:
        ana_data = json.load(f)
        
    df_rev = pd.DataFrame(rev_data)
    df_ana = pd.DataFrame(ana_data)
    
    if df_rev.empty or df_ana.empty:
        print("[System] 데이터가 비어 있습니다.")
        return None
        
    # Date를 기준으로 병합
    df_merged = pd.merge(df_ana, df_rev, on="date", how="inner")
    
    # 요약 통계 계산
    total_visitors = df_merged['visitors'].sum()
    total_revenue = df_merged['net_volume'].sum()
    arpu = total_revenue / total_visitors if total_visitors > 0 else 0
    
    # 최근 일자 추출
    latest_date = df_merged['date'].max()
    
    report_md = f"""# 📊 Business P&L Report ({latest_date} 기준)

## 💡 요약 (Summary)
- **총 방문자수 (Visitors)**: {total_visitors:,} 명
- **총 순매출 (Net Revenue)**: ${total_revenue:,.2f} USD
- **방문자 당 평균 매출 (ARPU)**: ${arpu:,.2f} USD

## 📈 세부 지표 (Details)
- **최고 매출일**: {df_merged.loc[df_merged['net_volume'].idxmax()]['date']} (${df_merged['net_volume'].max():,.2f})
- **최고 트래픽일**: {df_merged.loc[df_merged['visitors'].idxmax()]['date']} ({df_merged['visitors'].max():,} 명)

## 🤖 Business Agent 코멘트
현재 트래픽 대비 전환율과 ARPU를 고려할 때, **PayPal 결제 이탈률 방어**와 **객단가(AOV) 상승 전략**이 필요합니다.
"""
    return report_md

def save_and_approve(report_md):
    """
    보고서를 승인 대기 폴더에 저장하고, 텔레그램 발송 안전 게이트를 실행합니다.
    (Harness Engineering: Circuit Breaker & Safety Gate)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    approvals_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "approvals", "pending")
    os.makedirs(approvals_dir, exist_ok=True)
    
    filename = os.path.join(approvals_dir, f"pnl_report_{timestamp}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print(f"\n[System] 보고서 초안이 생성되었습니다: {filename}")
    print("=" * 40)
    print(report_md)
    print("=" * 40)
    
    # Safety Gate
    print("\n⚠️ [Circuit Breaker] Telegram 자동 발송 안전 게이트")
    choice = input("대표님, 위 보고서를 텔레그램으로 발송하시겠습니까? (y/N): ").strip().lower()
    
    if choice == 'y':
        # 텔레그램 발송 로직 (To be implemented with requests)
        print("[System] 🚀 텔레그램 발송 완료! (더미: 실제 발송 모듈 연동 필요)")
        
        # 보류 폴더에서 승인 폴더로 이동 (선택적)
        approved_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "approvals", "approved")
        os.makedirs(approved_dir, exist_ok=True)
        os.rename(filename, os.path.join(approved_dir, f"pnl_report_{timestamp}.md"))
    else:
        print("[System] 🛑 발송이 취소되었습니다. 보고서는 대기 폴더(pending)에 유지됩니다.")

if __name__ == "__main__":
    md = generate_pnl_report()
    if md:
        save_and_approve(md)
