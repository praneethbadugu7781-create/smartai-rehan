document.addEventListener('DOMContentLoaded', () => {
    
    // DOM Elements
    const farmForm = document.getElementById('farmForm');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingStatusText = document.getElementById('loadingStatusText');
    const loadingFill = document.getElementById('loadingFill');
    const resultsSection = document.getElementById('resultsSection');
    const btnRecalculate = document.getElementById('btnRecalculate');
    const presetButtonsContainer = document.getElementById('presetButtons');
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    // Chart instances
    let suitabilityChartInstance = null;
    let economicsChartInstance = null;

    // Mobile Navigation Toggle
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '4.5rem';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.backgroundColor = '#FFFFFF';
                navLinks.style.padding = '1.5rem';
                navLinks.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)';
            }
        });
    }

    // 1. Quick Sample Data Presets
    const samplePresets = {
        "rice_monsoon": { N: 90, P: 42, K: 43, temperature: 23.6, humidity: 82.0, ph: 6.5, rainfall: 220.5 },
        "wheat_winter": { N: 35, P: 65, K: 80, temperature: 19.2, humidity: 16.5, ph: 6.8, rainfall: 75.0 },
        "cotton_cash":  { N: 125, P: 48, K: 20, temperature: 24.5, humidity: 80.0, ph: 7.2, rainfall: 78.0 },
        "apple_temperate": { N: 20, P: 135, K: 200, temperature: 22.0, humidity: 92.0, ph: 6.0, rainfall: 110.0 }
    };

    if (presetButtonsContainer) {
        presetButtonsContainer.addEventListener('click', (e) => {
            const btn = e.target.closest('.btn-preset');
            if (!btn) return;
            const key = btn.dataset.preset;
            if (samplePresets[key]) {
                fillFormValues(samplePresets[key]);
                clearFormErrors();
            }
        });
    }

    function fillFormValues(data) {
        Object.keys(data).forEach(field => {
            const input = document.getElementById(field);
            if (input) {
                input.value = data[field];
            }
        });
    }

    // 2. Form Input Validation
    const validationBounds = {
        N: { min: 0, max: 250, name: 'Nitrogen' },
        P: { min: 0, max: 250, name: 'Phosphorus' },
        K: { min: 0, max: 250, name: 'Potassium' },
        temperature: { min: -10, max: 60, name: 'Temperature' },
        humidity: { min: 0, max: 100, name: 'Humidity' },
        ph: { min: 0, max: 14, name: 'pH Level' },
        rainfall: { min: 0, max: 1000, name: 'Rainfall' }
    };

    function clearFormErrors() {
        Object.keys(validationBounds).forEach(field => {
            const input = document.getElementById(field);
            const errDiv = document.getElementById(`err-${field}`);
            if (input) input.classList.remove('invalid');
            if (errDiv) {
                errDiv.textContent = '';
                errDiv.style.display = 'none';
            }
        });
    }

    function validateFormInputs() {
        clearFormErrors();
        let isValid = true;
        const formData = {};

        Object.keys(validationBounds).forEach(field => {
            const input = document.getElementById(field);
            const errDiv = document.getElementById(`err-${field}`);
            const bound = validationBounds[field];

            if (!input || input.value.trim() === '') {
                showFieldError(input, errDiv, `${bound.name} field cannot be empty.`);
                isValid = false;
                return;
            }

            const val = parseFloat(input.value);
            if (isNaN(val)) {
                showFieldError(input, errDiv, `Please enter a valid numeric value for ${bound.name}.`);
                isValid = false;
                return;
            }

            if (val < bound.min || val > bound.max) {
                showFieldError(input, errDiv, `${bound.name} must be between ${bound.min} and ${bound.max}.`);
                isValid = false;
                return;
            }

            formData[field] = val;
        });

        return isValid ? formData : null;
    }

    function showFieldError(input, errDiv, message) {
        if (input) input.classList.add('invalid');
        if (errDiv) {
            errDiv.textContent = message;
            errDiv.style.display = 'block';
        }
    }

    // 3. Form Submission & AJAX Call
    farmForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = validateFormInputs();
        if (!payload) {
            return;
        }

        // Show Agricultural Loading Sequence
        triggerLoadingSequence(async () => {
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (response.ok && data.status === 'success') {
                    renderResultsDashboard(data);
                } else {
                    alert(`Analysis Error: ${data.message || 'Server encountered an issue.'}`);
                }
            } catch (err) {
                console.error(err);
                alert('Network request failed. Please check if Flask server is running.');
            } finally {
                hideLoadingSequence();
            }
        });
    });

    // 4. Loading Sequence & Messages
    function triggerLoadingSequence(callback) {
        loadingOverlay.classList.add('active');
        loadingFill.style.width = '0%';
        
        const statusMessages = [
            "Reading soil conditions...",
            "Evaluating crop suitability...",
            "Analyzing weather patterns...",
            "Checking resource requirements...",
            "Calculating farm economics...",
            "Preparing SmartAgri report..."
        ];

        let step = 0;
        const interval = setInterval(() => {
            if (step < statusMessages.length) {
                loadingStatusText.textContent = statusMessages[step];
                const progress = Math.min(100, Math.round(((step + 1) / statusMessages.length) * 100));
                loadingFill.style.width = `${progress}%`;
                step++;
            } else {
                clearInterval(interval);
                callback();
            }
        }, 300);
    }

    function hideLoadingSequence() {
        setTimeout(() => {
            loadingOverlay.classList.remove('active');
        }, 400);
    }

    // 5. Render Results Dashboard
    function renderResultsDashboard(data) {
        resultsSection.classList.remove('hidden');

        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Summary Cards
        document.getElementById('resBestCropName').textContent = data.best_crop.display_name;
        document.getElementById('resBestCropCat').textContent = `${data.best_crop.icon} ${data.crop_information.category}`;
        document.getElementById('resConfidenceVal').textContent = `${data.best_crop.confidence}%`;
        
        const soilHealthElem = document.getElementById('resSoilHealthVal');
        soilHealthElem.textContent = data.soil_analysis.overall_status;
        document.getElementById('resSoilHealthSub').textContent = data.soil_analysis.ph_status + " pH";

        document.getElementById('resProfitVal').textContent = data.economics.formatted_profit;
        document.getElementById('resRevenueVal').textContent = `Revenue: ${data.economics.formatted_revenue}`;

        // Render Top 3 Crop Cards
        renderTop3Cards(data.top_3_crops);

        // Render Suitability Chart
        renderSuitabilityChart(data.top_3_crops);

        // Soil Analysis Breakdown
        document.getElementById('badgeSoilStatus').textContent = data.soil_analysis.overall_status;
        document.getElementById('soilSummaryText').textContent = data.soil_analysis.summary;

        document.getElementById('valSoilN').textContent = `${data.inputs.N} mg/kg`;
        document.getElementById('badgeSoilN').textContent = data.soil_analysis.nitrogen_status;
        
        document.getElementById('valSoilP').textContent = `${data.inputs.P} mg/kg`;
        document.getElementById('badgeSoilP').textContent = data.soil_analysis.phosphorus_status;

        document.getElementById('valSoilK').textContent = `${data.inputs.K} mg/kg`;
        document.getElementById('badgeSoilK').textContent = data.soil_analysis.potassium_status;

        document.getElementById('valSoilPH').textContent = `${data.inputs.ph} pH`;
        document.getElementById('badgeSoilPH').textContent = data.soil_analysis.ph_status;

        // Fertilizer Guidance List
        const fertilizerList = document.getElementById('fertilizerList');
        fertilizerList.innerHTML = '';
        data.fertilizer_guidance.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            fertilizerList.appendChild(li);
        });

        // Water Requirement
        document.getElementById('waterLevelDisplay').textContent = data.crop_information.water_requirement;
        document.getElementById('waterDescText').textContent = `Optimal for ${data.crop_information.water_requirement.toLowerCase()} water demand crop management.`;

        // Weather Intelligence
        document.getElementById('weatherSummaryText').textContent = data.weather_analysis.summary;
        document.getElementById('wmTemp').textContent = `${data.inputs.temperature} °C`;
        document.getElementById('wmHumidity').textContent = `${data.inputs.humidity} %`;
        document.getElementById('wmRainfall').textContent = `${data.inputs.rainfall} mm`;
        document.getElementById('weatherRiskText').textContent = data.weather_analysis.moisture_risk;

        // Alternative Crop Card
        document.getElementById('altCropIcon').textContent = data.alternative_crop.icon;
        document.getElementById('altCropName').textContent = data.alternative_crop.display_name;
        document.getElementById('altCropSuitability').textContent = `${data.alternative_crop.probability}% Suitability`;
        document.getElementById('altCropReason').textContent = data.alternative_crop.reason;
        document.getElementById('altCropWater').textContent = data.alternative_crop.water_requirement;
        document.getElementById('altCropProfit').textContent = data.alternative_crop.estimated_profit;

        // Crop Profile
        document.getElementById('cropCategory').textContent = data.crop_information.category;
        document.getElementById('cropSeason').textContent = data.crop_information.season;
        document.getElementById('cropDuration').textContent = data.crop_information.growth_duration;
        document.getElementById('cropIdealPH').textContent = data.crop_information.ideal_ph;
        document.getElementById('cropIdealTemp').textContent = data.crop_information.ideal_temp;

        // Economics Metrics & Chart
        document.getElementById('econYield').textContent = `${data.economics.yield_quintal_per_acre} quintals / acre`;
        document.getElementById('econPrice').textContent = data.economics.formatted_price;
        document.getElementById('econCost').textContent = data.economics.formatted_cost;
        document.getElementById('econRevenue').textContent = data.economics.formatted_revenue;
        document.getElementById('econNetProfit').textContent = `${data.economics.formatted_profit} / acre`;

        renderEconomicsChart(data.economics);

        // Smart Recommendation Summary Text
        document.getElementById('smartRecText').textContent = data.smart_recommendation;

        // Re-initialize Lucide Icons for injected components
        if (window.lucide) {
            lucide.createIcons();
        }
    }

    // 6. Top 3 Cards Renderer
    function renderTop3Cards(top3) {
        const container = document.getElementById('top3Container');
        container.innerHTML = '';

        const medalBadges = ['🥇 #1 Best Match', '🥈 #2 Runner-Up', '🥉 #3 Alternative'];

        top3.forEach((item, idx) => {
            const rankClass = `rank-${item.rank}`;
            const cardHtml = `
                <div class="crop-rank-card ${rankClass}">
                    <span class="medal-badge">${medalBadges[idx] || '#' + item.rank}</span>
                    <div class="crc-icon">${item.icon}</div>
                    <div class="crc-name">${item.display_name}</div>
                    <div class="crc-prob">${item.probability}%</div>
                    <div class="crc-progress-bg">
                        <div class="crc-progress-fill" style="width: ${item.probability}%"></div>
                    </div>
                </div>
            `;
            container.innerHTML += cardHtml;
        });
    }

    // 7. Chart.js Suitability Chart
    function renderSuitabilityChart(top3) {
        const ctx = document.getElementById('suitabilityChart').getContext('2d');
        
        if (suitabilityChartInstance) {
            suitabilityChartInstance.destroy();
        }

        const labels = top3.map(t => t.display_name);
        const dataVals = top3.map(t => t.probability);

        suitabilityChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Model Probability (%)',
                    data: dataVals,
                    backgroundColor: [
                        'rgba(217, 119, 6, 0.85)',
                        'rgba(45, 106, 79, 0.75)',
                        'rgba(2, 132, 199, 0.75)'
                    ],
                    borderColor: [
                        '#D97706',
                        '#2D6A4F',
                        '#0284C7'
                    ],
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` Suitability: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) { return value + '%'; }
                        }
                    }
                }
            }
        });
    }

    // 8. Chart.js Financial Economics Chart
    function renderEconomicsChart(econ) {
        const ctx = document.getElementById('economicsChart').getContext('2d');

        if (economicsChartInstance) {
            economicsChartInstance.destroy();
        }

        economicsChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Gross Revenue', 'Cultivation Cost', 'Net Profit'],
                datasets: [{
                    label: 'Amount (₹ / acre)',
                    data: [econ.estimated_revenue_inr, econ.cultivation_cost_per_acre_inr, econ.estimated_profit_inr],
                    backgroundColor: [
                        'rgba(2, 132, 199, 0.75)',
                        'rgba(220, 38, 38, 0.75)',
                        'rgba(5, 150, 105, 0.85)'
                    ],
                    borderColor: [
                        '#0284C7',
                        '#DC2626',
                        '#059669'
                    ],
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` ₹ ${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + (value / 1000) + 'k';
                            }
                        }
                    }
                }
            }
        });
    }

    // Recalculate Button Scroll Back to Form
    if (btnRecalculate) {
        btnRecalculate.addEventListener('click', () => {
            document.getElementById('analyze').scrollIntoView({ behavior: 'smooth' });
        });
    }

});
