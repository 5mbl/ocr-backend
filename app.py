from flask import Flask, request, jsonify
try:
    from PIL import Image
except ImportError:
    import Image

from io import BytesIO

import pytesseract


app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/extractImg2Text', methods=['POST'])
def index():
    file = request.files.get('file')
    
    if file is None or file.filename == '':
        return jsonify({"error": "No file uploaded"}), 400
    
    image = Image.open(file)
    extracted_text = pytesseract.image_to_string(image)
    
    return jsonify({"extracted_text": extracted_text}), 200

@app.route('/')
def index():
    return ("Home - API DIRECTORY")

