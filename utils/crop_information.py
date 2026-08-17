def get_crop_info(crop_name):
    """
    Returns agronomic profile information for a specified crop.
    """
    crop_name = crop_name.lower().strip()
    
    crop_profiles = {
        'rice': {
            'display_name': 'Rice (Paddy)',
            'season': 'Kharif (Monsoon)',
            'water_requirement': 'HIGH',
            'ideal_ph': '5.0 - 7.0',
            'ideal_temp': '20°C - 30°C',
            'growth_duration': '120 - 150 days',
            'category': 'Cereal Grain',
            'icon': '🌾'
        },
        'maize': {
            'display_name': 'Maize (Corn)',
            'season': 'Kharif / Rabi',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 7.5',
            'ideal_temp': '18°C - 27°C',
            'growth_duration': '90 - 120 days',
            'category': 'Cereal / Fodder',
            'icon': '🌽'
        },
        'chickpea': {
            'display_name': 'Chickpea (Gram)',
            'season': 'Rabi (Winter)',
            'water_requirement': 'LOW',
            'ideal_ph': '6.0 - 8.0',
            'ideal_temp': '15°C - 25°C',
            'growth_duration': '90 - 110 days',
            'category': 'Pulse / Legume',
            'icon': '🌱'
        },
        'kidneybeans': {
            'display_name': 'Kidney Beans (Rajma)',
            'season': 'Kharif / Rabi',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 6.5',
            'ideal_temp': '15°C - 24°C',
            'growth_duration': '100 - 120 days',
            'category': 'Pulse / Legume',
            'icon': '🫘'
        },
        'pigeonpeas': {
            'display_name': 'Pigeon Peas (Arhar / Tur)',
            'season': 'Kharif',
            'water_requirement': 'LOW',
            'ideal_ph': '5.0 - 7.5',
            'ideal_temp': '25°C - 35°C',
            'growth_duration': '150 - 180 days',
            'category': 'Pulse / Legume',
            'icon': '🌱'
        },
        'mothbeans': {
            'display_name': 'Moth Beans',
            'season': 'Kharif',
            'water_requirement': 'LOW',
            'ideal_ph': '5.0 - 8.5',
            'ideal_temp': '24°C - 34°C',
            'growth_duration': '75 - 90 days',
            'category': 'Pulse / Legume',
            'icon': '🌱'
        },
        'mungbean': {
            'display_name': 'Mung Bean (Green Gram)',
            'season': 'Kharif / Summer',
            'water_requirement': 'LOW',
            'ideal_ph': '6.2 - 7.2',
            'ideal_temp': '25°C - 35°C',
            'growth_duration': '60 - 75 days',
            'category': 'Pulse / Legume',
            'icon': '🫘'
        },
        'blackgram': {
            'display_name': 'Black Gram (Urad)',
            'season': 'Kharif / Rabi',
            'water_requirement': 'LOW',
            'ideal_ph': '6.5 - 7.8',
            'ideal_temp': '25°C - 35°C',
            'growth_duration': '80 - 95 days',
            'category': 'Pulse / Legume',
            'icon': '🫘'
        },
        'lentil': {
            'display_name': 'Lentil (Masoor)',
            'season': 'Rabi (Winter)',
            'water_requirement': 'LOW',
            'ideal_ph': '5.9 - 7.0',
            'ideal_temp': '18°C - 30°C',
            'growth_duration': '110 - 130 days',
            'category': 'Pulse / Legume',
            'icon': '🫘'
        },
        'pomegranate': {
            'display_name': 'Pomegranate',
            'season': 'Annual / Perennial',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 7.2',
            'ideal_temp': '18°C - 30°C',
            'growth_duration': 'Commercial orchard',
            'category': 'Horticulture Fruit',
            'icon': '🍎'
        },
        'banana': {
            'display_name': 'Banana',
            'season': 'Perennial',
            'water_requirement': 'HIGH',
            'ideal_ph': '5.5 - 6.5',
            'ideal_temp': '25°C - 32°C',
            'growth_duration': '11 - 13 months',
            'category': 'Horticulture Fruit',
            'icon': '🍌'
        },
        'mango': {
            'display_name': 'Mango',
            'season': 'Perennial',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 7.5',
            'ideal_temp': '24°C - 35°C',
            'growth_duration': 'Perennial Tree',
            'category': 'Horticulture Fruit',
            'icon': '🥭'
        },
        'grapes': {
            'display_name': 'Grapes',
            'season': 'Perennial',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 6.5',
            'ideal_temp': '15°C - 35°C',
            'growth_duration': 'Perennial Vine',
            'category': 'Horticulture Fruit',
            'icon': '🍇'
        },
        'watermelon': {
            'display_name': 'Watermelon',
            'season': 'Summer',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '6.0 - 7.0',
            'ideal_temp': '24°C - 30°C',
            'growth_duration': '80 - 100 days',
            'category': 'Melon Fruit',
            'icon': '🍉'
        },
        'muskmelon': {
            'display_name': 'Muskmelon',
            'season': 'Summer',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '6.0 - 6.8',
            'ideal_temp': '25°C - 32°C',
            'growth_duration': '75 - 90 days',
            'category': 'Melon Fruit',
            'icon': '🍈'
        },
        'apple': {
            'display_name': 'Apple',
            'season': 'Perennial (Hilly)',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '5.5 - 6.5',
            'ideal_temp': '20°C - 25°C',
            'growth_duration': 'Perennial Orchard',
            'category': 'Temperate Fruit',
            'icon': '🍎'
        },
        'orange': {
            'display_name': 'Orange (Citrus)',
            'season': 'Perennial',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '6.0 - 7.5',
            'ideal_temp': '15°C - 35°C',
            'growth_duration': 'Perennial Citrus',
            'category': 'Horticulture Fruit',
            'icon': '🍊'
        },
        'papaya': {
            'display_name': 'Papaya',
            'season': 'Perennial',
            'water_requirement': 'HIGH',
            'ideal_ph': '6.5 - 7.0',
            'ideal_temp': '22°C - 35°C',
            'growth_duration': '9 - 10 months',
            'category': 'Horticulture Fruit',
            'icon': '🥭'
        },
        'coconut': {
            'display_name': 'Coconut',
            'season': 'Perennial (Coastal)',
            'water_requirement': 'HIGH',
            'ideal_ph': '5.2 - 8.0',
            'ideal_temp': '25°C - 32°C',
            'growth_duration': 'Perennial Plantation',
            'category': 'Plantation Crop',
            'icon': '🥥'
        },
        'cotton': {
            'display_name': 'Cotton',
            'season': 'Kharif',
            'water_requirement': 'MEDIUM',
            'ideal_ph': '6.0 - 8.0',
            'ideal_temp': '21°C - 30°C',
            'growth_duration': '150 - 180 days',
            'category': 'Cash Commercial Fibre',
            'icon': '☁️'
        },
        'jute': {
            'display_name': 'Jute',
            'season': 'Kharif',
            'water_requirement': 'HIGH',
            'ideal_ph': '6.0 - 7.5',
            'ideal_temp': '24°C - 35°C',
            'growth_duration': '120 - 150 days',
            'category': 'Commercial Fibre',
            'icon': '🌾'
        },
        'coffee': {
            'display_name': 'Coffee',
            'season': 'Perennial (Hills)',
            'water_requirement': 'HIGH',
            'ideal_ph': '6.0 - 6.5',
            'ideal_temp': '18°C - 28°C',
            'growth_duration': 'Perennial Plantation',
            'category': 'Plantation Beverage',
            'icon': '☕'
        }
    }
    
    default_profile = {
        'display_name': crop_name.capitalize(),
        'season': 'Kharif / Rabi',
        'water_requirement': 'MEDIUM',
        'ideal_ph': '6.0 - 7.0',
        'ideal_temp': '20°C - 30°C',
        'growth_duration': '90 - 120 days',
        'category': 'Agricultural Crop',
        'icon': '🌱'
    }
    
    return crop_profiles.get(crop_name, default_profile)
