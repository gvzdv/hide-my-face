from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename
import face_recognition
import replicate
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def detect_faces(image_path):
    img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)
    return len(face_locations) > 0


def replace_face(image, swap):
    client = replicate.Client(api_token=REPLICATE_API_KEY)
    output = client.run(
        "yan-ops/face_swap:ad6bd82aaff9ffabee90890c7bfbb249e4433b7a9f0ebf27b39f927edbd9b129",
        input={"target_image": open(image, "rb"), "source_image": open(swap, "rb")},
    )
    response = output['image']
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if detect_faces(filepath):
            return jsonify({'face_detected': True, 'image_url': filepath})

        return jsonify({'face_detected': False, 'image_url': filepath})


@app.route('/replace', methods=['POST'])
def replace_image():
    data = request.get_json()
    image_url = data['image_url']
    swap_image = os.path.join(app.config['UPLOAD_FOLDER'], 'random_3.png')
    replaced_image = replace_face(image_url, swap_image)
    return jsonify({'image_url': replaced_image})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)