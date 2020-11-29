import os

from flask import Blueprint, request, current_app as app
from werkzeug.utils import secure_filename
from .db_methods import get_user_id
from .db import get_engine


bp = Blueprint('upload', __name__, url_prefix='/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@bp.route('', methods=('POST',))
def upload():
    content = request.form
    user_name = content['user_name']
    app.logger.info(f'user_name - {user_name}')

    engine = get_engine()
    user_id = get_user_id(engine, user_name)
    if user_id is None:
        return {'message': 'User does not exist'}, 400

    if request.method == 'POST':
        # check if less than 5 pictures

        if 'file' not in request.files:
            return {'message': 'No file field specified'}, 400
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if not allowed_file(file.filename):
            return {'message': 'Not allowed file extension'}, 400

        filename = secure_filename(file.filename)
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_name)

        os.makedirs(user_dir, exist_ok=True)
        file.save(os.path.join(user_dir, filename))
        return {'filename': f'{user_name}/{filename}'}, 201
