## Author

- Milan Procházka

## Currency converter project

- CLI application
- web API application

## Uses

- Flask
- Python3.4

## Parameters
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

## Functionality
- if output_currency param is missing, convert to all known currencies

## Output
- json with following structure.
```
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```
## Examples

### CLI 
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
```

### WEB API
- first launch flask app
```
FLASK_APP=currency_converter_web.py flask run
```
- then open given link in browser and add input parameters:
```
/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD
```
```
/currency_converter?amount=10.92&input_currency=£
```

