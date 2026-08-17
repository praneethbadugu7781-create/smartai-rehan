import numpy as np
import pandas as pd
import os

# Define realistic distributions for 22 crops (N, P, K, temp, humidity, ph, rainfall)
crop_profiles = {
    'rice':        {'N': (80, 120),  'P': (35, 60),  'K': (35, 45),  'temp': (20, 27), 'hum': (80, 90), 'ph': (5.0, 7.0), 'rain': (180, 300)},
    'maize':       {'N': (60, 100),  'P': (35, 60),  'K': (15, 25),  'temp': (18, 27), 'hum': (55, 75), 'ph': (5.5, 7.0), 'rain': (60, 110)},
    'chickpea':    {'N': (20, 60),   'P': (55, 80),  'K': (75, 85),  'temp': (17, 21), 'hum': (14, 20), 'ph': (6.0, 8.8), 'rain': (65, 95)},
    'kidneybeans': {'N': (15, 40),   'P': (55, 80),  'K': (15, 25),  'temp': (15, 24), 'hum': (18, 25), 'ph': (5.5, 6.0), 'rain': (60, 150)},
    'pigeonpeas':  {'N': (15, 40),   'P': (55, 80),  'K': (15, 25),  'temp': (27, 37), 'hum': (30, 65), 'ph': (4.5, 7.5), 'rain': (90, 200)},
    'mothbeans':   {'N': (15, 40),   'P': (35, 60),  'K': (15, 25),  'temp': (24, 32), 'hum': (40, 65), 'ph': (3.5, 10.0),'rain': (30, 75)},
    'mungbean':    {'N': (15, 40),   'P': (35, 60),  'K': (15, 25),  'temp': (27, 30), 'hum': (80, 90), 'ph': (6.2, 7.2), 'rain': (35, 60)},
    'blackgram':   {'N': (30, 60),   'P': (55, 80),  'K': (15, 25),  'temp': (25, 35), 'hum': (60, 70), 'ph': (6.5, 7.8), 'rain': (60, 75)},
    'lentil':      {'N': (15, 40),   'P': (55, 80),  'K': (15, 25),  'temp': (18, 30), 'hum': (60, 70), 'ph': (5.9, 7.0), 'rain': (35, 55)},
    'pomegranate': {'N': (15, 40),   'P': (10, 30),  'K': (35, 45),  'temp': (18, 25), 'hum': (85, 95), 'ph': (5.5, 7.2), 'rain': (100, 112)},
    'banana':      {'N': (90, 120),  'P': (70, 95),  'K': (45, 55),  'temp': (25, 30), 'hum': (75, 85), 'ph': (5.5, 6.5), 'rain': (90, 120)},
    'mango':       {'N': (15, 40),   'P': (15, 40),  'K': (25, 35),  'temp': (27, 36), 'hum': (45, 55), 'ph': (4.5, 7.0), 'rain': (85, 105)},
    'grapes':      {'N': (15, 40),   'P': (120, 145),'K': (195, 205),'temp': (8, 41),  'hum': (80, 85), 'ph': (5.5, 6.5), 'rain': (65, 75)},
    'watermelon':  {'N': (80, 120),  'P': (10, 30),  'K': (45, 55),  'temp': (24, 27), 'hum': (80, 90), 'ph': (6.0, 7.0), 'rain': (40, 60)},
    'muskmelon':   {'N': (80, 120),  'P': (10, 30),  'K': (45, 55),  'temp': (27, 29), 'hum': (90, 95), 'ph': (6.0, 6.8), 'rain': (20, 30)},
    'apple':       {'N': (0, 40),    'P': (120, 145),'K': (195, 205),'temp': (21, 24), 'hum': (90, 95), 'ph': (5.5, 6.5), 'rain': (100, 125)},
    'orange':      {'N': (15, 40),   'P': (10, 30),  'K': (5, 15),   'temp': (13, 35), 'hum': (90, 95), 'ph': (6.0, 8.0), 'rain': (100, 120)},
    'papaya':      {'N': (35, 70),   'P': (45, 70),  'K': (45, 55),  'temp': (23, 44), 'hum': (90, 95), 'ph': (6.5, 7.0), 'rain': (40, 250)},
    'coconut':     {'N': (15, 40),   'P': (10, 30),  'K': (25, 35),  'temp': (25, 28), 'hum': (90, 99), 'ph': (5.5, 6.5), 'rain': (130, 220)},
    'cotton':      {'N': (110, 140), 'P': (35, 60),  'K': (15, 25),  'temp': (22, 26), 'hum': (75, 85), 'ph': (6.0, 8.0), 'rain': (60, 90)},
    'jute':        {'N': (60, 90),   'P': (35, 60),  'K': (35, 45),  'temp': (23, 26), 'hum': (70, 90), 'ph': (6.0, 7.5), 'rain': (150, 200)},
    'coffee':      {'N': (80, 120),  'P': (15, 35),  'K': (25, 35),  'temp': (23, 28), 'hum': (50, 70), 'ph': (6.0, 7.5), 'rain': (115, 200)},
}

np.random.seed(42)
records = []
samples_per_crop = 100

for crop, bounds in crop_profiles.items():
    for _ in range(samples_per_crop):
        n = float(np.round(np.random.uniform(bounds['N'][0], bounds['N'][1]) + np.random.normal(0, 2), 1))
        p = float(np.round(np.random.uniform(bounds['P'][0], bounds['P'][1]) + np.random.normal(0, 2), 1))
        k = float(np.round(np.random.uniform(bounds['K'][0], bounds['K'][1]) + np.random.normal(0, 2), 1))
        temp = float(np.round(np.random.uniform(bounds['temp'][0], bounds['temp'][1]) + np.random.normal(0, 0.5), 1))
        hum = float(np.round(np.random.uniform(bounds['hum'][0], bounds['hum'][1]) + np.random.normal(0, 1), 1))
        ph = float(np.round(np.clip(np.random.uniform(bounds['ph'][0], bounds['ph'][1]) + np.random.normal(0, 0.1), 3.5, 9.5), 1))
        rain = float(np.round(np.random.uniform(bounds['rain'][0], bounds['rain'][1]) + np.random.normal(0, 5), 1))
        
        # Clip to sensible positive values
        n = max(0.0, n)
        p = max(0.0, p)
        k = max(0.0, k)
        temp = max(0.0, temp)
        hum = max(0.0, min(100.0, hum))
        rain = max(0.0, rain)
        
        records.append({
            'N': n,
            'P': p,
            'K': k,
            'temperature': temp,
            'humidity': hum,
            'ph': ph,
            'rainfall': rain,
            'label': crop
        })

df = pd.DataFrame(records)
os.makedirs('dataset', exist_ok=True)
df.to_csv('dataset/crop_data.csv', index=False)
print(f"Dataset generated successfully with {len(df)} records for {len(crop_profiles)} crops.")
