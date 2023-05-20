#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from boto3.dynamodb.conditions import Key, Attr
import requests
import boto3



from boto3.dynamodb.conditions import Key


application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/check/<string:currency>', methods=['GET'])
def get_currency_check(currency):
    return Response(json.dumps({'result': currency_rate.get(currency)}), mimetype='application/json', status=200)

# test: curl localhost:8000/check/bitcoin
@application.route('/check/bitcoin', methods=['GET'])
def get_bitcoin():
    res = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json');
    print(res.text)
    return Response(json.dumps(res.text), mimetype='application/json', status=200)

# get example for multiplication
# test get  
# curl -i http://"localhost:8000/v1/multiply?amount=12"
@application.route('/v1/multiply', methods=['GET', 'POST'])
def get_mult_res():
    amount = request.args.get('amount')
    return Response(json.dumps({'amount': amount}), mimetype='application/json', status=200)

currency_rate = {
    'usd' : 3.3,
    'pound' : 4.5,
    'euro' : 4.8
}

@application.route('/get_forms', methods=['GET'])
def get_frm():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)

# curl -i -X POST -d'{"form_title":"form title1", "form_body":"where is it?", "form_type":"finance"}' -H "Content-Type: application/json" http://localhost:8000/set_form/frm144
@application.route('/set_form/<frm_id>', methods=['POST'])
def set_doc(frm_id):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('forms')
    # get post data  
    data = request.data
    print(data)
    
    # convert the json to dictionary
    data_dict = json.loads(data)
    # retreive the parameters
    form_body = data_dict.get('form_body','default')
    form_title = data_dict.get('form_title','defualt')
    form_type = data_dict.get('form_type', 'default')

    item={
    'form_id': frm_id,
    'form_body': form_body,
    'form_title': form_title, 
    'form_type': form_type 
     }
    table.put_item(Item=item)
    
    return Response(json.dumps(item), mimetype='application/json', status=200)

@application.route('/get_generics', methods=['GET'])
def get_generics():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('generics')
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)

if __name__ == '__main__':
    flaskrun(application)