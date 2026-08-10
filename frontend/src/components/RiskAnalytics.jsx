import React from "react";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Bar,
} from "recharts";


const RiskAnalytics = ({
  pieData,
  barData,
  COLORS,
}) => {

  return (
    <div className="card">

      <h2>📊 Risk Analytics</h2>

      <div
        style={{
          width: "100%",
          height: 350,
        }}
      >

        <ResponsiveContainer>

          <PieChart>

            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              outerRadius={120}
              label
            >

              {pieData.map(
                (entry, index) => (

                  <Cell
                    key={`cell-${index}`}
                    fill={
                      COLORS[index % COLORS.length]
                    }
                  />

                )
              )}

            </Pie>

            <Tooltip />

            <Legend />

          </PieChart>

        </ResponsiveContainer>

      </div>


      <div
        style={{
          width: "100%",
          height: 350,
          marginTop: 30,
        }}
      >

        <ResponsiveContainer>

          <BarChart
            data={barData}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="risk"
            />

            <YAxis />

            <Tooltip />

            <Legend />

            <Bar
              dataKey="count"
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
};

export default RiskAnalytics;