from flask import Flask, flash, g, redirect, render_template, request, url_for

# from auth import bp as auth_bp  # Import the auth blueprint

app = Flask(__name__)

# Register the auth blueprint
# app.register_blueprint(auth_bp)
#dummy data for scooters
scooter_list = [
        {'id': 1, 'make': 'Ford', 'colour': 'Black', 'location': 'Melbourne', 'remaining_power': '20%', 'cost': '$12/hour'},
        {'id': 2, 'make': 'Lincoln', 'colour': 'White', 'location': 'Sydney', 'remaining_power': '60%', 'cost': '$13/hour'},
        {'id': 3, 'make': 'Subaru', 'colour': 'Red', 'location': 'Brisbane', 'remaining_power': '90%', 'cost': '$13.50/hour'},
    ]
# dummy data for bookings table
bookings = [
    {'id': 1, 'scooter_id': 1, 'start_time': '2024-09-22 10:00', 'end_time': '2024-09-22 12:00',"isClosed": "TRUE"},
    {'id': 2, 'scooter_id': 2, 'start_time': '2024-09-23 09:00', 'end_time': '2024-09-23 10:30',"isClosed": "FALSE"},
    {'id': 3, 'scooter_id': 3, 'start_time': '2024-09-24 08:30', 'end_time': '2024-09-24 09:30',"isClosed": "TRUE"},
]

currentUser = {"TopUp" : "23"}

#Landing page
@app.route('/')
def home():
    return render_template('base.html')

#Login Page
@app.route('/login')
def login():
    return render_template('auth/login.html')

#Register page
@app.route('/register')
def register():
    return render_template('auth/register.html')

#Scooters display page
@app.route('/scooters')
def scooters():
   
    return render_template('pages/scooters.html', scooters=scooter_list)

#Booking page
@app.route('/book/<int:scooter_id>', methods=['GET', 'POST'])
def book_scooter(scooter_id):
    # Find the scooter details based on scooter_id
    # Need to get details from backend in irl
    scooter = next((s for s in scooter_list if s['id'] == scooter_id), None)
    # if request.method == 'POST':
    #     start_time = request.form['start_time']
    #     end_time = request.form['end_time']
        
    #     #printing output
    #     flash(f'Scooter {scooter_id} booked from {start_time} to {end_time} successfully!')
    #     return redirect(url_for('scooters'))

    return render_template('pages/book_scooter.html', scooter_id=scooter_id, scooter=scooter)

#My Bookings page
@app.route('/bookings')
def bookings_page():
    return render_template('pages/bookings.html', bookings=bookings)

#My Bookings page
@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html', currentUser=currentUser)
#dummy
@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

if __name__ == '__main__':
    app.run(debug=True)
