from flask import Flask, render_template
import json, requests


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('dataseta.html')

@app.route('/data')
def data():
	req = requests.get('https://pomber.github.io/covid19/timeseries.json')
	values = req.json()
	return (values)

if __name__ == '__main__':
	app.run(debug=True)