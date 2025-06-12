from flask import Flask
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
from flask_cors import CORS

from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)  

api = Api(app, doc='/docs')

model = load_model('app/model/model.h5')
classes = ['Dry','Normal', 'Oily']

upload_parser = api.parser()
upload_parser.add_argument('image', location='files', type=FileStorage, required=True, help='Gambar wajah')

@api.route('/api/predict')
class Predict(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args.get('image')
        if file is None:
            return {'error': 'Tidak ada file dikirim'}, 400

        try:
            img = Image.open(BytesIO(file.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((224, 224))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            preds = model.predict(img)
            class_idx = int(np.argmax(preds))
            confidence = float(preds[0][class_idx])

            return {
                'predicted_class': classes[class_idx],
                'confidence': round(confidence * 100, 2)
            }, 200

        except Exception as e:
            return {'error': str(e)}, 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080)) 
    app.run(host='0.0.0.0', port=port, debug=False)
