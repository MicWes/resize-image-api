import os

from flask import Flask, render_template, send_file, request
from PIL import Image

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def hello():
    message = "Resize Image API is running!"

    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/resize', methods=['POST'])
def resize():
    image = request.files['image']
    
    if image:
        #resizing
        img = Image.open(image)
        size = request.args.get("size")
        if size:
            new_img = img.resize((int(size), int(size)))
            new_img.save('image_'+ str(size) +'.jpg')
            return send_file('image_'+ str(size) +'.jpg', mimetype='image/jpg'), 200
        else:
            new_img = img.resize((384, 384))
            new_img.save('image_384.jpg')
            return send_file('image_384.jpg', mimetype='image/jpg'), 200
    else:
        return 'Error: image not found.', 500

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
