from flask import send_from_directory
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from os import makedirs
from os.path import join, exists
from mltd_card_match import card_match

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

if not exists('upload'):
        makedirs('upload')

app = Flask(__name__, static_url_path='/icons', static_folder='icons')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main_page():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = (secure_filename(f.filename))
            f.save(join(app.config['UPLOAD_FOLDER'], filename))
            report = card_match(join(app.config['UPLOAD_FOLDER'], filename))
            print(report)
            return send_from_directory('report', report)
    else:
        return redirect('/')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
