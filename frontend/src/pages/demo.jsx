import { useState } from "react";
import ScanPanel from "../components/ScanPanel";
import ReportCard from "../components/ReportCard";

export default function Demo() {
  const [result, setResult] = useState(null);

  return (
    <>
      <ScanPanel onSubmit={setResult} />
      {result && <ReportCard data={result} />}
    </>
  );
}
