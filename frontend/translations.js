// Comprehensive translations for Autonomous Quote Agent
// Supports: English (en), Telugu (te), Hindi (hi), Tamil (ta)

const translations = {
  en: {

    // Language selector
    selectLanguage: "SELECT LANGUAGE",

    appTitle: "Autonomous Quote Agent",
subtitle: "AI-powered underwriting, conversion prediction and local Ollama explanations.",
language: "Language",
    
    // Driver Information Section
    driverInformation: "Driver Information",
    driverAge: "Driver Age",
    drivingExperience: "Driving Experience",
    previousAccidents: "Previous Accidents",
    trafficViolations: "Traffic Violations Count",
    
    // Vehicle Information Section
    vehicleInformation: "Vehicle Information",
    vehicleUsage: "Vehicle Usage",
    personalUsage: "Personal",
    businessUsage: "Business",
    commercialUsage: "Commercial",
    coverageLevel: "Coverage Level",
    basicCoverage: "Basic",
    standardCoverage: "Standard",
    premiumCoverage: "Premium",
    annualMiles: "Annual Miles",
    vehicleCostRange: "Vehicle Cost Range",
    below5Lakh: "Below ₹5 Lakh",
    range5to10Lakh: "₹5 - ₹10 Lakh",
    range10to20Lakh: "₹10 - ₹20 Lakh",
    above20Lakh: "Above ₹20 Lakh",
    
    // Financial Information Section
    financialInformation: "Financial Information",
    salaryRange: "Salary Range",
    below3Lakh: "Below ₹3 Lakh",
    range3to6Lakh: "₹3 - ₹6 Lakh",
    range6to12Lakh: "₹6 - ₹12 Lakh",
    above12Lakh: "Above ₹12 Lakh",
    currentPremium: "Current Insurance Premium (₹/year)",
    
    // Quote Analysis Section
    quoteAnalysis: "Quote Analysis",
    analysisDescription: "Click the button below to run the autonomous agent pipeline.",
    analyzeQuote: "Analyze Quote",
    
    // Agent Pipeline Section
    agentPipeline: "Agent Pipeline",
    riskProfilerLabel: "Risk Profiler",
    conversionPredictorLabel: "Conversion Predictor",
    premiumAdvisorLabel: "Premium Advisor",
    decisionRouterLabel: "Decision Router",
    
    // Agent Status Messages
    waitingStatus: "Waiting",
    riskProfilerStatus: "Analyzing Risk Profile",
    conversionPredictorStatus: "Predicting Conversion",
    advisorStatus: "Optimizing Premium",
    completeStatus: "Complete",
    
    // Loading Messages
    processingQuote: "AI Agents Processing Quote...",
    processingSteps: "Risk Analysis • Conversion Prediction • Premium Optimization",
    
    // Result Card Labels
    riskLevel: "Risk Level",
    conversionProbability: "Conversion Probability",
    recommendedPremium: "Recommended Premium",
    decision: "Decision",
    
    // Quote History Section
    quoteHistory: "Quote History",
    idColumn: "ID",
    riskColumn: "Risk",
    probabilityColumn: "Probability",
    decisionColumn: "Decision",
    
    // Validation Messages
    fillRequiredFields: "Please fill all required fields (Driver Age, Driving Experience, and Current Premium)",
    analysisError: "Error analyzing quote. Please try again.",
    
    // Status indicators
    failed: "❌ Failed",
    riskHigh: "HIGH",
riskMedium: "MEDIUM",
riskLow: "LOW",

decisionApprove: "APPROVE",
decisionReview: "REVIEW",
decisionReject: "REJECT",
decisionEscalate: "ESCALATE TO UNDERWRITER",
  },

  te: {
    // Language selector
    selectLanguage: "భాష ఎంచుకోండి",
    appTitle: "స్వయంచాలక కోట్ ఏజెంట్",
subtitle: "AI ఆధారిత అండర్రైటింగ్, కన్వర్షన్ అంచనా మరియు స్థానిక Ollama వివరణలు.",
language: "భాష",
    
    // Driver Information Section
    driverInformation: "డ్రైవర్ సమాచారం",
    driverAge: "డ్రైవర్ వయస్సు",
    drivingExperience: "డ్రైవింగ్ అనుభవం",
    previousAccidents: "గత ప్రమాదాలు",
    trafficViolations: "ట్రాఫిక్ ఉల్లంఘన సంఖ్య",
    
    // Vehicle Information Section
    vehicleInformation: "వాహన సమాచారం",
    vehicleUsage: "వాహన ఉపయోగం",
    personalUsage: "వ్యక్తిగత",
    businessUsage: "వ్యాపారం",
    commercialUsage: "వాణిజ్య",
    coverageLevel: "కవరేజ్ స్థాయి",
    basicCoverage: "ప్రాథమిక",
    standardCoverage: "ప్రామాణిక",
    premiumCoverage: "ప్రీమియం",
    annualMiles: "వార్షిక మైళ్లు",
    vehicleCostRange: "వాహన ఖర్చు పరిధి",
    below5Lakh: "₹5 లక్ష కంటే తక్కువ",
    range5to10Lakh: "₹5 - ₹10 లక్ష",
    range10to20Lakh: "₹10 - ₹20 లక్ష",
    above20Lakh: "₹20 లక్ష పైన",
    
    // Financial Information Section
    financialInformation: "ఆర్థిక సమాచారం",
    salaryRange: "జీతం పరిధి",
    below3Lakh: "₹3 లక్ష కంటే తక్కువ",
    range3to6Lakh: "₹3 - ₹6 లక్ష",
    range6to12Lakh: "₹6 - ₹12 లక్ష",
    above12Lakh: "₹12 లక్ష పైన",
    currentPremium: "ప్రస్తుత బీమా ప్రీమియం (₹/సంవత్సరం)",
    
    // Quote Analysis Section
    quoteAnalysis: "కోట్ విశ్లేషణ",
    analysisDescription: "స్వయంప్రక్రియ ఏజెంట్ పైపলైన్ను అమలు చేయడానికి క్రింద ఉన్న బటన్‌ను క్లిక్ చేయండి.",
    analyzeQuote: "కోట్ విశ్లేషించండి",
    
    // Agent Pipeline Section
    agentPipeline: "ఏజెంట్ పైపలైన్",
    riskProfilerLabel: "ఝుંపు ప్రొఫైలర్",
    conversionPredictorLabel: "కన్వర్షన్ ప్రిడిక్టర్",
    premiumAdvisorLabel: "ప్రీమియం సలహాదారు",
    decisionRouterLabel: "నిర్ణయ రూటర్",
    
    // Agent Status Messages
    waitingStatus: "వేచి ఉన్నారు",
    riskProfilerStatus: "ఝుంపు ప్రొఫైల్ విశ్లేషణ",
    conversionPredictorStatus: "కన్వర్షన్ ఊహించుకుంటున్నారు",
    advisorStatus: "ప్రీమియం ఆప్టిమైజ్ చేస్తున్నారు",
    completeStatus: "పూర్తయింది",
    
    // Loading Messages
    processingQuote: "AI ఏజెంట్‌లు కోట్‌ను ప్రాసెస్ చేస్తున్నారు...",
    processingSteps: "ఝుంపు విశ్లేషణ • కన్వర్షన్ ఊహ • ప్రీమియం ఆప్టిమైజేషన్",
    
    // Result Card Labels
    riskLevel: "ఝుంపు స్థాయి",
    conversionProbability: "కన్వర్షన్ సంభావ్యత",
    recommendedPremium: "సిఫారసు చేసిన ప్రీమియం",
    decision: "నిర్ణయం",
    
    // Quote History Section
    quoteHistory: "కోట్ చరిత్ర",
    idColumn: "ID",
    riskColumn: "ఝుంపు",
    probabilityColumn: "సంభావ్యత",
    decisionColumn: "నిర్ణయం",
    
    // Validation Messages
    fillRequiredFields: "దయచేసి అన్ని అవసరమైన ఫీల్డ్‌లను పూరించండి (డ్రైవర్ వయస్సు, డ్రైవింగ్ అనుభవం మరియు ప్రస్తుత ప్రీమియం)",
    analysisError: "కోట్ విశ్లేషణ సమయంలో లోపం. దయచేసి మళ్లీ ప్రయత్నించండి.",
    
    // Status indicators
    failed: "❌ విఫలమైనది",
    riskHigh: "అధికం",
riskMedium: "మధ్యస్థం",
riskLow: "తక్కువ",

decisionApprove: "ఆమోదించండి",
decisionReview: "సమీక్షించండి",
decisionReject: "తిరస్కరించండి",
decisionEscalate: "అండర్‌రైటర్‌కు పంపండి",
  },

  hi: {
    // Language selector
    selectLanguage: "भाषा चुनें",
    appTitle: "ऑटोनॉमस कोट एजेंट",
subtitle: "AI आधारित अंडरराइटिंग, रूपांतरण पूर्वानुमान और स्थानीय Ollama स्पष्टीकरण।",
language: "भाषा",
    
    // Driver Information Section
    driverInformation: "ड्राइवर सूचना",
    driverAge: "ड्राइवर की उम्र",
    drivingExperience: "ड्राइविंग अनुभव",
    previousAccidents: "पिछली दुर्घटनाएं",
    trafficViolations: "ट्रैफिक उल्लंघन गणना",
    
    // Vehicle Information Section
    vehicleInformation: "वाहन सूचना",
    vehicleUsage: "वाहन उपयोग",
    personalUsage: "व्यक्तिगत",
    businessUsage: "व्यवसाय",
    commercialUsage: "वाणिज्यिक",
    coverageLevel: "कवरेज स्तर",
    basicCoverage: "बुनियादी",
    standardCoverage: "मानक",
    premiumCoverage: "प्रीमियम",
    annualMiles: "वार्षिक मील",
    vehicleCostRange: "वाहन लागत सीमा",
    below5Lakh: "₹5 लाख से कम",
    range5to10Lakh: "₹5 - ₹10 लाख",
    range10to20Lakh: "₹10 - ₹20 लाख",
    above20Lakh: "₹20 लाख से ऊपर",
    
    // Financial Information Section
    financialInformation: "वित्तीय सूचना",
    salaryRange: "वेतन सीमा",
    below3Lakh: "₹3 लाख से कम",
    range3to6Lakh: "₹3 - ₹6 लाख",
    range6to12Lakh: "₹6 - ₹12 लाख",
    above12Lakh: "₹12 लाख से ऊपर",
    currentPremium: "वर्तमान बीमा प्रीमियम (₹/वर्ष)",
    
    // Quote Analysis Section
    quoteAnalysis: "कोट विश्लेषण",
    analysisDescription: "स्वायत्त एजेंट पाइपलाइन चलाने के लिए नीचे बटन पर क्लिक करें।",
    analyzeQuote: "कोट विश्लेषण करें",
    
    // Agent Pipeline Section
    agentPipeline: "एजेंट पाइपलाइन",
    riskProfilerLabel: "जोखिम प्रोफाइलर",
    conversionPredictorLabel: "रूपांतरण भविष्यद्वक्ता",
    premiumAdvisorLabel: "प्रीमियम सलाहकार",
    decisionRouterLabel: "निर्णय राउटर",
    
    // Agent Status Messages
    waitingStatus: "प्रतीक्षा में",
    riskProfilerStatus: "जोखिम प्रोफाइल विश्लेषण",
    conversionPredictorStatus: "रूपांतरण भविष्यवाणी",
    advisorStatus: "प्रीमियम अनुकूलन",
    completeStatus: "पूर्ण",
    
    // Loading Messages
    processingQuote: "AI एजेंट कोट संसाधित कर रहे हैं...",
    processingSteps: "जोखिम विश्लेषण • रूपांतरण भविष्यवाणी • प्रीमियम अनुकूलन",
    
    // Result Card Labels
    riskLevel: "जोखिम स्तर",
    conversionProbability: "रूपांतरण संभावना",
    recommendedPremium: "अनुशंसित प्रीमियम",
    decision: "निर्णय",
    
    // Quote History Section
    quoteHistory: "कोट का इतिहास",
    idColumn: "ID",
    riskColumn: "जोखिम",
    probabilityColumn: "संभावना",
    decisionColumn: "निर्णय",
    
    // Validation Messages
    fillRequiredFields: "कृपया सभी आवश्यक फ़ील्ड भरें (ड्राइवर की उम्र, ड्राइविंग अनुभव और वर्तमान प्रीमियम)",
    analysisError: "कोट विश्लेषण में त्रुटि। कृपया पुनः प्रयास करें।",
    
    // Status indicators
    failed: "❌ विफल",
    riskHigh: "उच्च",
riskMedium: "मध्यम",
riskLow: "कम",

decisionApprove: "स्वीकृत",
decisionReview: "समीक्षा करें",
decisionReject: "अस्वीकृत",
decisionEscalate: "अंडरराइटर को भेजें", 
  },

  ta: {
    // Language selector
    selectLanguage: "மொழியைத் தேர்வுசெய்யுங்கள்",
    appTitle: "தானியங்கி மேற்கோள் முகவர்",
subtitle: "AI அடிப்படையிலான மதிப்பீடு, மாற்று கணிப்பு மற்றும் உள்ளூர் Ollama விளக்கங்கள்.",
language: "மொழி",
    
    // Driver Information Section
    driverInformation: "ஓட்டுநர் தகவல்",
    driverAge: "ஓட்டுநர் வயது",
    drivingExperience: "வாகனம் ஓட்டிய அனுபவம்",
    previousAccidents: "முந்தைய விபத்துக்கள்",
    trafficViolations: "போக்குவரத்து மீறல் எண்ணிக்கை",
    
    // Vehicle Information Section
    vehicleInformation: "வாகன தகவல்",
    vehicleUsage: "வாகனத்தின் பயன்பாடு",
    personalUsage: "ব్যक్తिगत",
    businessUsage: "வணிகம்",
    commercialUsage: "வணிக",
    coverageLevel: "கவரேஜ் நிலை",
    basicCoverage: "அடிப்படை",
    standardCoverage: "நிலையான",
    premiumCoverage: "பிரீமியம்",
    annualMiles: "வার்ષிக மைல்கள்",
    vehicleCostRange: "வாகன செலவு வரம்பு",
    below5Lakh: "₹5 லட்சத்திற்கும் குறைவாக",
    range5to10Lakh: "₹5 - ₹10 லட்சம்",
    range10to20Lakh: "₹10 - ₹20 லட்சம்",
    above20Lakh: "₹20 லட்சத்திற்கு மேல்",
    
    // Financial Information Section
    financialInformation: "நிதி தகவல்",
    salaryRange: "சம்பள வரம்பு",
    below3Lakh: "₹3 லட்சத்திற்கும் குறைவாக",
    range3to6Lakh: "₹3 - ₹6 லட்சம்",
    range6to12Lakh: "₹6 - ₹12 லட்சம்",
    above12Lakh: "₹12 லட்சத்திற்கு மேல்",
    currentPremium: "தற்போதைய காப்பீட்டு பிரீமியம் (₹/வருடம்)",
    
    // Quote Analysis Section
    quoteAnalysis: "மேற்ப்பார்வை பிரிவு பகுப்பாய்வு",
    analysisDescription: "தன்னாட்சை முகவர் குழாய்ப் பரিக்ரமணத்தை இயக்க கீழே உள்ள பொத்தானைக் கிளிக் செய்யவும்.",
    analyzeQuote: "மேற்ப்பார்வை பரிక்ரமணை பகுப்பாய்வு செய்யவும்",
    
    // Agent Pipeline Section
    agentPipeline: "முகவர் குழாயி",
    riskProfilerLabel: "ஆபத்து சரிவை மிதி",
    conversionPredictorLabel: "மாற்றம் கணிப்பு",
    premiumAdvisorLabel: "பிரீமியம் ஆலோசகர்",
    decisionRouterLabel: "முடிவு ஏற்பாட்டாளர்",
    
    // Agent Status Messages
    waitingStatus: "வெதிர்பாரக்கிறது",
    riskProfilerStatus: "ஆபத்து சரிவை பகுப்பாய்வு",
    conversionPredictorStatus: "மாற்றம் கணிப்பு",
    advisorStatus: "பிரீமியம் உத்தம",
    completeStatus: "முடிந்தது",
    
    // Loading Messages
    processingQuote: "AI முகவர்கள் மேற்ப்பார்வை பிரிவை செயல்படுத்துகின்றன...",
    processingSteps: "ஆபத்து பகுப்பாய்வு • மாற்றம் கணிப்பு • பிரீமியம் உத்தம",
    
    // Result Card Labels
    riskLevel: "ஆபத்து நிலை",
    conversionProbability: "மாற்றம் நிகழ்தகவு",
    recommendedPremium: "பரிந்துரைக்கப்பட்ட பிரீமியம்",
    decision: "முடிவு",
    
    // Quote History Section
    quoteHistory: "மேற்ப்பார்வை வரலாறு",
    idColumn: "ID",
    riskColumn: "ஆபத்து",
    probabilityColumn: "நிகழ்தகவு",
    decisionColumn: "முடிவு",
    
    // Validation Messages
    fillRequiredFields: "தயவுசெய்து அனைத்து தேவையான புலங்களையும் நிரப்பவும் (ஓட்டுநர் வயது, வாகனம் ஓட்டிய அனுபவம் மற்றும் தற்போதைய பிரீமியம்)",
    analysisError: "மேற்ப்பார்வை பிரிவு பகுப்பாய்வில் பிழை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
    
    // Status indicators
    failed: "❌ தோல்வியடைந்தது",

    riskHigh: "அதிகம்",
riskMedium: "நடுத்தரம்",
riskLow: "குறைவு",

decisionApprove: "ஒப்புதல்",
decisionReview: "மதிப்பாய்வு",
decisionReject: "நிராகரி",
decisionEscalate: "அண்டர்ரைட்டருக்கு அனுப்பு",
  }
};
