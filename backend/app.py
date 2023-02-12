import base64
from flask import Flask, make_response
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

ITEMS_PER_PAGE = 10

@app.route('/jira/issue/<issue_id>', methods=['GET'])
def jira_issue(issue_id):
    # Base64 encode the credentials
    auth = base64.b64encode(b'sagi.twig:St123369').decode('utf-8')

    # Set the Authorization header
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json',
        "Content-Encoding": "gzip",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"

    }

    # Send the API request
    response = requests.get(f'https://jira-soft.ngsoft.com/rest/api/2/issue/{issue_id}', headers=headers)

    string_data = response.content.decode("utf-8")

    # Return the response
    return make_response(jsonify(string_data), 200)
    

@app.route('/jira/search/<project_id>', methods=['POST', 'GET'])
def jira_jql(project_id):
    # Base64 encode the credentials
    auth = base64.b64encode(b'sagi.twig:St123369').decode('utf-8')
    page = request.args.get('page', default=1, type=int)

    limit = ITEMS_PER_PAGE

    # Set the Authorization header
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json',
        "Content-Encoding": "gzip",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }


    # Send the API request
    response = requests.get(f'https://jira-soft.ngsoft.com/rest/api/2/search/?jql=project={project_id}&startAt={(page - 1) * limit}&maxResults={limit}', headers=headers)

    string_data = response.content.decode("utf-8")

    # Return the response
    print(project_id)
    return make_response(string_data, 200)
    

@app.route('/jira/project', methods=['POST', 'GET'])
def get_all_projects():
    # Extract the page and limit parameters from the query string
    page = request.args.get('page', default=1, type=int)
    limit = ITEMS_PER_PAGE
    # Base64 encode the credentials
    auth = base64.b64encode(b'sagi.twig:St123369').decode('utf-8')


    # Set the Authorization header
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json',
        "Content-Encoding": "gzip",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    # Send the API request with the startAt and maxResults parameters
    response = requests.get(f'https://jira-soft.ngsoft.com/rest/api/2/project?startAt={(page - 1) * limit}&maxResults={limit}', headers=headers)

    string_data = response.content.decode("utf-8")

    # Return the response
    return make_response(string_data, 200)

    
if __name__ == '__main__':
    app.run()