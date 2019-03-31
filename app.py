#!flask/bin/python
import os, re
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from sendgrid import send_mail

#-------------- Authorization --------------#
FLASK_USER = os.environ.get("FLASK_USER", default=None)
FLASK_PASS = os.environ.get("FLASK_PASS", default=None)
if not FLASK_PASS or not FLASK_USER:
    raise ValueError("Need to set credentials for Flask application (FLASK_USER and FLASK_PASS")

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == FLASK_USER:
        return FLASK_PASS
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403) # 403 is nicer since it doesn't pop open a login box, but it does violate HTTP standard...

#--------------- Flask setup ---------------#
app = Flask(__name__)

mail = [
    {
        'id': 1,
        'name': u'Dan Abramov',
        'email': u'dan@abramov.com',
        'subject': u'Your site needs some state management',
        'body': u'Have you heard of the library I wrote called Redux?'
    },
    {
        'id': 2,
        'name': u'Scout',
        'email': u'hey+scout@bridgerputnam.me',
        'subject': u'Need an allowance increase',
        'body': u'When I bring the paper in, I deserve at least two treats. Maybe even a milkbone.'
    }
]

#------------- Helper functions ------------#
def make_public_email(email):
    new_email = {}
    for field in email:
        if field == 'id':
            new_email['uri'] = url_for('get_mail_by_id', mail_id=email['id'], _external=True) #_external displays the server root URL!
        else:
            new_email[field] = email[field]
    return new_email

def validate_email(email):
    # RegEx adapted from https://www.regular-expressions.info/email.html
    if re.match(r'\b[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}\b', email):
        return True
    return False

#----------------- Routing -----------------#
# The following is example code, me playing around with making an API
@app.route('/')
def index():
    return '''What, this isn't an API!'''

@app.route('/mailer/api/v1.0/mail', methods=['GET'])
def get_mail():
    return jsonify({'mail': [make_public_email(email) for email in mail]})

@app.route('/mailer/api/v1.0/mail/<int:mail_id>', methods=['GET'])
def get_mail_by_id(mail_id):
    email = [email for email in mail if email['id'] == mail_id]
    if len(email) == 0:
        abort(404)
    return jsonify({'task': email[0]})

@app.route('/mailer/api/v1.0/mail/<int:mail_id>', methods=['PUT'])
@auth.login_required
def update_mail(mail_id):
    email = [email for email in mail if email['id'] == mail_id]
    if len(email) == 0 or not request.json:
        abort(400)
    if 'email' in request.json and type(request.json['email']) is not str:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'subject' in request.json and type(request.json['subject']) is not str:
        abort(400)
    if 'body' in request.json and type(request.json['body']) is not str:
        abort(400)
    email[0]['email'] = request.json.get('email',email[0]['email'])
    email[0]['name'] = request.json.get('name',email[0]['name'])
    email[0]['subject'] = request.json.get('subject',email[0]['subject'])
    email[0]['body'] = request.json.get('body',email[0]['body'])
    return jsonify({'email': email[0]})

@app.route('/mailer/api/v1.0/mail/<int:mail_id>', methods=['DELETE'])
@auth.login_required
def delete_mail(mail_id):
    email = [email for email in mail if email['id'] == mail_id]
    if len(email) == 0 or not request.json:
        abort(400)
    mail.remove(email[0])
    return jsonify({'result': True, 'message': 'Email deleted', 'email_deleted': email[0]})


# This is the only one that does anything
@app.route('/mailer/api/v1.0/mail', methods=['POST'])
@auth.login_required
def post_mail():
    if not request.json or not 'body' in request.json:
        abort(400)
    if len(mail) == 0:
        new_id = 1
    else:
        new_id = mail[-1]['id'] + 1
    email_address = request.json.get('email') if validate_email(request.json.get('email')) else ""
    email = {
        'id': new_id,
        'email': email_address,
        'name': request.json.get('name'),
        'subject': request.json.get('subject'),
        'body': request.json['body']
    }
    #mail.append(email)
    sent_mail = send_mail(email)
    return jsonify({'result': True, 'message': 'Message sent', 'email_sent': sent_mail}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#------------------- Main ------------------#
if __name__ == '__main__':
    app.run(debug=True)