document.getElementById("search-button").addEventListener("click", () => {
  const keyword = document.getElementById("keyword").value.toLowerCase();
  const period = document.getElementById("period").value;
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  // Construct the request payload
  const payload = {
    keyword: keyword,
    period: period,
    startDate: startDate,
    endDate: endDate,
  };

  // Log the payload to ensure it's correct
  console.log("Request payload:", payload);

  // Make the POST request
  fetch("http://127.0.0.1:5000/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Debugging: Ensure you receive the expected data
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
