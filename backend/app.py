import base64
from flask import Flask, make_response
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import json



app = Flask(__name__)
CORS(app)

ITEMS_PER_PAGE = 10
BASE_URL = "https://jira-soft.ngsoft.com/rest/api/2"
NO_RESULT_SEARCH = "startAt=0&maxResults=0"


def get_total_issues(jql, headers, BASE_URL, NO_RESULT_SEARCH):
    response = requests.get(f'{BASE_URL}/search/?jql={jql}&{NO_RESULT_SEARCH}', headers=headers)
    response_json = json.loads(response.text)
    return response_json['total']



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
    response = requests.get(f'{BASE_URL}/issue/{issue_id}', headers=headers)

    string_data = response.content.decode("utf-8")

    # Return the response
    return make_response(jsonify(string_data), 200)
    

@app.route('/jira/search/<project_id>', methods=['POST', 'GET'])
def jira_jql(project_id):
    # Base64 encode the credentials
    auth = base64.b64encode(b'sagi.twig:St123369').decode('utf-8')
    page = request.args.get('page', default=1, type=int)

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
    response = requests.get(f'{BASE_URL}/search/?jql=project={project_id}&startAt={(page - 1) * ITEMS_PER_PAGE}&maxResults={ITEMS_PER_PAGE}', headers=headers)
    string_data = response.content.decode("utf-8")



    total_issues = get_total_issues(f'project={project_id}', headers, BASE_URL, NO_RESULT_SEARCH)
    total_issues_blocker = get_total_issues(f'project={project_id} AND severity="blocker"', headers, BASE_URL, NO_RESULT_SEARCH)
    total_issues_critical = get_total_issues(f'project={project_id} AND severity="critical"', headers, BASE_URL, NO_RESULT_SEARCH)



    res = {
        "data": string_data,
        "total_issues" : total_issues,
        "total_blocker" : total_issues_blocker,
        "total_critical" : total_issues_critical,
    }


    # Return the response
    print(total_issues_blocker)
    return make_response(res, 200)
    

@app.route('/jira/project', methods=['POST', 'GET'])
def get_all_projects():
    # Extract the page parameters from the query string
    page = request.args.get('page', default=1, type=int)

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
    response = requests.get(f'https://jira-soft.ngsoft.com/rest/api/2/project?startAt={(page - 1) * ITEMS_PER_PAGE}&maxResults={ITEMS_PER_PAGE}', headers=headers)

    string_data = response.content.decode("utf-8")

    # Return the response
    return make_response(string_data, 200)

    
if __name__ == '__main__':
    app.run()