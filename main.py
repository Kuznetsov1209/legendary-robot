from flask import Flask, render_template, request, url_for, redirect  # Добавили redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Создаем папку для загрузок, если ее нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/load_photo', methods=['GET', 'POST'])
def upload_file():
    photo_url = None

    if request.method == 'POST':
        if 'photo' not in request.files:
            return render_template('load_photo.html', error='Файл не выбран')

        file = request.files['photo']

        if file.filename == '':
            return render_template('load_photo.html', error='Файл не выбран')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'img/{filename}')
            return render_template('load_photo.html', photo_url=photo_url)
        else:
            return render_template('load_photo.html', error='Недопустимый формат файла')

    return render_template('load_photo.html')


@app.route('/')
def redirect_to_load_photo():
    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)