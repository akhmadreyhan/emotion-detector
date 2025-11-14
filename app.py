import cv2
import base64
import time
import tensorflow as tf
import numpy as np
from keras.applications.mobilenet_v3 import preprocess_input as mobilenet_preprocess
from keras.applications.densenet import preprocess_input as densenet_preprocess
import os

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()

def index():
    return render_template('index.html')

@app.route('/input_page')
def input_page():
    return render_template('input-page.html')

@app.route('/capture_page')
def capture_page():
    return render_template('input-page.html')

@app.route('/submit', methods=['POST'])
def submit():
    model = 'MobileNetV3LargeFINETUNING-FIXX.keras'

    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, 'model', model)

    image_data = request.form['image']
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)

    # face detect
    cascade_path = os.path.join(base_path, 'model', 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(image, 1.3, 5)

    if len(faces) == 0:
        alert = 'No face detected'
        print(alert)
        return render_template('input-page.html', alert=alert)
    
    (x, y, w, h) = faces[0]
    image = image[y:y+h, x:x+w]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image = clahe.apply(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = cv2.resize(image, (100, 100))
    image = mobilenet_preprocess(image)
    image = np.expand_dims(image, axis=0)

    model = tf.keras.models.load_model(model_path, compile=False)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    start = time.time()
    prediction = model.predict(image)
    time.sleep(3)
    end = time.time()
    print(end-start)

    prediction = np.argmax(prediction, axis=1)

    if prediction == 0:
        class_name = 'angry'
        emoji_pict = 'assets/emoji/angry.png'
        color_id = 'angry'
        quote = "Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy."
        author = 'Roy T. Bennett'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    elif prediction == 1:
        class_name = 'neutral'
        emoji_pict = 'assets/emoji/neutral.png'
        color_id = 'neutral'
        quote = "Neutral men are the devils allies."
        author = 'Edwin Hubbel Chapin'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    elif prediction == 2:
        class_name = 'happy'
        emoji_pict = 'assets/emoji/happy.png'
        color_id = 'happy'
        quote = "You can never get enough of what you do not need to make you happy."
        author = 'Eric Hoffer'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    elif prediction == 3:
        class_name = 'sad'
        emoji_pict = 'assets/emoji/sad.png'
        color_id = 'sad'
        quote = "Things change. And friends leave. And life does not stop for anybody."
        author = 'Stephen Chbosky'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    elif prediction == 4:
        class_name = 'disgust'
        emoji_pict = 'assets/emoji/disgust.png'
        color_id = 'disgust'
        quote = "Every word that is spoken and sung here (the Cabaret Voltaire) represents at least this one thing: that this humiliating age has not succeeded in winning our respect."
        author = 'Hugo Ball'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    elif prediction == 5:
        class_name = 'fear'
        emoji_pict = 'assets/emoji/fear.png'
        color_id = 'fear'
        quote = "Don’t give into your fears, if you do, you won’t be able to talk to your heart."
        author = 'Paulo Coelho'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)
    else:
        class_name = 'suprised'
        emoji_pict = 'assets/emoji/suprised.png'
        color_id = 'suprised'
        quote = "Time changes everything except something within us which is always surprised by change."
        author = 'Thomas Hardy'
        print(class_name)
        return render_template('results.html', class_name=class_name, id=color_id, emoji=emoji_pict, quote=quote, author=author)

@app.route('/results')
def page():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=5000)