import React from "react";

const AnalysisCard = ({
  analysis,
  dashboard,
  downloadReport,
}) => {

  return (
    <div className="card">

      <h2>🧠 AI Threat Analysis</h2>

      <p>
        <strong>Risk Level:</strong>{" "}
        <span
          className={`badge ${
            analysis?.risk_level?.toLowerCase() || ""
          }`}
        >
          {analysis?.risk_level || "-"}
        </span>
      </p>

      <p>
        <strong>Attack Type:</strong>{" "}
        {analysis?.attack_type || "-"}
      </p>

      <p>
        <strong>Confidence:</strong>{" "}
        {analysis?.confidence ?? "N/A"}%
      </p>

      <p>
        <strong>Severity Score:</strong>{" "}
        {analysis?.severity_score ?? "N/A"}/100
      </p>

      <p>
        <strong>Summary:</strong>{" "}
        {analysis?.summary || "-"}
      </p>

      <p>
        <strong>Reasoning:</strong>{" "}
        {analysis?.reasoning || "-"}
      </p>

      <button
        style={{ marginBottom: "15px" }}
        onClick={() =>
          navigator.clipboard.writeText(
            analysis?.summary || ""
          )
        }
        disabled={!analysis?.summary}
      >
        📋 Copy Summary
      </button>

      <div>

        <strong>Recommendations:</strong>

        {analysis?.recommendations?.length ? (

          <ul>

            {analysis.recommendations.map(
              (item, index) => (
                <li key={index}>
                  {item}
                </li>
              )
            )}

          </ul>

        ) : (

          <p>-</p>

        )}

      </div>

      <br />

      <div>

        <strong>Next Steps:</strong>

        {analysis?.next_steps?.length ? (

          <ul>

            {analysis.next_steps.map(
              (step, index) => (
                <li key={index}>
                  {step}
                </li>
              )
            )}

          </ul>

        ) : (

          <p>-</p>

        )}

      </div>

      <br />

      {analysis &&
        dashboard?.latest_analysis && (

          <button
            onClick={() =>
              downloadReport(
                dashboard.latest_analysis
              )
            }
          >
            📄 Download PDF Report
          </button>

        )}

    </div>
  );
};

export default AnalysisCard;