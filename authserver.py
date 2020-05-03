from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User

@app.route("/")
def hello():
    return "This is de auth server"

@app.route("/add")
def add_user():
    username = request.args.get('username')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    try:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        db.session.commit()
        return "User added. The new id is {}".format(new_user.id)
    except Exception as e:
        return str(e)



@app.route("/getall")
def get_all():
    try:
        users=User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
	    return(str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        user=User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))


@app.route("/add/user",methods=['POST'])
def add_book_form():
    if request.method == 'POST':
        username = request.args.get('username')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        try:
            new_user = User(username,first_name,last_name)
            db.session.add(new_user)
            db.session.commit()
            return "User added by POST. The new id is {}".format(new_user.id)
        except Exception as e:
            return str(e)
    else:
        return "POST Not found"

if __name__ == '__main__':
    app.run()
