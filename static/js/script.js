document.getElementById("prediction-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  // Fetch form inputs
  const pregnancies = document.getElementById("pregnancies").value;
  const glucose = document.getElementById("glucose").value;
  const bmi = document.getElementById("bmi").value;
  const age = document.getElementById("age").value;

  // Send data to backend
  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `pregnancies=${pregnancies}&glucose=${glucose}&bmi=${bmi}&age=${age}`,
  });

  // Parse response
  const result = await response.text();
  document.getElementById("result").textContent = result;
  document.getElementById("result-box").style.display = "block";

  // Store inputs and prediction for report generation
  sessionStorage.setItem(
    "report",
    `Pregnancies: ${pregnancies}, Glucose Level: ${glucose}, BMI: ${bmi}, Age: ${age}, Prediction: ${result}`
  );
});

// Generate and download report
document.getElementById("result-box").addEventListener("click", function (event) {
  if (event.target.id === "generate-report") {
    const report = sessionStorage.getItem("report");
    const blob = new Blob([report], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Diabetes_Report.txt";
    link.click();
  }
});
