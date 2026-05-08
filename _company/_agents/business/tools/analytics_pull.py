import json
import os
import random
from datetime import datetime, timedelta

def pull_generic_analytics():
    """
    범용 트래픽 데이터 추출 스크립트.
    어떤 Analytics 툴을 쓸지 결정되지 않았으므로, 인터페이스만 잡아둔 Generic Placeholder입니다.
    """
    provider = os.environ.get("ANALYTICS_PROVIDER", "None")
    
    data = []
    end_date = datetime.now()
    
    print(f"[System] 지정된 Analytics Provider: {provider}. Mock 트래픽 데이터를 생성합니다.")
    # 최근 30일 더미 데이터 생성
    for i in range(30):
        date_str = (end_date - timedelta(days=29-i)).strftime("%Y-%m-%d")
        visitors = random.randint(100, 1000)
        pageviews = int(visitors * random.uniform(1.2, 3.5))
        data.append({
            "date": date_str,
            "visitors": visitors,
            "pageviews": pageviews,
            "bounce_rate": round(random.uniform(30.0, 70.0), 2),
            "avg_session_duration_sec": random.randint(30, 180)
        })
        
    return data

if __name__ == "__main__":
    analytics_data = pull_generic_analytics()
    
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "analytics.json")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analytics_data, f, indent=2)
        
    print(f"[Success] 트래픽 데이터가 {output_file} 에 저장되었습니다.")
