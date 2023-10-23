from flask import Flask, render_template, request, send_file
import pandas as pd
from app.synlab import synpage1, synpage2, synpage3, synname
from app.enterosan import enteropage1, enteropage2, enteroname
from io import BytesIO

APP = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route('/upload', methods=['POST', 'GET'])
def upload_file():
    # Handle file1 input
    if 'file1' in request.files:
        file = request.files['file1']

        # Check if a file was provided
        if file.filename == '':
            return 'No file provided for Synlab'

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            file.save(file.filename)
            df = pd.concat([synname(file.filename), synpage1(file.filename), synpage2(file.filename),
                            synpage3(file.filename)],
                           axis=0)

            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            return send_file(output, as_attachment=True, download_name=f'Synlab_{synname(file.filename).columns[0]}.xlsx',
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    elif 'file2' in request.files:
        file = request.files['file2']
        # Check if a file was provided
        if file.filename == '':
            return 'No file provided for Enterosan'

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            file.save(file.filename)
            df = pd.concat([enteroname(file.filename), enteropage1(file.filename), enteropage2(file.filename)],
                           axis=0)

            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            return send_file(output, as_attachment=True, download_name=f'Enterosan_{enteroname(file.filename).columns[0]}.xlsx',
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    elif 'file3' in request.files:
        file = request.files['file3']
        # TODO: Implement processing for file3
        return 'File3 processing not yet implemented'

    else:
        return 'No valid file input provided'

    return render_template('upload2.html')


@APP.route('/')
def index():
    return render_template('upload2.html')


if __name__ == '__main__':
    APP.run(debug=True)
