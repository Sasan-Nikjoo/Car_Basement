from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Use yaml.safe_load() for loading the YAML configuration file
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        carDetails = request.form
        name = carDetails['name']
        color = carDetails['color']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mycars(name, color) VALUES(%s, %s)", (name, color))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('list_cars'))
    return render_template('add_car.html')


@app.route('/cars')
def list_cars():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, color FROM mycars")
    cars = cur.fetchall()
    cur.close()
    return render_template('list_cars.html', cars=cars)


if __name__ == '__main__':
    app.run(debug=True)
