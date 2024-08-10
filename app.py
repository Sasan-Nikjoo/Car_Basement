from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace this with your MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/MYSQL80'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20), nullable=False)
    km = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Car {self.id}>'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_car():
    app.logger.info('Entered add_car route')
    if request.method == 'POST':
        try:
            color = request.form['color']
            km = float(request.form['km'])
            new_car = Cars(color=color, km=km)
            db.session.add(new_car)
            db.session.commit()
            app.logger.info('New car added successfully')
            return redirect(url_for('show_cars'))
        except Exception as e:
            app.logger.error(f'Error adding car: {e}')
            return f"There was an issue adding your car: {str(e)}"
    return render_template('add_car.html')


@app.route('/cars')
def show_cars():
    cars = Cars.query.all()
    return render_template('show_cars.html', cars=cars)


@app.route('/test')
def test():
    return "Test route is working!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
