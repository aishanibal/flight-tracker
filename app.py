from flask import Flask, render_template, request, redirect
import mysql.connector
from config_secret import DB_CONFIG


app = Flask(__name__)

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if request.method == 'POST':
        data = (
            request.form['speed'],
            request.form['maintained'] or None,
            request.form['airline_id'],
            request.form['neo'],
            request.form['tail_num'],
            request.form['location_id'],
            request.form['model'] or None,
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

if __name__ == '__main__':
    app.run(debug=True)
