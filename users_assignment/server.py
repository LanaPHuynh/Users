from flask import Flask, render_template, request, redirect, session
from users_sql import connectToMySQL

app = Flask(__name__)
app.secret_key = "this is the secret key"


@app.route("/users/new")
def index(): 
    print(request.form)
    return render_template("users_new.html")

@app.route("/create", methods=['POST'])
def add_new_user_to_db():
    mysql = connectToMySQL('users_assignment')
    print("\nAdded" + request.form["fname"] + "to database")
    print(request.form)
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    mysql.query_db(query, data)
    # name = session(request.form["fname"])

    return redirect("/users/id")


@app.route("/users/<id>")
def display_newly_added_user(id):
    mysql = connectToMySQL('users_assignment')
    query = "SELECT * FROM users WHERE id = :specific_id LIMIT 1;"
    data = {
        "specific_id": id
    }
    user = mysql.query_db(query,data)
    print(user)
    return render_template("users_id.html", id = id, user = user)



@app.route("/users")
def display_all_users():
    print("\nDisplaying new user")
    mysql = connectToMySQL('users_assignment')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template("users.html", all_users = users)

if __name__=="__main__":
    app.run(debug=True)
