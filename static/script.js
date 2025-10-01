document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("productForm");
  const scoreDisplay = document.getElementById("score");
  const ratingDisplay = document.getElementById("rating");
  const suggestionsList = document.getElementById("suggestions");
  const historyList = document.getElementById("historyList");

  let barChart, pieChart;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = {
      product_name: form.product_name.value,
      materials: form.materials.value.split(",").map(m => m.trim()),
      weight_grams: parseFloat(form.weight_grams.value),
      transport: form.transport.value,
      packaging: form.packaging.value,
      gwp: parseFloat(form.gwp.value),
      cost: parseFloat(form.cost.value),
      circularity: parseFloat(form.circularity.value),
      weight_gwp: parseFloat(form.weight_gwp.value),
      weight_cost: parseFloat(form.weight_cost.value),
      weight_circularity: parseFloat(form.weight_circularity.value)
    };

    try {
      const res = await fetch("/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await res.json();

      if (res.ok) {
        // Display score and rating
        scoreDisplay.textContent = `Score: ${data.sustainability_score}`;
        ratingDisplay.textContent = `Rating: ${data.rating}`;

        // Show suggestions
        suggestionsList.innerHTML = "";
        data.suggestions.forEach(suggestion => {
          const li = document.createElement("li");
          li.textContent = suggestion;
          suggestionsList.appendChild(li);
        });

        // Update charts and history
        await updateSummary();
        await updateHistory();
      } else {
        alert(data.error || "Error submitting product.");
      }
    } catch (err) {
      console.error("Submit failed:", err);
      alert("Error submitting product.");
    }
  });

  async function updateSummary() {
    try {
      const res = await fetch("/score-summary");
      const data = await res.json();
      if (data.message) return;

      const ctxBar = document.getElementById("barChart").getContext("2d");
      const ctxPie = document.getElementById("pieChart").getContext("2d");

      // Destroy previous charts if they exist
      if (barChart) barChart.destroy();
      if (pieChart) pieChart.destroy();

      // Bar Chart: Rating summary
      barChart = new Chart(ctxBar, {
        type: "bar",
        data: {
          labels: Object.keys(data.ratings),
          datasets: [{
            label: "Rating Count",
            data: Object.values(data.ratings),
            backgroundColor: "rgba(75, 192, 192, 0.6)"
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

      // Pie Chart: Top sustainability issues with real counts
      const labels = data.issue_labels || [];
      const values = data.issue_counts || [];

      const backgroundColors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#F77825", "#8E44AD", "#2ECC71", "#E67E22", "#34495E"
      ];

      pieChart = new Chart(ctxPie, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: backgroundColors.slice(0, labels.length)
          }]
        },
        options: {
          responsive: true
        }
      });
    } catch (err) {
      console.error("Error loading summary:", err);
    }
  }

  async function updateHistory() {
    try {
      const res = await fetch("/history");
      const data = await res.json();

      historyList.innerHTML = "";
      data.slice().reverse().forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.product_name}: ${item.score} (${item.rating})`;
        historyList.appendChild(li);
      });
    } catch (err) {
      console.error("Error loading history:", err);
    }
  }

  // Initial load
  updateSummary();
  updateHistory();
});
