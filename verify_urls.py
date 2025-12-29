import requests
import json

urls = [
    "http://nobell.it/70ffb52d079109dca5664cce6f317373782/login.SkyP.customer&nav=1/loading.php",
    "http://www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php",
    "http://rvce.edu.in", 
    "https://www.google.com"
]

print("🔍 Testing URLs against SecureSentinel API...\n")

for url in urls:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/detect",
            json={"text": url},
            timeout=5
        )
        data = response.json()
        score = data.get('max_risk_score', 0)
        status = "🔴 PHISHING" if score > 0.8 else "🟠 SUSPICIOUS" if score > 0.5 else "🟢 SAFE"
        print(f"{status} [{score:.2f}]: {url[:60]}...")
    except Exception as e:
        print(f"❌ ERROR: {url[:30]}... - {e}")
