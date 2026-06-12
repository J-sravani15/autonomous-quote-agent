const API_BASE_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://autonomous-quote-agent.onrender.com";

let quoteCounter = 1;

async function processQuote() {
  const currentLang =
  localStorage.getItem("appLanguage") || "en";

const t = translations[currentLang];

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
    alert(t.fillRequiredFields);
    return;
  }
  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("agent1").innerHTML =
`${t.riskProfilerLabel} : ${t.riskProfilerStatus}`;

document.getElementById("agent2").innerHTML =
`${t.conversionPredictorLabel} : ${t.waitingStatus}`;

document.getElementById("agent3").innerHTML =
`${t.premiumAdvisorLabel} : ${t.waitingStatus}`;

document.getElementById("agent4").innerHTML =
`${t.decisionRouterLabel} : ${t.waitingStatus}`;

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
`${t.riskProfilerLabel} : ${t.riskProfilerStatus}`;

setTimeout(() => {
  document.getElementById("agent1").innerHTML =
  `${t.riskProfilerLabel} : ${t.completeStatus}`;

  document.getElementById("agent2").innerHTML =
  `${t.conversionPredictorLabel} : ${t.conversionPredictorStatus}`;
}, 500);

setTimeout(() => {
  document.getElementById("agent2").innerHTML =
  `${t.conversionPredictorLabel} : ${t.completeStatus}`;

  document.getElementById("agent3").innerHTML =
  `${t.premiumAdvisorLabel} : ${t.advisorStatus}`;
}, 1000);

setTimeout(() => {
  document.getElementById("agent3").innerHTML =
  `${t.premiumAdvisorLabel} : ${t.completeStatus}`;

  document.getElementById("agent4").innerHTML =
  `${t.decisionRouterLabel} : ${t.completeStatus}`;
}, 1500);

    // Display Results

  

let translatedRisk = result.risk_level;

if (result.risk_level === "HIGH")
    translatedRisk = t.riskHigh;
else if (result.risk_level === "MEDIUM")
    translatedRisk = t.riskMedium;
else if (result.risk_level === "LOW")
    translatedRisk = t.riskLow;

document.getElementById("risk").innerHTML =
    translatedRisk;

document.getElementById("probability").innerHTML =
    (result.conversion_probability * 100).toFixed(2) + "%";

document.getElementById("premium").innerHTML =
    "₹ " + result.recommended_premium;

let translatedDecision = result.decision;

if (result.decision === "APPROVE")
    translatedDecision = t.decisionApprove;
else if (result.decision === "REVIEW")
    translatedDecision = t.decisionReview;
else if (result.decision === "REJECT")
    translatedDecision = t.decisionReject;
else if (result.decision === "ESCALATE TO UNDERWRITER")
    translatedDecision = t.decisionEscalate;

document.getElementById("decision").innerHTML =
    translatedDecision;
    document.getElementById("probability").innerHTML =
      (result.conversion_probability * 100).toFixed(2) + "%";

    document.getElementById("premium").innerHTML =
      "₹ " + result.recommended_premium;

    

    // Add to History Table

    addHistory(result);

  } catch (error) {
    document.getElementById("loader").classList.add("hidden");

    console.error(error);

    alert(t.analysisError);

    document.getElementById("agent1").innerHTML =
  `❌ ${t.failed}`;

document.getElementById("agent2").innerHTML =
  `❌ ${t.failed}`;

document.getElementById("agent3").innerHTML =
  `❌ ${t.failed}`;

document.getElementById("agent4").innerHTML =
  `❌ ${t.failed}`;
  }
}

function addHistory(result) {

  const currentLang =
    localStorage.getItem("appLanguage") || "en";

  const t = translations[currentLang];

  let translatedRisk = result.risk_level;

  if (result.risk_level === "HIGH")
      translatedRisk = t.riskHigh;
  else if (result.risk_level === "MEDIUM")
      translatedRisk = t.riskMedium;
  else if (result.risk_level === "LOW")
      translatedRisk = t.riskLow;

  let translatedDecision = result.decision;

  if (result.decision === "APPROVE")
      translatedDecision = t.decisionApprove;
  else if (result.decision === "REVIEW")
      translatedDecision = t.decisionReview;
  else if (result.decision === "REJECT")
      translatedDecision = t.decisionReject;
  else if (result.decision === "ESCALATE TO UNDERWRITER")
      translatedDecision = t.decisionEscalate;

  const row = document.createElement("tr");

  row.className = "border-b border-slate-700";

  row.innerHTML = `
  
    <td class="py-2">${quoteCounter++}</td>
    <td class="py-2">${translatedRisk}</td>
    <td class="py-2">${(result.conversion_probability * 100).toFixed(1)}%</td>
    <td class="py-2">${translatedDecision}</td>
  `;

  document
    .getElementById("historyTable")
    .prepend(row);
}