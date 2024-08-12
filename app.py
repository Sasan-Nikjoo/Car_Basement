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


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('list_cars'))


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        carDetails = request.form
        name = carDetails['name']
        color = carDetails['color']
        count_of_airbags = carDetails['count_of_airbags']
        has_sunroof = 'has_sunroof' in carDetails
        first_release_day = carDetails['first_release_day']
        image_url = carDetails['image_url']
        company_id = carDetails['company_id']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO mycars(name, color, count_of_airbags, has_sunroof, first_release_day, image_url, company_id) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (name, color, count_of_airbags, has_sunroof, first_release_day, image_url, company_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('list_cars'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name FROM companies")
        companies = cur.fetchall()
        cur.close()

        return render_template('add_car.html', companies=companies)


@app.route('/cars', methods=['GET'])
def list_cars():
    search_query = request.args.get('search', '')
    company_id = request.args.get('company_id', '')

    cur = mysql.connection.cursor()
    query = """
        SELECT mycars.id, mycars.name, mycars.color, mycars.count_of_airbags, mycars.has_sunroof, mycars.first_release_day, mycars.image_url, companies.name 
        FROM mycars 
        JOIN companies ON mycars.company_id = companies.id 
        WHERE mycars.name LIKE %s
    """

    if company_id:
        query += " AND mycars.company_id = %s"
        cur.execute(query, ('%' + search_query + '%', company_id))
    else:
        cur.execute(query, ('%' + search_query + '%',))

    cars = cur.fetchall()
    cur.execute("SELECT id, name FROM companies")
    companies = cur.fetchall()
    cur.close()

    return render_template('list_cars.html', cars=cars, search_query=search_query, companies=companies,
                           selected_company_id=company_id)


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


@app.route('/car/<int:id>', methods=['GET'])
def car_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, color, count_of_airbags, has_sunroof, first_release_day, image_url FROM mycars WHERE id = %s", [id])
    car = cur.fetchone()
    cur.close()
    if car:
        return render_template('car_detail.html', car=car)
    else:
        return "Car not found", 404


if __name__ == '__main__':
    app.run(debug=True)
