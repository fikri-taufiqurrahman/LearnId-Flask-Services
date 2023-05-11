from application import app
from flask import redirect, render_template, url_for, request,session
from application import utils
import secrets
import os
from application.forms import MyForm
import cv2
from flask import jsonify
from gtts import gTTS
import pytesseract
import numpy as np



@app.route('/ocr', methods=['POST'])
def ocr():

    sentence= ""
    f = request.files.get("file")
    filename, extension = f.filename.split(".")
    generated_filename = secrets.token_hex(20)+ f".{extension}"

    file_location = os.path.join(app.config["UPLOADED_PATH"], generated_filename)
    f.save(file_location) 

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    img = cv2.imread(file_location)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    # Perform image compression
    compression_quality = 90
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, compression_quality]
    compressed_img_location = os.path.join(app.config["UPLOADED_PATH"], "compressed_image.jpg")
    cv2.imwrite(compressed_img_location, img, compression_params)
    img = cv2.imread(compressed_img_location)
    
    boxes = pytesseract.image_to_data(img)
    for i, box in enumerate(boxes.splitlines()):
        if i ==0:
            continue
        box = box.split()
        if len(box) == 12:
            sentence += box[11]+" "
    session["sentence"] = sentence
    response_data = {
        "sentence": sentence
    }

    return jsonify(response_data)


@app.route("/translate", methods=["POST"])
def translate_with_audio():
    data = request.get_json()
    text_data = data['text']
    translate_to = data["translate_to"]
    generated_audio_filename = secrets.token_hex(30) + ".mp4"
    translated_text = utils.translate_text(text_data, translate_to)
    
    tts = gTTS(translated_text, lang=translate_to)
    file_location = os.path.join(app.config["AUDIO_FILE_UPLOAD"], generated_audio_filename)
    
    tts.save(file_location)
    
    response_data = {
        "translated_text": translated_text,
        "audio_path": "http://127.0.0.1:8080/static/audio_files/"+generated_audio_filename
    }
    
    return jsonify(response_data)
