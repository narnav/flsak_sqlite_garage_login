import sqlite3
from flask import Flask, redirect, render_template, request, url_for

api = Flask(__name__)

con = sqlite3.connect("tutorial.db",check_same_thread=False)
logged =False
cur = con.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT NOT NULL,
#                 password TEXT NOT NULL
#              )''')
@api.route('/')
def hello():
    return render_template("home.html")


@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Insert user data into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        return redirect(url_for('hello'))
    return render_template("register.html")

@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in the database
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        
        if user:
            logged =True
            # User exists, perform login action (e.g., set session)
            # Here, you might set a session or cookie to maintain user's login state
            return "Logged in successfully!"
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")


# Modify your add route to handle both GET and POST requests
@api.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        year = request.form['year']
        make = request.form['make']
        color = request.form['color']
        
        # Insert data into the database
        cur.execute("INSERT INTO cars VALUES (?, ?, ?)", (year, make, color))
        con.commit()
        return "Car added successfully!"
    return render_template("add.html")


@api.route('/get_cars')
def get_cars():
    if not logged:
        return redirect(url_for('login'))
    # Fetch data from the database
    cur.execute("SELECT *,rowid FROM cars")
    cars = cur.fetchall()  # Fetch all rows
    
    # Render the template and pass the retrieved data
    return render_template("cars.html", cars=cars)


@api.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    if request.method == 'POST':
        # Delete the specified car from the database
        cur.execute("DELETE FROM cars WHERE rowid=?", (car_id,))
        con.commit()
        return "Car deleted successfully!"


if __name__ == '__main__':
    api.run(debug=True)

