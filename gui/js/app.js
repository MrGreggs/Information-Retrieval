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

function displayResults(results) {
  const resultsTable = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  resultsTable.innerHTML = ""; // Clear previous results

  if (!results || results.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 5; // Adjust for your table's number of columns
    td.textContent = "No results found.";
    tr.appendChild(td);
    resultsTable.appendChild(tr);
    return;
  }

  results.forEach((item) => {
    const tr = document.createElement("tr");
    let speechContent = item.speech;
    const isTruncated = speechContent.length > 50;
    const speechPreview = isTruncated ? speechContent.substring(0, 50) + "..." : speechContent;
    const showMoreButton = isTruncated
      ? `<button class="show-more" data-speech="${speechContent}" data-truncated="${isTruncated}">Show More</button>`
      : "";
    const showLessButton = !isTruncated ? "" : `<button class="show-less" style="display:none;">Show Less</button>`;

    tr.innerHTML = `
      <td>${item.member_name}</td>
      <td>${item.sitting_date}</td>
      <td>${item.parliamentary_period}</td>
      <td>${item.political_party}</td>
      <td>
        <p class="speech-preview">${speechPreview}</p>
        ${showMoreButton}
        ${showLessButton}
      </td>
    `;
    resultsTable.appendChild(tr);
  });

  // Add event listeners for "Show More" buttons
  document.querySelectorAll(".show-more").forEach(button => {
    button.addEventListener("click", (e) => {
      const fullSpeech = e.target.dataset.speech;
      e.target.parentElement.querySelector(".speech-preview").textContent = fullSpeech;
      e.target.style.display = "none";  // Hide "Show More" button
      e.target.parentElement.querySelector(".show-less").style.display = "inline-block";  // Show "Show Less" button
    });
  });

  // Add event listeners for "Show Less" buttons
  document.querySelectorAll(".show-less").forEach(button => {
    button.addEventListener("click", (e) => {
      const truncatedSpeech = e.target.previousElementSibling.dataset.speech.substring(0, 50) + "...";
      e.target.parentElement.querySelector(".speech-preview").textContent = truncatedSpeech;
      e.target.style.display = "none";  // Hide "Show Less" button
      e.target.parentElement.querySelector(".show-more").style.display = "inline-block";  // Show "Show More" button
    });
  });
}
