from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def car_list():
    df = pd.read_csv('cars.csv')

    if request.method == 'POST':
        search_query = request.form.get('search')
        max_price = request.form.get('max_price')
        min_price = request.form.get('min_price')
        max_speed = request.form.get('max_speed')

        if search_query:
            df = df[df['name'].str.contains(search_query, case=False, na=False)]

        if max_price:
            df = df[df['price'] <= float(max_price)]

        if min_price:
            df = df[df['price'] >= float(min_price)]

        if max_speed:
            df = df[df['max_speed'] <= float(max_speed)]

    cars = df.to_dict(orient='records')
    return render_template('car_list.html', cars=cars)

if __name__ == '__main__':
    app.run(debug=True)
