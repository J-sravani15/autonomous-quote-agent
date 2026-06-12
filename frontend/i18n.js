// i18n - Internationalization (i18n) Management System
// Handles language switching, translation lookup, and persistence

let currentLanguage = 'en'; // Default language

/**
 * Initialize the language system on page load
 * Reads saved language from localStorage or uses default
 */
function initializeLanguage() {
  // Check if language is saved in localStorage
  const savedLanguage = localStorage.getItem('appLanguage');
  
  if (savedLanguage && translations[savedLanguage]) {
    currentLanguage = savedLanguage;
  } else {
    currentLanguage = 'en'; // Default to English
    localStorage.setItem('appLanguage', currentLanguage);
  }
  
  // Set the dropdown to the current language
  const langSelect = document.getElementById('lang');
  if (langSelect) {
    langSelect.value = currentLanguage;
  }
  
  // Apply translations to the page
  updatePageTranslations();
}

/**
 * Get translation text for a given key
 * @param {string} key - Translation key
 * @returns {string} Translated text or key if not found
 */
function t(key) {
  if (translations[currentLanguage] && translations[currentLanguage][key]) {
    return translations[currentLanguage][key];
  }
  
  // Fallback to English if translation not found
  if (translations['en'] && translations['en'][key]) {
    return translations['en'][key];
  }
  
  // Return the key itself if no translation found
  return key;
}

/**
 * Change the current language and update the page
 * @param {string} language - Language code (en, te, hi, ta)
 */
function changeLanguage(language) {
  // Validate language code
  if (!translations[language]) {
    console.error(`Language ${language} not supported`);
    return;
  }
  
  currentLanguage = language;
  
  // Save to localStorage for persistence
  localStorage.setItem('appLanguage', language);
  
  // Update the language selector dropdown
  const langSelect = document.getElementById('lang');
  if (langSelect) {
    langSelect.value = language;
  }
  
  // Update all page translations
  updatePageTranslations();
}

/**
 * Update all page elements with current language translations
 * Handles both data-i18n attributes and direct element updates
 */
function updatePageTranslations() {
  // Update all elements with data-i18n attribute
  const elements = document.querySelectorAll('[data-i18n]');
  
  elements.forEach((element) => {
    const key = element.getAttribute('data-i18n');
    const translatedText = t(key);
    
    // Update the text content
    if (element.tagName === 'OPTION' || element.tagName === 'INPUT' || element.tagName === 'SELECT') {
      // For form elements, update placeholder or value
      if (element.getAttribute('placeholder')) {
        element.setAttribute('placeholder', translatedText);
      } else if (element.tagName === 'OPTION') {
        element.textContent = translatedText;
      }
    } else {
      // For regular elements, update text content
      element.textContent = translatedText;
    }
  });
  
  // Update specific elements by ID that need translation
  updateElementById('Driver_Age', 'driverAge');
  updateElementById('Driving_Exp', 'drivingExperience');
  updateElementById('Prev_Accidents', 'previousAccidents');
  updateElementById('Prev_Citations', 'trafficViolations');
  updateElementById('Annual_Miles_Range', 'annualMiles');
  updateElementById('Quoted_Premium', 'currentPremium');
  updateElementById('Veh_Usage', 'vehicleUsage');
  updateElementById('Coverage', 'coverageLevel');
  updateElementById('Vehicle_Cost_Range', 'vehicleCostRange');
  updateElementById('Sal_Range', 'salaryRange');
  
  // Update select option labels
  updateSelectOptions();
  
  // Update page title
  updatePageTitle();
  
  // Trigger custom event for other components to react
  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: currentLanguage } }));
}

/**
 * Update placeholder for a form element by ID
 * @param {string} elementId - Element ID
 * @param {string} translationKey - Translation key
 */
function updateElementById(elementId, translationKey) {
  const element = document.getElementById(elementId);
  if (element) {
    const translatedText = t(translationKey);
    if (element.tagName === 'INPUT' || element.tagName === 'SELECT') {
      element.setAttribute('placeholder', translatedText);
    }
  }
}

/**
 * Update select option labels based on current language
 */
function updateSelectOptions() {
  // Vehicle Usage Options
  const vehicleUsageSelect = document.getElementById('Veh_Usage');
  if (vehicleUsageSelect) {
    const options = vehicleUsageSelect.querySelectorAll('option');
    if (options.length > 0) {
      options[0].textContent = t('vehicleUsage');
      options[1].textContent = t('personalUsage');
      options[2].textContent = t('businessUsage');
      options[3].textContent = t('commercialUsage');
    }
  }
  
  // Coverage Level Options
  const coverageSelect = document.getElementById('Coverage');
  if (coverageSelect) {
    const options = coverageSelect.querySelectorAll('option');
    if (options.length > 0) {
      options[0].textContent = t('coverageLevel');
      options[1].textContent = t('basicCoverage');
      options[2].textContent = t('standardCoverage');
      options[3].textContent = t('premiumCoverage');
    }
  }
  
  // Vehicle Cost Range Options
  const vehicleCostSelect = document.getElementById('Vehicle_Cost_Range');
  if (vehicleCostSelect) {
    const options = vehicleCostSelect.querySelectorAll('option');
    if (options.length > 0) {
      options[0].textContent = t('vehicleCostRange');
      options[1].textContent = t('below5Lakh');
      options[2].textContent = t('range5to10Lakh');
      options[3].textContent = t('range10to20Lakh');
      options[4].textContent = t('above20Lakh');
    }
  }
  
  // Salary Range Options
  const salarySelect = document.getElementById('Sal_Range');
  if (salarySelect) {
    const options = salarySelect.querySelectorAll('option');
    if (options.length > 0) {
      options[0].textContent = t('salaryRange');
      options[1].textContent = t('below3Lakh');
      options[2].textContent = t('range3to6Lakh');
      options[3].textContent = t('range6to12Lakh');
      options[4].textContent = t('above12Lakh');
    }
  }
}

/**
 * Update page title based on current language
 */
function updatePageTitle() {
  const pageTitle = document.querySelector('title');
  if (pageTitle) {
    pageTitle.textContent = t('selectLanguage') + ' | Autonomous Quote Agent';
  }
}

// Initialize language when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initializeLanguage();
});
window.addEventListener('languageChanged', function () {

    // Clear result cards
    const risk = document.getElementById('risk');
    const probability = document.getElementById('probability');
    const premium = document.getElementById('premium');
    const decision = document.getElementById('decision');

    if (risk) risk.innerHTML = '-';
    if (probability) probability.innerHTML = '-';
    if (premium) premium.innerHTML = '-';
    if (decision) decision.innerHTML = '-';

    // Clear history table
    const historyTable = document.getElementById('historyTable');
    if (historyTable) {
        historyTable.innerHTML = '';
    }

    // Reset pipeline
    const tObj = translations[currentLanguage];

    const agent1 = document.getElementById('agent1');
    const agent2 = document.getElementById('agent2');
    const agent3 = document.getElementById('agent3');
    const agent4 = document.getElementById('agent4');

    if (agent1)
        agent1.innerHTML = `${tObj.riskProfilerLabel} : ${tObj.waitingStatus}`;

    if (agent2)
        agent2.innerHTML = `${tObj.conversionPredictorLabel} : ${tObj.waitingStatus}`;

    if (agent3)
        agent3.innerHTML = `${tObj.premiumAdvisorLabel} : ${tObj.waitingStatus}`;

    if (agent4)
        agent4.innerHTML = `${tObj.decisionRouterLabel} : ${tObj.waitingStatus}`;
});