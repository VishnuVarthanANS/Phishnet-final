import re
from urllib.parse import urlparse

def safe_text(x):
    return re.sub(r"\s+", " ", (x or "")).strip().lower()

def extract_features(url: str, html: str, js: str):
    features = {}

    text = safe_text(html + " " + js)

    features["has_login_form"] = bool(re.search(r"(password|login|signin|auth)", text))
    features["has_external_js"] = bool(re.search(r"https?://", js))
    features["uses_iframe"] = "<iframe" in html.lower()
    features["suspicious_keywords"] = len(re.findall(
        r"(verify|account|bank|secure|update|confirm|reset|wallet|payment)", text
    ))

    domain = urlparse(url).netloc
    features["is_ip_domain"] = bool(re.match(r"\d+\.\d+\.\d+\.\d+", domain))

    return features
