from flask import Flask, render_template
import json, requests


app = Flask(__name__)

@app.route('/')
def index():
	response = requests.get('https://pomber.github.io/covid19/timeseries.json')
	
	#returns an exception if something is wrong
	if response.status_code != 200:
		raise Exception(f"Unexpected status code {response.status_code}")
		
	return render_template('datasetb.html')

@app.route('/data')
def data():
	req = requests.get('https://pomber.github.io/covid19/timeseries.json')
	values = req.json()
	return (values)

if __name__ == '__main__':
	app.run(debug=True)
