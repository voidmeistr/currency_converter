from flask import Flask, request, jsonify, abort
from converter.converter import *

app = Flask(__name__)


@app.route("/currency_converter")
def currency_converter():
    amount = request.args.get("amount", type=float, default=-1)
    input_cur = request.args.get("input_currency", type=str, default="")
    output_cur = request.args.get("output_currency", type=str, default="")

    # invalid arguments
    if amount == -1 or input_cur == "":
        abort(404)

    try:
        # input parameters
        input_currency = currency_code(input_cur)
        input_dict = {
            "amount": amount,
            "currency": input_currency
        }

        # try to make output dictionary
        output_dict = make_output(amount, input_currency, output_cur)

        # make response
        response = app.response_class(
            response=to_json(input_dict, output_dict),
            status=200,
            mimetype="application/json"
        )

        # return
        return response

        # jsonify has different indentation than example output
        # return jsonify(result)

    # unknow currency code / connection to ECB couldn't be established
    except Exception as err:
        return str(err)
