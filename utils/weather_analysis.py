def analyze_weather(temp, humidity, rainfall):
    """
    Evaluates temperature, humidity, and rainfall to generate weather insight text.
    """
    # Thermal regime
    if temp < 18:
        thermal_desc = "cool temperature regime"
    elif temp <= 32:
        thermal_desc = "warm, favorable thermal zone"
    else:
        thermal_desc = "hot climate condition"
        
    # Humidity regime
    if humidity < 50:
        humidity_desc = "low atmospheric humidity"
    elif humidity <= 75:
        humidity_desc = "moderate humidity level"
    else:
        humidity_desc = "humid atmospheric environment"
        
    # Moisture regime
    if rainfall < 70:
        rainfall_desc = "low seasonal rainfall"
        moisture_risk = "Supplementary irrigation essential for water-intensive crops."
    elif rainfall <= 150:
        rainfall_desc = "moderate moisture supply"
        moisture_risk = "Well-balanced natural rainfall suitable for standard rain-fed/irrigated crops."
    else:
        rainfall_desc = "heavy rainfall conditions"
        moisture_risk = "Ensure adequate field drainage to prevent waterlogging and fungal disease."
        
    summary = f"Current inputs reflect a {thermal_desc} ({temp:.1f}°C) with {humidity_desc} ({humidity:.1f}%) and {rainfall_desc} ({rainfall:.1f} mm)."
    
    return {
        "temperature_c": temp,
        "humidity_percent": humidity,
        "rainfall_mm": rainfall,
        "summary": summary,
        "moisture_risk": moisture_risk,
        "disclaimer": "Rule-based analysis derived from user-provided weather inputs."
    }
