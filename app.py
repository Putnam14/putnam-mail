#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

mail = [
    {
        'id': 1,
        'name': u'Dan Abramov',
        'email': u'dan@abramov.com',
        'subject': u'Your site needs some state management',
        'description': u'Have you heard of the library I wrote called Redux?'
    },
    {
        'id': 2,
        'name': u'Scout',
        'email': u'hey+scout@bridgerputnam.me',
        'subject': u'Need an allowance increase',
        'description': u'When I bring the paper in, I deserve at least two treats. Maybe even a milkbone.'
    }
]

@app.route('/')
def index():
    return '''What, this isn't an API!'''

@app.route('/mailer/api/v1.0/mail', methods=['GET'])
def get_mail():
    return jsonify({'mail': mail})

@app.route('/mailer/api/v1.0/mail/<int:mail_id>', methods=['GET'])
def get_mail_by_id(mail_id):
    single_mail = [single_mail for single_mail in mail if single_mail['id'] == mail_id]
    if len(single_mail) == 0:
        abort(404)
    return jsonify({'task': single_mail[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)