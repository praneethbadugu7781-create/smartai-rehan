import os
import pandas as pd

_economics_df = None

def load_economics_data():
    global _economics_df
    if _economics_df is None:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'crop_economics.csv')
        if os.path.exists(csv_path):
            _economics_df = pd.read_csv(csv_path)
            _economics_df['crop_norm'] = _economics_df['crop'].astype(str).str.lower().str.strip()
        else:
            _economics_df = pd.DataFrame()
    return _economics_df

def calculate_crop_economics(crop_name):
    """
    Looks up economic metrics from dataset/crop_economics.csv and computes Revenue and Profit per acre.
    Formulas:
    Revenue = Expected Yield (quintals/acre) * Price per Quintal (₹)
    Estimated Profit = Estimated Revenue - Cultivation Cost (₹/acre)
    """
    df = load_economics_data()
    crop_norm = str(crop_name).lower().strip()
    
    match = df[df['crop_norm'] == crop_norm] if not df.empty and 'crop_norm' in df.columns else pd.DataFrame()
    
    if not match.empty:
        row = match.iloc[0]
        yield_per_acre = float(row['yield_quintal_per_acre'])
        price_per_quintal = float(row['price_per_quintal_inr'])
        cultivation_cost = float(row['cultivation_cost_per_acre_inr'])
        season = str(row.get('season', 'Kharif/Rabi'))
        water_req = str(row.get('water_requirement_level', 'MEDIUM'))
        description = str(row.get('description', 'High yielding agricultural crop.'))
    else:
        # Fallback default values if crop not explicitly found
        yield_per_acre = 15.0
        price_per_quintal = 3000.0
        cultivation_cost = 25000.0
        season = "Kharif / Rabi"
        water_req = "MEDIUM"
        description = "Standard farm crop with estimated regional parameters."
        
    revenue = yield_per_acre * price_per_quintal
    profit = revenue - cultivation_cost
    
    return {
        "crop": crop_name,
        "yield_quintal_per_acre": yield_per_acre,
        "price_per_quintal_inr": price_per_quintal,
        "cultivation_cost_per_acre_inr": cultivation_cost,
        "estimated_revenue_inr": revenue,
        "estimated_profit_inr": profit,
        "season": season,
        "water_requirement_level": water_req,
        "description": description,
        "formatted_revenue": f"₹{revenue:,.2f}",
        "formatted_cost": f"₹{cultivation_cost:,.2f}",
        "formatted_profit": f"₹{profit:,.2f}",
        "formatted_price": f"₹{price_per_quintal:,.2f}",
        "disclaimer": "Project economics data values, not live market spot prices."
    }
