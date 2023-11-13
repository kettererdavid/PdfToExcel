from flask import Flask, render_template, request, send_file
import pandas as pd
from app.synlab import synpage1, synpage2, synpage3, synname
from app.enterosan import enteropage1, enteropage2, enteroname
from app.censa import censa1
from app.microtrace import micro1, micro2, microname
from app.nutriplus import nutri1
from io import BytesIO


APP = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf'}

testperson = pd.DataFrame(columns=['Testperson 1'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route('/upload', methods=['POST', 'GET'])
def upload_file():
    # Check for file1
    file1 = request.files.get('file1', None)
    if file1 and file1.filename and allowed_file(file1.filename):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        file_stream1 = BytesIO(file1.read())
        df1 = pd.concat([synname(file_stream1), synpage1(file_stream1), synpage2(file_stream1),
                         synpage3(file_stream1)], axis=0)
        df1.to_excel(writer, sheet_name='Synlab', index=False)
        writer.close()
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f'Synlab{synname(file_stream1).columns[0]}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Check for file2
    file2 = request.files.get('file2', None)
    if file2 and file2.filename and allowed_file(file2.filename):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        file_stream2 = BytesIO(file2.read())
        df2 = pd.concat([enteroname(file_stream2), enteropage1(file_stream2), enteropage2(file_stream2)],
                        axis=0)
        df2.to_excel(writer, sheet_name='Enterosan', index=False)
        writer.close()
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f'Enterosan{enteroname(file_stream2).columns[0]}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Check for file3
    file3 = request.files.get('file3', None)
    if file3 and file3.filename and allowed_file(file3.filename):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        file_stream3 = BytesIO(file3.read())
        df3 = pd.concat([testperson, censa1(file_stream3)], axis=0)
        df3.to_excel(writer, sheet_name='Censa', index=False)
        writer.close()
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='Censa.xlsx',
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Check for file4
    file4 = request.files.get('file4', None)
    if file4 and file4.filename and allowed_file(file4.filename):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        file_stream4 = BytesIO(file4.read())
        df4 = pd.concat([testperson, micro1(file_stream4), micro2(file_stream4)],
                        axis=0)
        df4.to_excel(writer, sheet_name='Microtrace', index=False)
        writer.close()
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f'Microtrace {microname(file_stream4)}.xlsx',
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Check for file6
    file6 = request.files.get('file6', None)
    if file6 and file6.filename and allowed_file(file6.filename):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        file_stream6 = BytesIO(file6.read())
        df6 = pd.concat([testperson, nutri1(file_stream6)], axis=0)
        df6.to_excel(writer, sheet_name='Nutriplus', index=False)
        writer.close()
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f'Nutriplus.xlsx',
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return render_template('6uploads.html')


@APP.route('/')
def index():
    return render_template('6uploads.html')


if __name__ == '__main__':
    APP.run(debug=True)
