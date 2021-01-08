from werkzeug.utils import secure_filename, validate_arguments
import requests
from flask import Flask,request,redirect
from flask_restful import Api, Resource
from requests.models import Response
import os
app = Flask(__name__)
api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg','docx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
class getextension(Resource):
    def post(self):
        if 'file' not in request.files:
            return ({
                "status":False,
                "fileuploade":False

            })
        file = request.files['file']    
        if file.filename == '':
            return ({
                "status":False,
                "fileuploade":"no file selected"
                
            })
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print(jsonify('uploaded'))
            return ({
                "extension":os.path.splitext(filename)[1],
                })  
        else:
            return({
                "allowedextensionsare":"pdf, png, jpg, jpeg"
            })     


api.add_resource(getextension, "/extension")

if __name__ == "__main__":
    app.run(debug=True)