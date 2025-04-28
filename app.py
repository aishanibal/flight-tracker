from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from config_secret import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'phase4_secret'

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def clean_int(value):
    return int(value) if value.strip() else None

def clean_bool(value):
    if value.strip() == '':
        return None
    return bool(int(value))

def clean_str(value):
    return value if value.strip() else None

def call_proc(proc_name, params):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.callproc(proc_name, params)
        for result in cursor.stored_results():
            output = result.fetchall()
            if output:
                flash(output[0][0], 'error')
                return False
        db.commit()
        flash(f"{proc_name.replace('_', ' ').capitalize()} successful!", 'success')
        return True
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"MySQL error: {err}", 'error')
        return False
    finally:
        cursor.close()
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

# Procedures
@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if request.method == 'POST':
        data = (
            clean_str(request.form['airline_id']),
            clean_str(request.form['tail_num']),
            clean_int(request.form['seat_cap']),
            clean_int(request.form['speed']),
            clean_str(request.form['location_id']),
            clean_str(request.form['plane_type']),
            clean_bool(request.form.get('maintained') or ''),
            clean_str(request.form.get('model') or ''),
            clean_bool(request.form.get('neo') or ''),
        )
        if call_proc('add_airplane', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('add_airplane.html')

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if request.method == 'POST':
        data = (
            clean_str(request.form['airport_id']),
            clean_str(request.form['airport_name']),
            clean_str(request.form['city']),
            clean_str(request.form['state']),
            clean_str(request.form['country']),
            clean_str(request.form['location_id']),
        )
        if call_proc('add_airport', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('add_airport.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        data = (
            clean_str(request.form['person_id']),
            clean_str(request.form['first_name']),
            clean_str(request.form.get('last_name') or ''),
            clean_str(request.form['location_id']),
            clean_str(request.form.get('tax_id') or ''),
            clean_int(request.form.get('experience') or ''),
            clean_int(request.form.get('miles') or ''),
            clean_int(request.form.get('funds') or ''),
        )
        if call_proc('add_person', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('add_person.html')

@app.route('/grant_or_revoke_pilot_license', methods=['GET', 'POST'])
def grant_or_revoke_pilot_license():
    if request.method == 'POST':
        data = (
            clean_str(request.form['person_id']),
            clean_str(request.form['license'].capitalize()),
        )
        if call_proc('grant_or_revoke_pilot_license', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('grant_or_revoke_pilot_license.html')

@app.route('/offer_flight', methods=['GET', 'POST'])
def offer_flight():
    if request.method == 'POST':
        data = (
            clean_str(request.form['flight_id']),
            clean_str(request.form['route_id']),
            clean_str(request.form.get('support_airline') or ''),
            clean_str(request.form.get('support_tail') or ''),
            clean_int(request.form.get('progress') or ''),
            clean_str(request.form.get('next_time') or ''),
            clean_int(request.form.get('cost') or ''),
        )
        if call_proc('offer_flight', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('offer_flight.html')

@app.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('flight_landing', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('flight_landing.html')

@app.route('/flight_takeoff', methods=['GET', 'POST'])
def flight_takeoff():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('flight_takeoff', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('flight_takeoff.html')

@app.route('/passengers_board', methods=['GET', 'POST'])
def passengers_board():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('passengers_board', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('passengers_board.html')

@app.route('/passengers_disembark', methods=['GET', 'POST'])
def passengers_disembark():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('passengers_disembark', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('passengers_disembark.html')

@app.route('/assign_pilot', methods=['GET', 'POST'])
def assign_pilot():
    if request.method == 'POST':
        data = (
            clean_str(request.form['flight_id']),
            clean_str(request.form['person_id']),
        )
        if call_proc('assign_pilot', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('assign_pilot.html')

@app.route('/recycle_crew', methods=['GET', 'POST'])
def recycle_crew():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('recycle_crew', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('recycle_crew.html')

@app.route('/retire_flight', methods=['GET', 'POST'])
def retire_flight():
    if request.method == 'POST':
        data = (clean_str(request.form['flight_id']),)
        if call_proc('retire_flight', data):
            return redirect('/')
        return redirect(request.url)
    return render_template('retire_flight.html')

@app.route('/simulation_cycle', methods=['GET', 'POST'])
def simulation_cycle():
    if request.method == 'POST':
        if call_proc('simulation_cycle', ()): 
            return redirect('/')
        return redirect(request.url)
    return render_template('simulation_cycle.html')

# Views
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
