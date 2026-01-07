from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.core.heuristics import analyze_heuristics
from app.core.signatures import run_yara, run_clam_like
from app.core.ml_infer import infer_model
import requests
from bs4 import BeautifulSoup

router = APIRouter()

class ScanRequest(BaseModel):
    url: Optional[str] = None
    html: Optional[str] = None
    js: Optional[str] = None


@router.post("")
async def scan_page(payload: ScanRequest):

    url = payload.url or ""
    html = payload.html
    js = payload.js

    if url and not html:
        try:
            resp = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            html = soup.prettify()
            js = "\n".join([s.string or "" for s in soup.find_all("script")])
        except Exception:
            html = ""
            js = ""

    heuristics_report = analyze_heuristics(url=url, html=html or "", js=js or "")

    yara_matches = run_yara((html or "") + (js or ""))
    clam_matches = run_clam_like((html or "") + (js or ""))

    ml_score, ml_explain = infer_model(url=url, html=html or "")

    sig_score = 1.0 if (yara_matches or clam_matches) else 0.0
    heur_score = heuristics_report.get("suspicion_score", 0)

    final_score = round(
        (0.50 * heur_score) +
        (0.30 * sig_score) +
        (0.20 * ml_score),
        2
    )


    result = {
        "url": url,
        "final_score": final_score,
        "reasons": {
            "heuristics": heuristics_report.get("reasons"),
            "yara": yara_matches,
            "clam": clam_matches,
            "ml": ml_explain
        }
    }

    return result
