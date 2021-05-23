import json
import boto3
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('emails')


@app.route('/')
def index():
    return json_response({"message": "Hello, world!"})


@app.route('/emails', methods=['GET', 'POST'])
def put_list_emails():
    if request.method == 'GET':
        emails = table.scan()['Items']
        return json_response(emails)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "email entry created"})


@app.route('/emails/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_email(id):
    key = {'id': id}
    if request.method == 'GET':
        email = table.get_item(Key=key).get('Item')
        if email:
            return json_response(email)
        else:
            return json_response({"message": "email not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "email entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "email entry deleted"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
