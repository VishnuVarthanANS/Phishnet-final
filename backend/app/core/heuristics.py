import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict

URL_SHORTENERS = ["bit.ly","tinyurl.com","t.co","goo.gl"]

def analyze_heuristics(url: str="", html: str="", js: str="") -> Dict:
    score = 0.0
    reasons = []

    soup = BeautifulSoup(html or "", "html.parser")
    text = (html + " " + js).lower()

    # 1. Password field
    if soup.find("input", {"type": "password"}):
        score += 0.25
        reasons.append("password_field")

    # 2. Lure keywords
    if re.search(r"(verify|confirm|secure|account|login|signin|update)", text):
        score += 0.15
        reasons.append("lure_language")

    # 3. External form submission
    for form in soup.find_all("form"):
        action = form.get("action","")
        if action.startswith("http"):
            page_domain = urlparse(url).netloc
            form_domain = urlparse(action).netloc
            if page_domain and form_domain and page_domain not in form_domain:
                score += 0.30
                reasons.append("external_form_post")

    # 4. IP-based URL
    domain = urlparse(url).netloc
    if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
        score += 0.20
        reasons.append("ip_based_url")

    # 5. URL shorteners
    if any(s in domain for s in URL_SHORTENERS):
        score += 0.25
        reasons.append("url_shortener")

    # 6. Abnormal domain length
    if len(domain) > 35:
        score += 0.10
        reasons.append("long_domain")

    score = min(score, 1.0)
    return {"suspicion_score": round(score,2), "reasons": reasons}


