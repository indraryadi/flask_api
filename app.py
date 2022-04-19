from flask import Flask, jsonify, request
from db.query_raw import connection

app = Flask(__name__)

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == 'GET':
        query = """
        SELECT * FROM aji.users
        """
        conn, cursor = connection()
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)
    
    elif request.method == 'POST':
        name = request.args.get('name')
        address = request.args.get('address')
        query = f"""
        INSERT INTO aji.users (name, address)
        VALUES ('{name}', '{address}')
        """
        conn, cursor = connection()
        cursor.execute(query)
        conn.commit()
        return {"message": f"Users {name} has been created successfully."}


if __name__ == "__main__":
    app.run(debug=True, port=8080)

