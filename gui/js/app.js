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

  fetch("http://127.0.0.1:5000/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  .then(response => response.json())
  .then(data => {
    console.log(data); // Debugging purposes
    displayResults(data.results);
  })
  .catch(error => console.error("Error:", error));
});

function displayResults(results) {
  const resultsDiv = document.getElementById("results");
  if (!resultsDiv) {
    console.error("Results div not found!");
    return;
  }

  resultsDiv.innerHTML = ""; // Clear previous results

  if (results.length === 0) {
    resultsDiv.textContent = "No results found.";
    return;
  }

  results.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.date}</td>
      <td>${item.parliamentaryPeriod}</td>
      <td>${item.politicalParty}</td>
      <td>${item.speech}</td>
    `;
    resultsDiv.appendChild(tr);
  });
}

// Fetch data and handle results
document.getElementById("search-button").addEventListener("click", () => {
  const keyword = document.getElementById("keyword").value.toLowerCase();

  fetch("http://127.0.0.1:5000/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ keyword: keyword }),
  })
  .then(response => response.json())
  .then(data => {
    displayResults(data.results); // Call the function to display results
  })
  .catch(error => console.error("Error:", error));
});
