import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'minha_chave_super_secreta'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) 
              if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Evita duplicatas — bloqueia se já existir
        if not os.path.exists(save_path):
            file.save(save_path)
            flash('Imagem enviada com sucesso!')
        else:
            flash(f"O arquivo {filename} já existe. Upload ignorado.")

    return redirect(url_for('home'))

    
    return redirect(url_for('home'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Imagem "{filename}" deletada com sucesso.')
    else:
        flash('Imagem não encontrada.')
    return redirect(url_for('home'))
if __name__ == '__main__':
    
    app.run(debug=True)


