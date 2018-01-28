from flask import Flask, request, jsonify
from converter.converter import *

app = Flask(__name__)


@app.route('/')
def index():
	return 'Index page'


@app.route('/currency_converter')
def currency_converter():
	amount = request.args.get('amount', type=float)
	input_cur = request.args.get('input_currency', type=str)
	output_cur = request.args.get('output_currency', type=str, default="")

	input_dict = {}
	output_dict = {}

	try:
		input_currency = currency_code(input_cur)
		input_dict['amount'] = amount
		input_dict['currency'] = input_currency

		if(output_cur != ""):
			output_currency = currency_code(output_cur)
			output_dict[output_currency] = exchange(
				input_currency, output_currency, amount)
		else:
			output_dict = {currency: exchange(
				input_currency, currency, amount) for currency in currency_symbols.values()}
			output_dict.pop(input_currency)

		result={}
		result["input"] = input_dict
		result["output"] = output_dict

		# for identation as in examples, I have to make custom response and use json.dumps
		result_json = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
		response = app.response_class(
			response=result_json,
			status = 200,
			mimetype='application/json'
		)
		return response

		#jsonify has different indentation than example output
		#return jsonify(result)

	except Exception as err:
		return str(err)
