const API_BASE_URL = "https://autonomous-quote-agent.onrender.com";

let quoteCounter = 1;
let lastResult = null; // Store last result for explanation

// Tab switching function
function switchTab(tabName) {
  // Hide all tabs
  const tabs = document.querySelectorAll('.tab-content');
  tabs.forEach(tab => tab.classList.add('hidden'));
  
  // Remove active state from all buttons
  const buttons = document.querySelectorAll('.tab-btn');
  buttons.forEach(btn => {
    btn.classList.remove('bg-blue-600');
    btn.classList.add('bg-slate-700');
  });
  
  // Show selected tab
  document.getElementById(tabName + '-tab').classList.remove('hidden');
  
  // Set active button
  document.getElementById('tab-' + tabName).classList.remove('bg-slate-700');
  document.getElementById('tab-' + tabName).classList.add('bg-blue-600');
}

async function generateExplanation() {
  if (!lastResult) {
    alert('Please analyze a quote first');
    return;
  }

  const currentLang = localStorage.getItem("appLanguage") || "en";
  const t = translations[currentLang];

  document.getElementById('explainBtn').disabled = true;
  document.getElementById('explainBtn').innerHTML = '<span data-i18n="generating">Generating...</span>';

  try {
    const response = await fetch(API_BASE_URL + "/explain", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Driver_Age: parseInt(document.getElementById("Driver_Age").value) || 0,
        Driving_Exp: parseInt(document.getElementById("Driving_Exp").value) || 0,
        Prev_Accidents: parseInt(document.getElementById("Prev_Accidents").value) || 0,
        Prev_Citations: parseInt(document.getElementById("Prev_Citations").value) || 0,
        Coverage: parseInt(document.getElementById("Coverage").value) || 0,
        Veh_Usage: parseInt(document.getElementById("Veh_Usage").value) || 0,
        Annual_Miles_Range: parseInt(document.getElementById("Annual_Miles_Range").value) || 0,
        Vehicl_Cost_Range: parseInt(document.getElementById("Vehicl_Cost_Range").value) || 0,
        Sal_Range: parseInt(document.getElementById("Sal_Range").value) || 0,
        Quoted_Premium: parseFloat(document.getElementById("Quoted_Premium").value) || 0,
        risk_level: lastResult.risk_level,
        prediction: lastResult.prediction,
        conversion_probability: lastResult.conversion_probability,
        recommended_premium: lastResult.recommended_premium,
        decision: lastResult.decision
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', errorText);
      throw new Error(`API Error: ${response.status}`);
    }

    const data = await response.json();
    if (data.explanation) {
      document.getElementById('explanationContent').innerHTML = `<p class="text-gray-300">${data.explanation}</p>`;
    } else {
      throw new Error("No explanation in response");
    }
  } catch (error) {
    console.error("Explanation Error:", error);
    document.getElementById('explanationContent').innerHTML = `
      <div class="bg-yellow-900 border border-yellow-700 p-4 rounded">
        <p class="text-yellow-300 font-bold mb-2">⚠️ Explanation Not Available</p>
        <p class="text-yellow-200 text-sm mb-3">${error.message}</p>
        <p class="text-yellow-200 text-sm mb-2"><strong>Possible reasons:</strong></p>
        <ul class="text-yellow-200 text-sm list-disc list-inside space-y-1">
          <li>Ollama is not running. Start it with: <code class="bg-slate-800 px-2 py-1 rounded">ollama serve</code></li>
          <li>Ollama model not available. Install with: <code class="bg-slate-800 px-2 py-1 rounded">ollama pull llama3</code></li>
          <li>Backend cannot connect to Ollama</li>
        </ul>
        <p class="text-yellow-200 text-sm mt-3">The Decision Analysis tab still works without Ollama!</p>
      </div>
    `;
  } finally {
    document.getElementById('explainBtn').disabled = false;
    document.getElementById('explainBtn').innerHTML = '<span data-i18n="generateExplanation">Generate AI Explanation</span>';
  }
}

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
      parseInt(document.getElementById("Vehicl_Cost_Range").value) || 0,

    Sal_Range:
      parseInt(document.getElementById("Sal_Range").value) || 0,

    Quoted_Premium:
      parseFloat(document.getElementById("Quoted_Premium").value) || 0,
  };

  // Basic Validation

  if (
    requestData.Driver_Age === "" ||
    requestData.Driving_Exp === "" ||
    requestData.Quoted_Premium === ""
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

    const response = await fetch(API_BASE_URL + "/predict", {
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
    lastResult = result; // Store for explanation
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
else if (result.decision === "AUTO APPROVE")
    translatedDecision = "✓ Auto Approve";
else if (result.decision === "AGENT FOLLOW-UP")
    translatedDecision = "→ Agent Follow-up";

document.getElementById("decision").innerHTML =
    translatedDecision;
    document.getElementById("probability").innerHTML =
      (result.conversion_probability * 100).toFixed(2) + "%";

    document.getElementById("premium").innerHTML =
      "₹ " + result.recommended_premium;

    // Display Decision Analysis (v2.0)
    if (result.analysis) {
      const analysis = result.analysis;
      
      // Confidence Score
      document.getElementById("confidenceScore").innerHTML = 
        (analysis.confidence_score * 100).toFixed(1) + "%";
      document.getElementById("confidenceLevel").innerHTML = 
        analysis.confidence_level;
      document.getElementById("confidenceBar").style.width = 
        (analysis.confidence_score * 100) + "%";
      
      // Color code confidence bar
      if (analysis.confidence_score >= 0.85) {
        document.getElementById("confidenceBar").className = "bg-green-500 h-full transition-all duration-300";
      } else if (analysis.confidence_score >= 0.70) {
        document.getElementById("confidenceBar").className = "bg-yellow-500 h-full transition-all duration-300";
      } else {
        document.getElementById("confidenceBar").className = "bg-orange-500 h-full transition-all duration-300";
      }
      
      // Risk Factors
      if (analysis.risk_factors && analysis.risk_factors.length > 0) {
        document.getElementById("riskFactors").innerHTML = 
          analysis.risk_factors.map(factor => `<div class="flex items-start gap-2"><span class="text-yellow-400">•</span><span>${factor}</span></div>`).join("");
      } else {
        document.getElementById("riskFactors").innerHTML = '<p class="text-gray-400">No significant risk factors identified</p>';
      }
      
      // Reasoning
      document.getElementById("reasoning").innerHTML = analysis.reasoning;
      
      // Premium Adjustment
      document.getElementById("premiumAdjustment").innerHTML = analysis.premium_adjustment_reason;
      
      // Recommended Action
      document.getElementById("recommendedAction").innerHTML = analysis.recommended_action;
      
      // Override Alert
      if (analysis.override_triggered) {
        document.getElementById("overrideAlert").classList.remove("hidden");
        document.getElementById("overrideReason").innerHTML = analysis.override_reason;
      } else {
        document.getElementById("overrideAlert").classList.add("hidden");
      }
    }

    // Add to History Table

    addHistory(result);
    
    // Switch to results tab
    switchTab('results');

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
  else if (result.decision === "AUTO APPROVE")
      translatedDecision = "✓ Auto Approve";
  else if (result.decision === "AGENT FOLLOW-UP")
      translatedDecision = "→ Agent Follow-up";

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
