from flask import Flask, request, send_file
from pdf2image import convert_from_bytes
import io, zipfile

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    images = convert_from_bytes(file.read(), dpi=100, fmt='jpeg')

    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as zipf:
        for i, img in enumerate(images):
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            zipf.writestr(f'page_{i+1}.png', img_bytes.getvalue())

    output.seek(0)
    return send_file(output, mimetype='application/zip', as_attachment=True, download_name='pages.zip')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
