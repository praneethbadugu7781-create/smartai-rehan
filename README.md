# SmartAgri AI — Intelligent Crop Recommendation & Farm Profit Analysis System

SmartAgri AI is a real, fully functional, production-ready agricultural decision-support web application. It combines machine learning crop suitability classification with soil health diagnosis, fertilizer management, weather risk analysis, and farm economics to assist farmers and agricultural analysts in making data-driven farming decisions.

---

## 🌟 Key Features

1. **Random Forest Crop Recommendation Engine**:
   - Uses a trained `RandomForestClassifier` on 7 soil and climate features (`N, P, K, temperature, humidity, ph, rainfall`).
   - Achieves **99.32% test classification accuracy**.

2. **True Top-3 Probability Ranking**:
   - Utilizes `model.predict_proba()` to rank crops by statistical suitability percentage.
   - Displays Gold (🥇 #1), Silver (🥈 #2), and Bronze (🥉 #3) match cards with animated confidence progress bars.

3. **Decoupled Farm Economics Engine**:
   - Uses a dedicated `crop_economics.csv` dataset.
   - Computes expected yield (quintals/acre), market price per quintal (₹), cultivation cost (₹/acre), **Gross Revenue**, and **Estimated Net Profit / Acre**.

4. **Soil Health & Fertilizer Guidance**:
   - Evaluates N, P, K, and soil pH levels against standard agronomic baselines.
   - Categorizes soil condition into *Healthy*, *Moderate*, or *Needs Attention*.
   - Recommends specific eco-friendly and balanced soil management steps.

5. **Weather & Resource Insights**:
   - Evaluates temperature, relative humidity, and seasonal rainfall.
   - Classifies water requirement level (**HIGH**, **MEDIUM**, **LOW**).
   - Recommends alternative crops for risk mitigation.

6. **Light Agricultural Design System**:
   - Clean, modern, responsive visual identity (Forest Green `#1B4D3E`, Warm Ivory background `#F8FAF6`, Soft Sunlight accents).
   - Dynamic Chart.js visualizations for crop suitability and financial comparisons.
   - Custom agricultural loading sequence with cycling status messages.

---

## 🏗️ System Architecture

```text
SmartAgri_AI/
│
├── app.py                      # Main Flask Web Application & API Routes
├── requirements.txt            # Python Dependencies
├── README.md                   # Complete Documentation
├── .gitignore                  # Git Ignore Settings
│
├── model/
│   └── crop_model.pkl          # Trained Random Forest Model Binary
│
├── dataset/
│   ├── crop_data.csv           # 2,200 Agronomic Crop Records (22 Crops)
│   ├── crop_economics.csv      # Regional Yield, Price & Cost Dataset
│   └── generate_dataset.py     # Dataset Generation Script
│
├── training/
│   └── train_model.py          # Model Training & Evaluation Pipeline
│
├── templates/
│   └── index.html              # Modern Responsive Web Interface
│
├── static/
│   ├── css/
│   │   └── style.css           # Light Agricultural CSS3 Design System
│   └── js/
│       └── app.js              # Form Validation, AJAX & Chart.js Logic
│
└── utils/
    ├── soil_analysis.py        # Soil Status & Nutrient Diagnostics
    ├── fertilizer.py           # Fertilizer & pH Guidance Generator
    ├── weather_analysis.py     # Thermal & Rainfall Risk Analysis
    ├── crop_information.py     # Agronomic Profiles & Water Requirements
    └── economics.py            # Revenue & Net Profit Calculator
```

---

## 📊 Economic Calculation Formulas

Economic calculations are kept separate from the ML classifier model:

$$\text{Gross Revenue} = \text{Expected Yield (quintals/acre)} \times \text{Market Price per Quintal (\text{₹})}$$

$$\text{Estimated Net Profit} = \text{Gross Revenue} - \text{Cultivation Cost (\text{₹}/acre)}$$

Example for **Rice**:
- Expected Yield = $25\text{ quintals/acre}$
- Market Price = $\text{₹}2,300\text{ / quintal}$
- Gross Revenue = $25 \times 2,300 = \text{₹}57,500$
- Cultivation Cost = $\text{₹}35,000\text{ / acre}$
- **Estimated Net Profit** = $\text{₹}57,500 - \text{₹}35,000 = \text{₹}22,500\text{ / acre}$

---

## ⚡ Installation & Execution Guide

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Step 1: Clone or Navigate to Project Directory
```bash
cd "d:/smartai rehan"
```

### Step 2: Set Up Virtual Environment (Optional but Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the Random Forest Model
```bash
python training/train_model.py
```
*Outputs model accuracy metrics and saves `model/crop_model.pkl`.*

### Step 5: Launch the SmartAgri AI Server
```bash
python app.py
```

### Step 6: Open Web Application
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧪 API Endpoints

### 1. `GET /`
Renders the main SmartAgri AI interactive web application.

### 2. `GET /api/sample-data`
Returns pre-configured valid soil and weather input presets for fast demonstration.

### 3. `POST /predict`
Submits 7 input features to the trained model and decision support modules.

**Sample Request Body:**
```json
{
  "N": 90.0,
  "P": 42.0,
  "K": 43.0,
  "temperature": 23.6,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```

---

## ⚠️ Academic Disclaimer & Limitations

- **Model Probability**: AI confidence represents statistical suitability based on historical dataset alignment and is not a guaranteed biological harvest outcome.
- **Economic Estimates**: Economic prices, costs, and yields reflect regional benchmark demo values and may not represent live real-time commodity spot market prices.
- **Real-World Factors**: Actual farm profitability is influenced by local weather events, pest outbreaks, labor rates, fuel costs, transportation, storage, and government subsidies.
