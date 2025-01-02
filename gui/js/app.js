document.getElementById("search-button").addEventListener("click", () => {
  const keyword = document.getElementById("keyword").value.toLowerCase();
  const periodSelect = document.getElementById("period");
  const period = periodSelect.options[periodSelect.selectedIndex].value.trim();  // Ensure no extra spaces
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  const payload = {
    keyword: keyword,
    period: period,  // Send the period value directly
    startDate: startDate,
    endDate: endDate,
  };

  fetch("http://127.0.0.1:5000/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      displayResults(data.results);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

// Function to display results
function displayResults(results) {
  const resultsTable = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  resultsTable.innerHTML = ""; // Clear previous results

  if (!results || results.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 5;
    td.textContent = "No results found.";
    tr.appendChild(td);
    resultsTable.appendChild(tr);
    return;
  }

  results.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.date}</td>
      <td>${item.period}</td>
      <td>${item.party}</td>
      <td>${item.speech}</td>
    `;
    resultsTable.appendChild(tr);
  });
}
