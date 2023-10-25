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
    # Create an in-memory Excel writer
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Check for file1
    file1 = request.files.get('file1', None)
    if file1 and file1.filename and allowed_file(file1.filename):
        file_stream1 = BytesIO(file1.read())
        df1 = pd.concat([synname(file_stream1), synpage1(file_stream1), synpage2(file_stream1),
                         synpage3(file_stream1)], axis=0)
        df1.to_excel(writer, sheet_name='Synlab', index=False)

    # Check for file2
    file2 = request.files.get('file2', None)
    if file2 and file2.filename and allowed_file(file2.filename):
        file_stream2 = BytesIO(file2.read())
        df2 = pd.concat([enteroname(file_stream2), enteropage1(file_stream2), enteropage2(file_stream2)],
                        axis=0)
        df2.to_excel(writer, sheet_name='Enterosan', index=False)

    # Save and set the position to beginning
    writer.close()
    output.seek(0)

    # Send the file for download
    return send_file(output, as_attachment=True, download_name='combined_report.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# def upload_file():
#     # Handle file1 input
#     if 'file1' in request.files:
#         file = request.files['file1']
#
#         # Check if a file was provided
#         if file.filename == '':
#             return 'No file provided for Synlab'
#
#         # Check if the file is allowed
#         if file and allowed_file(file.filename):
#             file.save(file.filename)
#             df = pd.concat([synname(file.filename), synpage1(file.filename), synpage2(file.filename),
#                             synpage3(file.filename)],
#                            axis=0)
#
#             output = BytesIO()
#             df.to_excel(output, index=False)
#             output.seek(0)
#
#             return send_file(output, as_attachment=True, download_name=f'Synlab_{synname(file.filename).columns[0]}.xlsx',
#                              mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#
#     elif 'file2' in request.files:
#         file = request.files['file2']
#         # Check if a file was provided
#         if file.filename == '':
#             return 'No file provided for Enterosan'
#
#         # Check if the file is allowed
#         if file and allowed_file(file.filename):
#             file.save(file.filename)
#             df = pd.concat([enteroname(file.filename), enteropage1(file.filename), enteropage2(file.filename)],
#                            axis=0)
#
#             output = BytesIO()
#             df.to_excel(output, index=False)
#             output.seek(0)
#
#             return send_file(output, as_attachment=True, download_name=f'Enterosan_{enteroname(file.filename).columns[0]}.xlsx',
#                              mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#
#     elif 'file3' in request.files:
#         file = request.files['file3']
#         # TODO: Implement processing for file3
#         return 'File3 processing not yet implemented'
#
#     else:
#         return 'No valid file input provided'
#
#     return render_template('upload2.html')


@APP.route('/')
def index():
    return render_template('upload_combined.html')


if __name__ == '__main__':
    APP.run(debug=True)
