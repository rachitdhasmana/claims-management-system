import os
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

# setting up flask app and in-memory db config through ORM
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 10  # 10 MB max upload size
db = SQLAlchemy(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# schema model for Claim
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    claim_type = db.Column(db.String(20), nullable=False)
    claim_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='new')
    attachment = db.Column(db.String(200))


# making sure that db is initialised when app is loaded
with app.app_context():
    db.create_all()


# render root page, creation of claims
@app.route('/')
def index():
    return render_template('index.html')


# render claims listing
@app.route('/claims')
def claims():
    return render_template('claims.html')


# fetch claims and return to javascript
@app.route('/api/claims', methods=['GET'])
def get_claims():
    claims = Claim.query.all()
    result = [{
        'id': claim.id,
        'title': claim.title,
        'description': claim.description,
        'claim_type': claim.claim_type,
        'claim_value': claim.claim_value,
        'status': claim.status,
        'attachment': claim.attachment
    } for claim in claims]
    return jsonify(result)


# add claim's record to the DB
@app.route('/api/claims', methods=['POST'])
def add_claim():
    data = request.form
    attachment = request.files.get('attachment')
    attachment_filename = None
    if attachment:
        attachment_filename = secure_filename(attachment.filename)
        attachment.save(
            os.path.join(app.config['UPLOAD_FOLDER'], attachment_filename)
        )
    new_claim = Claim(
        title=data['title'],
        description=data['description'],
        claim_type=data['claim_type'],
        claim_value=data['claim_value'],
        attachment=attachment_filename
    )
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({
        'id': new_claim.id,
        'title': new_claim.title,
        'description': new_claim.description,
        'claim_type': new_claim.claim_type,
        'claim_value': new_claim.claim_value,
        'status': new_claim.status,
        'attachment': new_claim.attachment
    })


# update claim's record in DB
@app.route('/api/claims/<int:id>', methods=['PUT'])
def update_claim(id):
    data = request.json
    claim = Claim.query.get(id)
    if not claim:
        return jsonify({'message': 'Claim not found'}), 404
    claim.title = data['title']
    claim.description = data['description']
    claim.claim_type = data['claim_type']
    claim.claim_value = data['claim_value']
    claim.status = data['status']
    db.session.commit()
    return jsonify({
        'id': claim.id,
        'title': claim.title,
        'description': claim.description,
        'claim_type': claim.claim_type,
        'claim_value': claim.claim_value,
        'status': claim.status,
        'attachment': claim.attachment
    })


# delete claim with specific id from DB
@app.route('/api/claims/<int:id>', methods=['DELETE'])
def delete_claim(id):
    claim = Claim.query.get(id)
    if not claim:
        return jsonify({'message': 'Claim not found'}), 404
    db.session.delete(claim)
    db.session.commit()
    return jsonify({'message': 'Claim deleted'})


# setting up SwaggerUI for API specification
@app.route("/swagger.json")
def swagger_json():
    with open('swagger.json') as f:
        return jsonify(json.load(f))


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Claims Management API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
