# api/app.py
from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import os
import warnings

# Suppression des avertissements de version sklearn
warnings.filterwarnings('ignore', category=UserWarning)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Chargement du modèle
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/model.pkl')
try:
    model = joblib.load(MODEL_PATH)
    print(f"Modele charge depuis {MODEL_PATH}")
except Exception as e:
    print(f"Erreur chargement modele: {e}")
    model = None

FEATURE_NAMES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
CLASS_NAMES = ['setosa', 'versicolor', 'virginica']

@app.route('/')
def index():
    """Page d'accueil avec l'interface web"""
    return render_template('index.html')

@app.route('/api')
def api_docs():
    """Documentation de l'API"""
    return jsonify({
        'message': 'API de classification Iris',
        'endpoints': {
            'GET /': 'Interface web',
            'POST /predict': 'Prediction',
            'GET /health': 'Statut du service',
            'GET /api': 'Documentation API'
        },
        'features': FEATURE_NAMES,
        'classes': CLASS_NAMES,
        'example_request': {
            'sepal_length': 5.1,
            'sepal_width': 3.5,
            'petal_length': 1.4,
            'petal_width': 0.2
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint de prediction"""
    if model is None:
        return jsonify({'error': 'Modele non disponible'}), 500
    
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'Donnees JSON requises'}), 400
        
        missing = [f for f in FEATURE_NAMES if f not in data]
        if missing:
            return jsonify({'error': f'Features manquantes: {missing}'}), 400
        
        # Conversion
        features = [float(data[f]) for f in FEATURE_NAMES]
        input_array = np.array(features).reshape(1, -1)
        
        # Prediction
        prediction = model.predict(input_array)
        proba = model.predict_proba(input_array)
        
        # Formatage de la reponse
        class_idx = int(prediction[0])
        response = {
            'prediction': CLASS_NAMES[class_idx],
            'class_index': class_idx,
            'probabilities': {
                CLASS_NAMES[i]: float(prob) 
                for i, prob in enumerate(proba[0])
            },
            'features': data
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': 'Valeurs numeriques requises'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de sante"""
    status = 'healthy' if model is not None else 'unhealthy'
    return jsonify({
        'status': status,
        'model_loaded': model is not None,
        'service': 'Iris Classification API'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)