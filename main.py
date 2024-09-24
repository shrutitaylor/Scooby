import requests
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
myScooter = {'id': 2, 'make': 'Lincoln', 'colour': 'White', 'location': 'Sydney', 'remaining_power': '60%', 'cost': '$13/hour', 'isLocked':'TRUE'}


# Backend API base URL
BACKEND_URL = 'http://localhost:5001/api'

#Landing page
@app.route('/')
def home():
    return render_template('base.html')

#Login Page
@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_data = {
            'username': username,
            'password': start_time,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        login_response = requests.post(f'{BACKEND_URL}/user', json=login_data)

        if login_response.status_code == 201:
            flash(f'User - {username} login successfully!')
            g.user = login_response.user
            return redirect(url_for('pages/dashboard.html'))
        else:
            flash('login failed. Please try again.')
            return redirect(url_for('auth/login.html'))

    return render_template('auth/login.html')

#Register page
@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        
        # Post the user details to the backend
        user_data = {
            'username': username,
            'password': start_time,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        user_response = requests.post(f'{BACKEND_URL}/user', json=user_data)

        if user_response.status_code == 201:
            flash(f'User - {username} registered successfully!')
            return redirect(url_for('pages/dashboard.html'))
        else:
            flash('Register user failed. Please try again.')
            return redirect(url_for('auth/register.html'))
    
    return render_template('auth/register.html')

#Scooters display page
@app.route('/scooters')
def scooters():
    response = requests.get(f'{BACKEND_URL}/scooters')
    scooter_list = response.json()
    return render_template('pages/scooters.html', scooters=scooter_list)

#Booking page
@app.route('/book/<int:scooter_id>', methods=['GET', 'POST'])
def book_scooter(scooter_id):
    # Find the scooter details based on scooter_id
    # Need to get details from backend in irl
    scooter = next((s for s in scooter_list if s['id'] == scooter_id), None)
    
     # Get scooter details from the backend
    response = requests.get(f'{BACKEND_URL}/scooters/{scooter_id}')
    scooter = response.json()
    
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        # Post the booking details to the backend
        booking_data = {
            'scooter_id': scooter_id,
            'start_time': start_time,
            'end_time': end_time,
        }
        booking_response = requests.post(f'{BACKEND_URL}/bookings', json=booking_data)

        if booking_response.status_code == 201:
            flash(f'Scooter {scooter_id} booked from {start_time} to {end_time} successfully!')
            # i need = email of user_details +  start_time, end_time of booking details + scooter id and location in scooter details
            #createCalendarEvent(user_details= user_details, booking_details = booking_details, scooter_details = scooter_details) # creating calendar event
            return redirect(url_for('scooters'))
        else:
            flash('Booking failed. Please try again.')
            return redirect(url_for('book_scooter', scooter_id=scooter_id))


    return render_template('pages/book_scooter.html', scooter_id=scooter_id, scooter=scooter)

#My Bookings page
@app.route('/bookings')
def bookings_page():
    response = requests.get(f'{BACKEND_URL}/bookings')
    bookings = response.json()
    print(response.json())
    return render_template('pages/bookings.html', bookings=bookings)

#My Dashboard page
@app.route('/dashboard')
def dashboard():
    response = requests.get(f'{BACKEND_URL}/myScooter')
    myScooter = response.json()
    return render_template('pages/dashboard.html', currentUser=g.user, scooter = myScooter)

#dummy
@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name


def createCalendarEvent(booking_details,scooter_details,user_details):
    # date = datetime.now()
    # tomorrow = (date + timedelta(days = 1)).strftime("%Y-%m-%d")
    # time_start = "{}T06:00:00+10:00".format(tomorrow)
    # time_end = "{}T07:00:00+10:00".format(tomorrow)
    event = {
        "summary": "Scooby Booked",
        "location": scooter_details.location,
        "description": "Your scooter with scooterID:"+scooter_details.id,
        "start": {
            "dateTime": booking_details.start_time,
            "timeZone": "Australia/Melbourne",
        },
        "end": {
            "dateTime": booking_details.end_time,
            "timeZone": "Australia/Melbourne",
        },
        "attendees": [
            { "email": user_details.email },
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "email", "minutes": 5 },
                { "method": "popup", "minutes": 10 },
            ],
        }
    }

    event = service.events().insert(calendarId = "primary", body = event).execute()
    print("Event created: {}".format(event.get("htmlLink")))

if __name__ == '__main__':
    app.run(debug=True)
