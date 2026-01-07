import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ScanPanel({ onSubmit }) {
  const [url, setUrl] = useState("");
  const [html, setHtml] = useState("");
  const [js, setJs] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
  console.log("Sending request...");
  console.log({ url, html, js });

  const res = await fetch("http://localhost:8000/api/scan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, html, js })
  });

  console.log("Response status:", res.status);

  const data = await res.json();
  console.log("Response data:", data);

  onSubmit(data);
};


  return (
    <div className="card">
      <h2 style={{ margin: 0 }}>Input</h2>

      {/* URL FIELD */}
      <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
        <label style={{ marginBottom: "4px" }}>URL</label>
        <input
          style={{
            width: "100%",
            padding: "10px",
            fontSize: "15px",
            borderRadius: "6px",
            border: "1px solid #ccc"
          }}
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      </div>

      {/* HTML FIELD */}
      <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
        <label style={{ marginBottom: "4px" }}>HTML</label>
        <textarea
          rows={6}
          style={{
            width: "100%",
            padding: "10px",
            fontSize: "15px",
            borderRadius: "6px",
            border: "1px solid #ccc"
          }}
          placeholder="<html>...</html>"
          value={html}
          onChange={(e) => setHtml(e.target.value)}
        />
      </div>

      {/* JS FIELD */}
      <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
        <label style={{ marginBottom: "4px" }}>JavaScript</label>
        <textarea
          rows={4}
          style={{
            width: "100%",
            padding: "10px",
            fontSize: "15px",
            borderRadius: "6px",
            border: "1px solid #ccc"
          }}
          placeholder="console.log('script')"
          value={js}
          onChange={(e) => setJs(e.target.value)}
        />
      </div>

      <button
      style={{
        background: "black",
        color: "white",
        padding: "12px",
        fontSize: "15px",
        borderRadius: "6px",
        cursor: "pointer",
        border: "none",
        marginTop: "10px",
        width: "150px"
      }}
      onClick={handleRun}
      >
        {loading ? "Analyzing..." : "Run Analysis"}
      </button>

    </div>
  );
}






