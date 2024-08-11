from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Load the database configuration from the YAML file
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
        count_of_airbags = carDetails['count_of_airbags']
        has_sunroof = 'has_sunroof' in carDetails
        first_release_day = carDetails['first_release_day']
        image_url = carDetails['image_url']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO mycars(name, color, count_of_airbags, has_sunroof, first_release_day, image_url) VALUES(%s, %s, %s, %s, %s, %s)",
            (name, color, count_of_airbags, has_sunroof, first_release_day, image_url))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('list_cars'))
    return render_template('add_car.html')



@app.route('/cars', methods=['GET'])
def list_cars():
    search_query = request.args.get('search', '')
    cur = mysql.connection.cursor()
    query = "SELECT id, name, color, count_of_airbags, has_sunroof, first_release_day, image_url FROM mycars WHERE name LIKE %s ORDER BY id"
    cur.execute(query, ('%' + search_query + '%',))
    cars = cur.fetchall()
    cur.close()
    return render_template('list_cars.html', cars=cars, search_query=search_query)



@app.route('/delete_car/<int:id>', methods=['POST'])
def delete_car(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mycars WHERE id = %s", [id])
    mysql.connection.commit()

    # Re-number the remaining IDs
    cur.execute("SET @new_id = 0;")
    cur.execute("UPDATE mycars SET id = (@new_id := @new_id + 1) ORDER BY id;")
    cur.execute("ALTER TABLE mycars AUTO_INCREMENT = 1;")

    mysql.connection.commit()
    cur.close()
    return redirect(url_for('list_cars'))


if __name__ == '__main__':
    app.run(debug=True)
