from flask import Flask, request, jsonify, send_file, url_for
from PIL import Image
import io
import logging
from logging.config import dictConfig
import json
from datetime import datetime
from flask_cors import CORS
import os
import uuid
import sqlite3
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()
UPLOAD_FILES_TO_S3 = os.getenv('UPLOAD_FILES_TO_S3', 'False').lower() == 'true'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

print(f"Uploading files to s3? {UPLOAD_FILES_TO_S3}")

app = Flask(__name__)
CORS(app)


# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'json_file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'json'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
})

# Ensure a directory for storing processed images
UPLOAD_FOLDER = 'processed_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE'] = 'images.db'

print(app.root_path)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/upload', methods=['POST'])
def upload_image():
    logger = logging.getLogger(__name__)
    
    if 'image' not in request.files:
        logger.error('No image file in request')
        return jsonify({'error': 'No image file in request'}), 400

    image_file = request.files['image']
    
    if image_file.filename == '':
        logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if image_file:
        try:
            # Open the image using Pillow
            img = Image.open(image_file)

            # Convert the image to black and white
            bw_img = img.convert('L')

            # Generate a unique filename
            new_filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)


            # Save the black and white image
            bw_img.save(filepath, 'PNG')
            
            if UPLOAD_FILES_TO_S3:
                print("Uploading image to s3")
                s3_client = boto3.client(service_name='s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

                try:
                    bucket = 'reactflaskfileuploadimages'
                    file_name = f"{app.root_path}/../../processed_images/{new_filename}"
                    object_name = 'random-image-object-name'
                    response = s3_client.upload_file(file_name, bucket, object_name)
                except Exception as e:
                    print(e)
                    logger.error(e)
                    # return False
                # return True
            else:
                print("Uploading image locally")

            
            
            conn = get_db_connection()
            conn.execute('INSERT INTO images (filename, filepath) VALUES (?, ?)', (new_filename, filepath))
            conn.commit()

            # Generate URL for the saved image
            image_url = url_for('get_image', filename=new_filename, _external=True)

            logger.info('Image processed successfully', extra={
                'original_file': image_file.filename,
                'processed_file': new_filename,
                'original_size': img.size,
                'original_mode': img.mode
            })

            # Return JSON response
            return jsonify({
                'message': 'Image processed successfully',
                'download_url': image_url
            }), 200

        except Exception as e:
            logger.error('Error processing image', extra={
                'original_file': image_file.filename,
                'error': str(e)
            })
            return jsonify({'error': 'Error processing image'}), 500

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    logger = logging.getLogger(__name__)
    logger.info(f'Finding image {filename}')
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/png', as_attachment=True, download_name='hello_world.png')

if __name__ == '__main__':
    app.run(debug=True)