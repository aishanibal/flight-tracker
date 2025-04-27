from flask import Flask, render_template, request, redirect
import mysql.connector
from config_secret import DB_CONFIG


app = Flask(__name__)

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if request.method == 'POST':
        data = (
            request.form['speed'],
            request.form.get('maintained') or None,
            request.form['airline_id'],
            request.form['neo'],
            request.form['tail_num'],
            request.form['location_id'],
            request.form.get('model') or None,
            request.form['seat_cap'],
            request.form['plane_type'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('add_airplane', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('add_airplane.html')

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if request.method == 'POST':
        data = (
            request.form['state'],
            request.form['airport_id'],
            request.form['airport_name'],
            request.form['country'],
            request.form['city'],
            request.form['location_id'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('add_airport', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('add_airport.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        data = (
            request.form['location_id'],
            request.form.get('miles') or None,
            request.form['person_id'],
            request.form['first_name'],
            request.form['tax_id'],
            request.form.get('funds') or None,
            request.form['last_name'],
            request.form['experience'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('add_person', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('add_person.html')

@app.route('/grant_or_revoke_pilot_license', methods=['GET', 'POST'])
def grant_or_revoke_pilot_license():
    if request.method == 'POST':
        data = (
            request.form['license'],
            request.form['person_id'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('grant_or_revoke_pilot_license', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('grant_or_revoke_pilot_license.html')

@app.route('/offer_flight', methods=['GET', 'POST'])
def offer_flight():
    if request.method == 'POST':
        data = (
            request.form['progress'],
            request.form['cost'],
            request.form['flight_id'],
            request.form['route_id'],
            request.form['next_time'],
            request.form['support_airline'],
            request.form['support_tail'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('offer_flight', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('offer_flight.html')

@app.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('flight_landing', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('flight_landing.html')

@app.route('/flight_takeoff', methods=['GET', 'POST'])
def flight_takeoff():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('flight_takeoff', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('flight_takeoff.html')

@app.route('/passengers_board', methods=['GET', 'POST'])
def passengers_board():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('passengers_board', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('passengers_board.html')

@app.route('/passengers_disembark', methods=['GET', 'POST'])
def passengers_disembark():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('passengers_disembark', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('passengers_disembark.html')

@app.route('/assign_pilot', methods=['GET', 'POST'])
def assign_pilot():
    if request.method == 'POST':
        data = (
            request.form['flight_id'],
            request.form['person_id'],
        )
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('assign_pilot', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('assign_pilot.html')

@app.route('/recycle_crew', methods=['GET', 'POST'])
def recycle_crew():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('recycle_crew', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('recycle_crew.html')

@app.route('/retire_flight', methods=['GET', 'POST'])
def retire_flight():
    if request.method == 'POST':
        data = (request.form['flight_id'],)
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('retire_flight', data)
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('retire_flight.html')

@app.route('/simulation_cycle', methods=['GET', 'POST'])
def simulation_cycle():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.callproc('simulation_cycle')
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('simulation_cycle.html')


@app.route('/flights_in_air')
def flights_in_air():
    return render_view('flights_in_the_air')

@app.route('/flights_on_ground')
def flights_on_ground():
    return render_view('flights_on_the_ground')

@app.route('/people_in_air')
def people_in_air():
    return render_view('people_in_the_air')

@app.route('/people_on_ground')
def people_on_ground():
    return render_view('people_on_the_ground')

@app.route('/route_summary')
def route_summary():
    return render_view('route_summary')

@app.route('/alternative_airports')
def alternative_airports():
    return render_view('alternative_airports')


def render_view(view_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {view_name};")
    rows = cursor.fetchall()
    columns = cursor.column_names
    cursor.close()
    db.close()
    return render_template('view.html', rows=rows, columns=columns, view_name=view_name)

if __name__ == '__main__':
    app.run(debug=True)
