from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import fitz

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = "static/files/"

# for py-mu pdf
ALLOWED_EXTENSIONS = {'pdf', 'xps', 'oxps', 'epub', 'fb2', 'mobi', 'pdb'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    text = upload_file()
    return render_template('index.html', text=text)


def read_pdf(file_path):
    # Open the PDF file
    doc = fitz.open(file_path)

    # Read the text
    text = ""
    for page in doc:
        text += page.get_text()

    return text


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # if user does not select file
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Call the read_pdf function
            text = read_pdf(file_path)

            return text  # return the text to the user


if __name__ == '__main__':
    app.run(debug=True)
