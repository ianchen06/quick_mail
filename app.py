import re
import mailbox
import os
import string, random
import pathlib
#pathlib.Path('/my/directory').mkdir(parents=True, exist_ok=True) 

from flask import Flask, jsonify
from flask.views import MethodView

from utils import getbody, write_user, read_users, write_domains, read_domains

app = Flask(__name__)

MAILDIR_BASE = '/var/spool/vhosts/'

@app.route("/")
def hello():
    return """
    curl -XPOST http://mail.bitform.co:5000/users/
    curl -XGET http://mail.bitform.co:5000/users/
    curl -XGET http://mail.bitform.co:5000/users/jvdsaupnyr@bitform.co/mails/
    curl -XGET http://mail.bitform.co:5000/users/jvdsaupnyr@bitform.co/mails/fb
    """

class MailAPI(MethodView):
    def get(self, user, msg_id):
        username = user.split('@')[0]
        domain = user.split('@')[1]
        mbox = mailbox.Maildir(MAILDIR_BASE + "%s/%s"%(domain,username))
        if not msg_id:
            app.logger.debug([msg.items() for msg in mbox])
            return jsonify([msg['Message-Id'].replace('<','').replace('>','') for msg in mbox])
        elif msg_id == 'fb':
            for msg in mbox:
                if 'facebook' in msg.get('Message-Id'):
                    content = getbody(msg)
                    app.logger.debug(content)
                    confirm_code = re.findall('\n\n(\d{5})\n\nFacebook', content)
            return jsonify(confirm_code)
        else:
            return jsonify([msg['Message-Id'] for msg in mbox if
            msg['Message-Id'] == "<%s>"%msg_id])

class DomainAPI(MethodView):
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass

    def post(self):
        # create a new user
        username = ''.join(random.sample(string.ascii_lowercase, 10))
        return jsonify([username])

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            users = read_users()
            return jsonify(users)
        else:
            # expose a single user
            pass

    def post(self):
        # create a new user
        domains = read_domains()
        app.logger.debug(domains)
        username = ''.join(random.sample(string.ascii_lowercase, 10))
        user = "%s@%s"%(username, random.choice(domains))
        write_user(user)
        return jsonify([user])

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

mail_view = MailAPI.as_view('mail_api')
domain_view = DomainAPI.as_view('domain_api')
user_view = UserAPI.as_view('user_api')

app.add_url_rule('/domains/', view_func=domain_view, methods=['POST',])
app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/users/<user>/mails/',
                 defaults={'msg_id': None},
                 view_func=mail_view, methods=['GET',])
app.add_url_rule('/users/<user>/mails/<msg_id>',
                 view_func=mail_view, methods=['GET',])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
