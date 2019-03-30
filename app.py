#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

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

def make_public_email(email):
    new_email = {}
    for field in email:
        if field == 'id':
            new_email['uri'] = url_for('get_mail_by_id', mail_id=email['id'], _external=True) #_external displays the server root URL!
        else:
            new_email[field] = email[field]
    return new_email

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
def delete_mail(mail_id):
    email = [email for email in mail if email['id'] == mail_id]
    if len(email) == 0 or not request.json:
        abort(400)
    mail.remove(email[0])
    return jsonify({'email_to_delete': email[0]})
    #return jsonify({'result': True, 'message': 'Email deleted'})


# This is the only one that does anything
@app.route('/mailer/api/v1.0/mail', methods=['POST'])
def send_mail():
    if not request.json or not 'subject' in request.json:
        abort(400)
    if len(mail) == 0:
        new_id = 1
    else:
        new_id = mail[-1]['id'] + 1
    email = {
        'id': new_id,
        'email': request.json.get('email',""),
        'name': request.json.get('name',""),
        'subject': request.json['subject'],
        'body': request.json.get('body',"")
    }
    mail.append(email)
    #send_mail(email)
    return jsonify({'result': True, 'message': 'Message sent'}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)