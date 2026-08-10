import React from "react";

const DashboardCards = ({ dashboard }) => {
  return (
    <div className="card">

      <h2>Dashboard</h2>

      <div className="stats">

        <div className="box">
          <h3>Total</h3>
          <p>
            {dashboard?.total_analyses ?? 0}
          </p>
        </div>

        <div className="box">
          <h3>Critical</h3>
          <p>
            {dashboard?.critical_risk ?? 0}
          </p>
        </div>

        <div className="box">
          <h3>High</h3>
          <p>
            {dashboard?.high_risk ?? 0}
          </p>
        </div>

        <div className="box">
          <h3>Medium</h3>
          <p>
            {dashboard?.medium_risk ?? 0}
          </p>
        </div>

        <div className="box">
          <h3>Low</h3>
          <p>
            {dashboard?.low_risk ?? 0}
          </p>
        </div>

      </div>

      <br />

      <p>
        <strong>Most Common Attack:</strong>{" "}
        {dashboard?.most_common_attack || "N/A"}
      </p>

    </div>
  );
};

export default DashboardCards;