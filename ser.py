from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def respond():
	name = request.args.get('name')
	print(name)
	res = {'name':name}
	return jsonify(res)

@app.route('/webhook', methods=['POST'])
def query():
	req=request.get_json(silent=True, force=True)
	intent=req.get('queryResult').get('intent').get('displayName')
	if intent=='Default Welcome Intent':
		qtext=req.get('queryResult').get('queryText')
		#name = request.form.get('name')
		res = {'fulfillmentText':'Received '+qtext}
		return jsonify(res)
	elif intent=='number':
		qtype=req.get('queryResult').get('parameters').get('type')
		num=req.get('queryResult').get('parameters').get('number-integer')
		#print(qtype,null)
		num=int(num)
		url = 'http://numbersapi.com/'
		final_url = url + str(num) + '/' +qtype + '?json'
		res = requests.get(final_url)
		text=res.json()['text']
		return jsonify({'fulfillmentText':text})
	return jsonify({'fulfillmentText':'error'})

@app.route('/hello')
def hello():
	return 'Hello World!'

if __name__ == '__main__':
	app.run()
