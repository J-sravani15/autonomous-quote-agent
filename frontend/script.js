let quoteCounter = 1;

async function processQuote() {

  const requestData = {
    Driver_Age: parseInt(document.getElementById("Driver_Age").value) || 0,

    Driving_Exp:
      parseInt(document.getElementById("Driving_Exp").value) || 0,

    Prev_Accidents:
      parseInt(document.getElementById("Prev_Accidents").value) || 0,

    Prev_Citations:
      parseInt(document.getElementById("Prev_Citations").value) || 0,

    Coverage:
      parseInt(document.getElementById("Coverage").value) || 0,

    Veh_Usage:
      parseInt(document.getElementById("Veh_Usage").value) || 0,

    Annual_Miles_Range:
      parseInt(document.getElementById("Annual_Miles_Range").value) || 0,

    Vehicl_Cost_Range:
      parseInt(document.getElementById("Vehicle_Cost_Range").value) || 0,

    Sal_Range:
      parseInt(document.getElementById("Sal_Range").value) || 0,

    Quoted_Premium:
      parseFloat(document.getElementById("Quoted_Premium").value) || 0,
  };

  // Basic Validation

  if (
    requestData.Driver_Age === 0 ||
    requestData.Driving_Exp === 0 ||
    requestData.Quoted_Premium === 0
  ) {
    alert(
      "Please fill Driver Age, Driving Experience and Quoted Premium."
    );
    return;
  }
  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("agent1").innerHTML =
    "🟡 Risk Profiler Running...";

  document.getElementById("agent2").innerHTML =
    "⏳ Waiting";

  document.getElementById("agent3").innerHTML =
    "⏳ Waiting";

  document.getElementById("agent4").innerHTML =
    "⏳ Waiting";

  try {

    const response = await fetch("https://autonomous-quote-agent.onrender.com/predict", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(requestData),
      }
    );

    if (!response.ok) {
      throw new Error("API Error");
    }

    const result = await response.json();
    document.getElementById("loader").classList.add("hidden");

    // Update Agent Status

    document.getElementById("agent1").innerHTML =
"🟡 Risk Profiler Running...";

setTimeout(() => {
  document.getElementById("agent1").innerHTML =
  "✅ Risk Profiler Completed";

  document.getElementById("agent2").innerHTML =
  "🟡 Conversion Predictor Running...";
}, 500);

setTimeout(() => {
  document.getElementById("agent2").innerHTML =
  "✅ Conversion Predictor Completed";

  document.getElementById("agent3").innerHTML =
  "🟡 Premium Advisor Running...";
}, 1000);

setTimeout(() => {
  document.getElementById("agent3").innerHTML =
  "✅ Premium Advisor Completed";

  document.getElementById("agent4").innerHTML =
  "✅ Decision Router completed...";
}, 1500);

    // Display Results

    document.getElementById("risk").innerHTML =
      result.risk_level;

    document.getElementById("probability").innerHTML =
      (result.conversion_probability * 100).toFixed(2) + "%";

    document.getElementById("premium").innerHTML =
      "₹ " + result.recommended_premium;

    document.getElementById("decision").innerHTML =
      result.decision;

    // Add to History Table

    addHistory(result);

  } catch (error) {
    document.getElementById("loader").classList.add("hidden");

    console.error(error);

    alert(
      "Unable to connect to backend. Make sure FastAPI server is running."
    );

    document.getElementById("agent1").innerHTML =
      "❌ Failed";

    document.getElementById("agent2").innerHTML =
      "❌ Failed";

    document.getElementById("agent3").innerHTML =
      "❌ Failed";

    document.getElementById("agent4").innerHTML =
      "❌ Failed";
  }
}

function addHistory(result) {

  const row = document.createElement("tr");

  row.className = "border-b border-slate-700";

  row.innerHTML = `
    <td class="py-2">${quoteCounter++}</td>
    <td class="py-2">${result.risk_level}</td>
    <td class="py-2">${(result.conversion_probability * 100).toFixed(1)}%</td>
    <td class="py-2">${result.decision}</td>
  `;

  document
    .getElementById("historyTable")
    .prepend(row);
}