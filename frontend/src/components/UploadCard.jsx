import React from "react";

const UploadCard = ({
  setFile,
  analyzeLog,
  loading,
}) => {
  return (
    <div className="card">

      <h2>Upload Security Log</h2>

      <input
        type="file"
        accept=".txt,.log,.csv"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] || null
          )
        }
      />

      <button
        onClick={analyzeLog}
        disabled={loading}
      >
        {loading
          ? "Analyzing..."
          : "Analyze Log"}
      </button>

    </div>
  );
};

export default UploadCard;