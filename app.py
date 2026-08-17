import os
import sys
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify

# Import domain utility modules
from utils.soil_analysis import analyze_soil
from utils.fertilizer import generate_fertilizer_guidance
from utils.weather_analysis import analyze_weather
from utils.crop_information import get_crop_info
from utils.economics import calculate_crop_economics

app = Flask(__name__)

# Load trained Random Forest model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'crop_model.pkl')
crop_model = None

def load_ml_model():
    global crop_model
    if os.path.exists(MODEL_PATH):
        try:
            crop_model = joblib.load(MODEL_PATH)
            print(f"[OK] Random Forest model loaded successfully from {MODEL_PATH}")
        except Exception as e:
            print(f"[ERROR] Failed to load ML model: {e}")
            crop_model = None
    else:
        print(f"[WARNING] Model file not found at {MODEL_PATH}. Please run training/train_model.py first.")

load_ml_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    return render_template('index.html')

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Provides sample input presets for quick UI demonstration."""
    samples = {
        "rice_monsoon": {
            "title": "🌾 Rice / Monsoon Preset",
            "N": 90, "P": 42, "K": 43,
            "temperature": 23.6, "humidity": 82.0,
            "ph": 6.5, "rainfall": 220.5
        },
        "wheat_winter": {
            "title": "🌱 Chickpea / Dry Winter Preset",
            "N": 35, "P": 65, "K": 80,
            "temperature": 19.2, "humidity": 16.5,
            "ph": 6.8, "rainfall": 75.0
        },
        "cotton_cash": {
            "title": "☁️ Cotton / Black Soil Preset",
            "N": 125, "P": 48, "K": 20,
            "temperature": 24.5, "humidity": 80.0,
            "ph": 7.2, "rainfall": 78.0
        },
        "apple_temperate": {
            "title": "🍎 Apple / Hilly Cool Preset",
            "N": 20, "P": 135, "K": 200,
            "temperature": 22.0, "humidity": 92.0,
            "ph": 6.0, "rainfall": 110.0
        }
    }
    return jsonify({"status": "success", "samples": samples})

@app.route('/predict', methods=['POST'])
def predict():
    if crop_model is None:
        return jsonify({
            "status": "error",
            "message": "ML Model is not loaded. Please ensure training/train_model.py has been run."
        }), 500

    try:
        data = request.get_json(force=True) if request.is_json else request.form.to_dict()
        
        # Parse and validate required feature fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        inputs = {}
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                return jsonify({"status": "error", "message": f"Missing or empty required field: {field}"}), 400
            try:
                val = float(data[field])
                inputs[field] = val
            except ValueError:
                return jsonify({"status": "error", "message": f"Invalid numeric value for {field}: {data[field]}"}), 400

        # Numeric range validation bounds
        bounds = {
            'N': (0, 250, 'Nitrogen (N)'),
            'P': (0, 250, 'Phosphorus (P)'),
            'K': (0, 250, 'Potassium (K)'),
            'temperature': (-10, 60, 'Temperature (°C)'),
            'humidity': (0, 100, 'Humidity (%)'),
            'ph': (0, 14, 'Soil pH'),
            'rainfall': (0, 1000, 'Rainfall (mm)')
        }
        for field, (min_val, max_val, label) in bounds.items():
            if inputs[field] < min_val or inputs[field] > max_val:
                return jsonify({
                    "status": "error",
                    "message": f"{label} value {inputs[field]} is out of realistic range ({min_val} to {max_val})."
                }), 400

        # Construct DataFrame matching exact model feature order
        feature_order = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        input_df = pd.DataFrame([[inputs[f] for f in feature_order]], columns=feature_order)

        # 1. Real ML Top-3 Probabilities Prediction
        probabilities = crop_model.predict_proba(input_df)[0]
        classes = crop_model.classes_

        # Sort descending by probability
        sorted_indices = np.argsort(probabilities)[::-1]

        top_3 = []
        for rank, idx in enumerate(sorted_indices[:3], start=1):
            crop_label = str(classes[idx])
            prob_percent = round(float(probabilities[idx]) * 100, 1)
            info = get_crop_info(crop_label)
            top_3.append({
                "rank": rank,
                "crop": crop_label,
                "display_name": info['display_name'],
                "probability": prob_percent,
                "icon": info['icon']
            })

        best_crop = top_3[0]['crop']
        best_crop_display = top_3[0]['display_name']
        best_confidence = top_3[0]['probability']

        # 2. Decision Support Module Processing
        soil_res = analyze_soil(inputs['N'], inputs['P'], inputs['K'], inputs['ph'])
        fertilizer_res = generate_fertilizer_guidance(inputs['N'], inputs['P'], inputs['K'], inputs['ph'])
        weather_res = analyze_weather(inputs['temperature'], inputs['humidity'], inputs['rainfall'])
        crop_info_res = get_crop_info(best_crop)
        economics_res = calculate_crop_economics(best_crop)

        # Alternative crop (Rank 2) processing
        alt_crop = top_3[1]['crop'] if len(top_3) > 1 else "maize"
        alt_info = get_crop_info(alt_crop)
        alt_economics = calculate_crop_economics(alt_crop)
        alternative_crop_res = {
            "crop": alt_crop,
            "display_name": alt_info['display_name'],
            "probability": top_3[1]['probability'] if len(top_3) > 1 else 0.0,
            "icon": alt_info['icon'],
            "water_requirement": alt_info['water_requirement'],
            "reason": f"Ranked #2 by AI model. Suitable alternative if market prices or water supply vary.",
            "estimated_profit": alt_economics['formatted_profit']
        }

        # 3. Dynamic Smart Recommendation Generation
        smart_recommendation = (
            f"Based on the provided soil and weather conditions, {best_crop_display} received the highest model suitability "
            f"score of {best_confidence}%. The current soil condition is evaluated as {soil_res['overall_status']}, while {best_crop_display} "
            f"has {crop_info_res['water_requirement']} water requirements. Based on the project's economic dataset, the estimated profit is "
            f"{economics_res['formatted_profit']} per acre."
        )

        return jsonify({
            "status": "success",
            "inputs": inputs,
            "top_3_crops": top_3,
            "best_crop": {
                "name": best_crop,
                "display_name": best_crop_display,
                "confidence": best_confidence,
                "icon": crop_info_res['icon']
            },
            "soil_analysis": soil_res,
            "fertilizer_guidance": fertilizer_res,
            "weather_analysis": weather_res,
            "crop_information": crop_info_res,
            "economics": economics_res,
            "alternative_crop": alternative_crop_res,
            "smart_recommendation": smart_recommendation,
            "disclaimer": "AI confidence represents model probability and is not a guarantee of crop success. Economic values are project/demo values and may not represent current market prices."
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"status": "error", "message": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting SmartAgri AI Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
