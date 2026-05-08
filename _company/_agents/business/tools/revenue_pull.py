import json
import os
import random
from datetime import datetime, timedelta

def pull_paypal_revenue():
    """
    페이팔(PayPal) REST API를 호출하여 매출 데이터를 추출하는 스크립트.
    현재는 자격 증명이 없는 상태이므로, PayPal API 구조에 맞춘 더미 데이터를 반환합니다.
    (Harness Engineering: 토큰 부재 시 Mock 모드로 동작하는 Circuit Breaker 적용)
    """
    client_id = os.environ.get("PAYPAL_CLIENT_ID")
    client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")
    
    data = []
    end_date = datetime.now()
    
    if not client_id or not client_secret:
        print("[System] PayPal 토큰이 감지되지 않았습니다. Mock 데이터를 생성합니다.")
        # 최근 30일 더미 데이터 생성
        for i in range(30):
            date_str = (end_date - timedelta(days=29-i)).strftime("%Y-%m-%d")
            data.append({
                "date": date_str,
                "gross_volume": round(random.uniform(50, 300), 2),
                "net_volume": round(random.uniform(40, 280), 2),
                "currency": "USD",
                "transactions": random.randint(1, 10),
                "gateway": "PayPal"
            })
    else:
        # 실제 PayPal API 호출 로직 (To be implemented)
        # requests.post("https://api-m.paypal.com/v1/oauth2/token", ...)
        pass
        
    return data

if __name__ == "__main__":
    revenue_data = pull_paypal_revenue()
    
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "revenue.json")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(revenue_data, f, indent=2)
        
    print(f"[Success] 매출 데이터가 {output_file} 에 저장되었습니다.")
