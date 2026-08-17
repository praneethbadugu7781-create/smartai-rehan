def analyze_soil(n, p, k, ph):
    """
    Evaluates soil N, P, K, and pH levels based on agronomic standards.
    Returns structured soil status and individual feature evaluations.
    """
    n_status = "Low" if n < 40 else ("High" if n > 110 else "Adequate")
    p_status = "Low" if p < 30 else ("High" if p > 75 else "Adequate")
    k_status = "Low" if k < 30 else ("High" if k > 75 else "Adequate")
    
    if ph < 5.5:
        ph_status = "Acidic"
    elif ph > 7.5:
        ph_status = "Alkaline"
    else:
        ph_status = "Optimal"
        
    deviations = 0
    if n_status != "Adequate": deviations += 1
    if p_status != "Adequate": deviations += 1
    if k_status != "Adequate": deviations += 1
    if ph_status != "Optimal": deviations += 1
    
    if deviations == 0:
        overall_status = "Healthy"
        status_color = "success"
        summary = "Soil nutrient profile and pH are nicely balanced for optimal crop development."
    elif deviations == 1:
        overall_status = "Moderate"
        status_color = "warning"
        summary = "Soil condition is acceptable, but one nutrient parameter requires light management."
    else:
        overall_status = "Needs Attention"
        status_color = "danger"
        summary = "Soil exhibits multiple nutrient imbalances or extreme pH requiring conditioning."
        
    return {
        "overall_status": overall_status,
        "status_color": status_color,
        "summary": summary,
        "nitrogen_status": n_status,
        "phosphorus_status": p_status,
        "potassium_status": k_status,
        "ph_status": ph_status,
        "disclaimer": "Based on standard project nutrient & pH classification rules."
    }
