from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
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


if __name__ == '__main__':
    app.run(debug=True)
