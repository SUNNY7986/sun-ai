import React from "react";

const SearchFilter = ({
  search,
  setSearch,
  riskFilter,
  setRiskFilter,
}) => {
  return (
    <div className="card">

      <h2>🔍 Search & Filter</h2>

      <div className="search-filter">

        <input
          type="text"
          placeholder="Search by filename..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          className="search-box"
        />

        <select
          value={riskFilter}
          onChange={(e) =>
            setRiskFilter(e.target.value)
          }
          className="filter-box"
        >

          <option value="All">
            All Risks
          </option>

          <option value="Critical">
            Critical
          </option>

          <option value="High">
            High
          </option>

          <option value="Medium">
            Medium
          </option>

          <option value="Low">
            Low
          </option>

        </select>

      </div>

    </div>
  );
};

export default SearchFilter;