import React from "react";

const HistoryTable = ({
  filteredHistory,
  downloadReport,
  deleteAnalysis,
}) => {
  return (
    <div className="card">

      <h2>📜 Analysis History</h2>

      <table className="history-table">

        <thead>

          <tr>
            <th>ID</th>
            <th>Filename</th>
            <th>Risk</th>
            <th>Attack Type</th>
            <th>PDF</th>
            <th>Delete</th>
          </tr>

        </thead>

        <tbody>

          {filteredHistory.length === 0 ? (

            <tr>

              <td
                colSpan="6"
                style={{
                  textAlign: "center",
                  padding: "20px",
                }}
              >
                No analysis found.
              </td>

            </tr>

          ) : (

            filteredHistory.map((item) => (

              <tr key={item.id}>

                <td>
                  {item.id}
                </td>

                <td>
                  {item.filename}
                </td>

                <td>

                  <span
                    className={`badge ${
                      item.risk_level
                        ?.toLowerCase() || ""
                    }`}
                  >
                    {item.risk_level}
                  </span>

                </td>

                <td>
                  {item.attack_type}
                </td>

                <td>

                  <button
                    className="download-btn"
                    onClick={() =>
                      downloadReport(item.id)
                    }
                  >
                    📄 PDF
                  </button>

                </td>

                <td>

                  <button
                    className="delete-btn"
                    onClick={() =>
                      deleteAnalysis(item.id)
                    }
                  >
                    🗑 Delete
                  </button>

                </td>

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  );
};

export default HistoryTable;