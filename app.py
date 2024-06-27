import json
import os
import bleach

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager,
                                create_access_token,
                                jwt_required,
                                get_jwt_identity)
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

# setting up flask app and in-memory db config through ORM
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 10  # 10 MB max upload size

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

auth_bp = Blueprint('auth', __name__)
claims_bp = Blueprint('claims', __name__)
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Claims Management API"
    }
)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# schema model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # admin or user


# schema model for Claim
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='new', nullable=False)
    attachment = db.Column(db.String(255))

    def to_dict(self, role=''):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'value': self.value,
            'status': self.status,
            'attachment': self.attachment,
            'allow_status_edit': True if role == 'admin' else False
        }


def sanitize_input(input):
    if input:
        return bleach.clean(input)

    return input


# render root page, registration of Users
@app.route('/')
def register():
    return render_template('register.html')


# render login page
@app.route('/login')
def login():
    return render_template('login.html')


# render claims listing
@app.route('/claims')
def claims():
    return render_template('claims.html')


# render all claim page
@app.route('/add')
def index():
    return render_template('add_claim.html')


# handler for register user post call
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = \
        bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        username=sanitize_input(data['username']),
        password=hashed_password,
        role=sanitize_input(data['role'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


# handler for login user post call
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity={
                'username': user.username,
                'role': user.role
            }
        )
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401


# handler for fetching the claims get call
@claims_bp.route('/api/claims', methods=['GET'])
@jwt_required()
def get_claims():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user.role == 'admin':
        claims = Claim.query.all()
    else:
        claims = Claim.query.filter_by(user_id=user.id).all()
    return jsonify([claim.to_dict(user.role) for claim in claims])


# handler for adding the claim post call
@claims_bp.route('/api/claims', methods=['POST'])
@jwt_required()
def add_claim():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    data = request.form
    attachment = request.files.get('attachment')
    attachment_filename = None
    if attachment:
        attachment_filename = secure_filename(attachment.filename)
        attachment.save(
            os.path.join(app.config['UPLOAD_FOLDER'], attachment_filename)
        )
    new_claim = Claim(user_id=user.id,
                      title=sanitize_input(data['title']),
                      description=sanitize_input(data['description']),
                      type=sanitize_input(data['type']),
                      value=sanitize_input(data['value']),
                      attachment=attachment_filename)
    db.session.add(new_claim)
    db.session.commit()
    return jsonify(new_claim.to_dict(user.role)), 201


# handler for updating the claim put call
@claims_bp.route('/api/claims/<int:claim_id>', methods=['PUT'])
@jwt_required()
def update_claim(claim_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    claim = Claim.query.get_or_404(claim_id)
    if user.role != 'admin' and claim.user_id != user.id:
        return jsonify({'message': 'Permission denied'}), 403
    if not claim:
        return jsonify({'message': 'Claim not found'}), 404
    data = request.json
    claim.title = sanitize_input(data.get('title', claim.title))
    claim.description = sanitize_input(data.get('description', claim.description))
    claim.type = sanitize_input(data.get('type', claim.type))
    claim.value = sanitize_input(str(data.get('value', claim.value)))
    claim.status = sanitize_input(data.get('status', claim.status))
    claim.attachment = sanitize_input(data.get('attachment', claim.attachment))
    db.session.commit()
    return jsonify(claim.to_dict(user.role)), 200


# handler for deleting the claim delete call
@claims_bp.route('/api/claims/<int:claim_id>', methods=['DELETE'])
@jwt_required()
def delete_claim(claim_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    claim = Claim.query.get_or_404(claim_id)
    if user.role != 'admin' and claim.user_id != user.id:
        return jsonify({'message': 'Permission denied'}), 403
    if not claim:
        return jsonify({'message': 'Claim not found'}), 404
    db.session.delete(claim)
    db.session.commit()
    return jsonify({'message': 'Claim deleted'}), 200


# setting up SwaggerUI for API specification
@app.route("/swagger.json")
def swagger_json():
    with open('swagger.json') as f:
        return jsonify(json.load(f))


# registering blueprint within app
app.register_blueprint(auth_bp)
app.register_blueprint(claims_bp)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

# initialising the db when app is loaded
with app.app_context():
    db.create_all()


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


if __name__ == '__main__':
    app.run(debug=True)
