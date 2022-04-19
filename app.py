from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
DB_URI = "postgresql+psycopg2://digitalskola:D6GhCbaaiq8LlNy7@35.193.53.27:5432/api"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

users = {
    "agus": generate_password_hash("hello"),
    "bambang": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

class Users(db.Model):
  __table_args__ = {"schema": "aji"}
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String)

  def __init__(self, name, address):
    self.name = name
    self.address = address

@auth.login_required
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.authorization is None:
        return {"message": f"Not Authorized."}
    else:
        pass
    if request.method == 'GET':
        users = Users.query.all()
        result = [
            {
                "name": user.name,
                "address": user.address
            } for user in users]
        return jsonify(result)
    
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_users = Users(name=data['name'], address=data['address'])
            db.session.add(new_users)
            db.session.commit()
            return {"message": f"User {new_users.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = Users.query.get_or_404(user_id)

    if request.method == 'GET':
        response = {
            "name": user.name,
            "address": user.address
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user.name = data['name']
        user.address = data['address']
        db.session.add(user)
        db.session.commit()
        return {"message": f"user {user.name} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"user {user.name} successfully deleted."}

if __name__ == "__main__":
    app.run(debug=True, port=8080)

