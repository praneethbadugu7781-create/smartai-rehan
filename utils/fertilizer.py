def generate_fertilizer_guidance(n, p, k, ph):
    """
    Generates basic fertilizer recommendations based on soil N, P, K, and pH levels.
    Provides standard organic and eco-friendly soil management suggestions.
    """
    recommendations = []
    
    # Nitrogen guidance
    if n < 40:
        recommendations.append("Nitrogen is low: Apply nitrogen-rich organic compost, neem-coated Urea, or incorporate leguminous green manure.")
    elif n > 110:
        recommendations.append("Nitrogen is high: Avoid synthetic nitrogen fertilizers to prevent excessive vegetative growth and nutrient leaching.")
    else:
        recommendations.append("Nitrogen level is optimal: Maintain current organic manure schedule.")
        
    # Phosphorus guidance
    if p < 30:
        recommendations.append("Phosphorus is low: Apply Single Super Phosphate (SSP) or Rock Phosphate during soil preparation to stimulate root growth.")
    elif p > 75:
        recommendations.append("Phosphorus is high: Skip phosphate application for this season to avoid micronutrient lockup.")
    else:
        recommendations.append("Phosphorus level is adequate: Supports healthy root structure and early flower development.")
        
    # Potassium guidance
    if k < 30:
        recommendations.append("Potassium is low: Supplement soil with Muriate of Potash (MOP) or bio-potash to enhance disease resistance and grain quality.")
    elif k > 75:
        recommendations.append("Potassium is high: Sufficient potassium reserves available; minimize extra potash inputs.")
    else:
        recommendations.append("Potassium level is optimal: Promotes crop hardiness and yield quality.")
        
    # pH soil conditioning
    if ph < 5.5:
        recommendations.append("Soil is acidic: Apply agricultural lime (calcium carbonate) to neutralize soil acidity and increase nutrient uptake.")
    elif ph > 7.5:
        recommendations.append("Soil is alkaline: Apply gypsum (calcium sulfate) or elemental sulfur to gently lower soil pH.")
    else:
        recommendations.append("Soil pH is ideal for most nutrient bioavailability.")
        
    return {
        "recommendations": recommendations,
        "disclaimer": "General agricultural guidance. Conduct local soil testing before chemical application."
    }
