export default function ReportCard({ data }) {
  if (!data) return null;

  const score = data.final_score;

  const verdict =
    score > 0.6 ? "PHISHING" :
    score > 0.35 ? "SUSPICIOUS" :
    "SAFE";

  const color =
    verdict === "PHISHING" ? "#e53935" :
    verdict === "SUSPICIOUS" ? "#fb8c00" :
    "#43a047";

  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #ddd",
        borderRadius: "10px",
        padding: "20px",
        marginTop: "20px"
      }}
    >
      <h2>Scan Report</h2>

      <p><b>URL:</b> {data.url}</p>

      <p>
        <b>Risk Score:</b>{" "}
        <span style={{ fontWeight: "bold" }}>{score.toFixed(2)}</span>
      </p>

      <p>
        <b>Verdict:</b>{" "}
        <span style={{ color, fontWeight: "bold" }}>{verdict}</span>
      </p>

      <h4>Detection Evidence</h4>

      <ul>
        {data.reasons.heuristics?.map((r, i) => (
          <li key={i}>Heuristic: {r}</li>
        ))}
        {data.reasons.yara?.map((r, i) => (
          <li key={i}>Signature(YARA): {r}</li>
        ))}
        {data.reasons.clam?.map((r, i) => (
          <li key={i}>Signature(Clam): {r}</li>
        ))}
      </ul>

      <details style={{ marginTop: "10px" }}>
        <summary>ML Explanation</summary>
        <pre style={{ background: "#f7f7f7", padding: "10px" }}>
          {JSON.stringify(data.reasons.ml, null, 2)}
        </pre>
      </details>
    </div>
  );
}
