from flask import Flask, request, jsonify, send_file
import os
import tempfile
import time
from gradio_client import Client, handle_file

app = Flask(__name__)
client = Client("levihsu/OOTDiffusion")

app.config['TEMP_DIR'] = tempfile.mkdtemp()

@app.route('/process', methods=['POST'])
def process():
    vton_url = request.json.get('vton_img')
    garm_url = request.json.get('garm_img')

    if vton_url and garm_url:
        result = client.predict(
            vton_img=handle_file(vton_url),
            garm_img=handle_file(garm_url),
            n_samples=1,
            n_steps=20,
            image_scale=2,
            seed=-1,
            api_name="/process_hd"
        )

        if result:
            image_path = result[0]['image']
            temp_filename = os.path.join(app.config['TEMP_DIR'], 'result_image_' + str(int(time.time())) + '.jpg')
            os.rename(image_path, temp_filename)

            image_url = f"http://localhost:8080/images/{os.path.basename(temp_filename)}"
            
            return jsonify({'image_url': image_url})
        else:
            return jsonify({'error': 'Image processing failed'}), 500
    else:
        return jsonify({'error': 'Missing image URLs'}), 400

@app.route('/images/<filename>')
def get_image(filename):
    return send_file(os.path.join(app.config['TEMP_DIR'], filename), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
