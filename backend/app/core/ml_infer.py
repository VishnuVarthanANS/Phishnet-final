import onnxruntime as rt
import numpy as np
from pathlib import Path
from urllib.parse import urlparse
import re

MODEL_PATH = Path(__file__).parent.parent / "models" / "sample_model.onnx"
sess = None

def extract_features(url: str, html: str):
    domain = urlparse(url).netloc

    having_ip = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0
    url_length = 1 if len(url) > 54 else 0
    prefix_suffix = 1 if "-" in domain else 0
    having_subdomain = 1 if domain.count(".") > 2 else 0
    ssl = 1 if url.startswith("https") else 0
    request_url = 1 if html.count("http") > 10 else 0
    anchor_url = 1 if html.count("<a") > 10 else 0
    web_traffic = 0
    google_index = 1 if "google" in html.lower() else 0
    statistical = 0

    return np.array([[having_ip, url_length, prefix_suffix, having_subdomain,
                      ssl, request_url, anchor_url, web_traffic,
                      google_index, statistical]], dtype=np.float32)

def infer_model(url: str, html: str):
    global sess
    try:
        if sess is None:
            sess = rt.InferenceSession(str(MODEL_PATH))
        x = extract_features(url, html)
        name = sess.get_inputs()[0].name
        score = float(sess.run(None,{name:x})[0][0][0])
        return score, {"features": x.tolist()}
    except Exception:
        return 0.3, {"fallback": True}
