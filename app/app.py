import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from tensorflow.keras.models import load_model
import cv2
import tensorflow as tf

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

IMG_SIZE = 32
class_name = ['adenocarcinoma', 'large.cell.carcinoma', 'squamous.cell.carcinoma', 'normal']


@app.route('/api/cancer_prostate/predict', methods=['POST'])
def predict_cancer_prostate():
	try:        
		# Log pour vérifier si une image est reçue
		print("Fichier reçu :", request.files)

		if 'image' not in request.files:
			return jsonify({'error': 'No image file provided'}), 400

		# Traitement de l'image
		image_file = request.files['image']
		image = np.frombuffer(image_file.read(), np.uint8)
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		image = cv2.resize(image,(IMG_SIZE,IMG_SIZE))
		image = image.reshape(1, IMG_SIZE, IMG_SIZE, 3)

		# Prétraitement
		image_processing = tf.cast(image, tf.float32)
		image_processing /= 255.0

		#print(image_processing.shape)

		model = load_model('../cancer_prostate_predicr_CNN.h5')

		predict = np.argmax(model.predict(image_processing), axis=1)[0]
		
		if predict == 0:
			y_predict = class_name[0]
		elif predict == 1:
			y_predict = class_name[1]
		elif predict == 2:
			y_predict = class_name[2]
		elif predict == 3:
			y_predict = class_name[3]

		if y_predict !='':
			print(y_predict)
			return jsonify({'cancer_prostate':y_predict}), 200
		else:
			return jsonify({'error': 'No license plate detected'}), 404

	except Exception as e:
		print(f"Erreur : {str(e)}")  # Log de l'exception
		return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
	