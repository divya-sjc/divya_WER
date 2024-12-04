

import csv
import requests

GITHUB_OWNER = 'slanglabs'
GITHUB_REPO = 'polyglot'
GITHUB_TOKEN = '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'
GITHUB_PROJECT_ID = 'PVT_kwDOBusoOM4AiTaY'  # Global project ID
GRAPHQL_URL = "https://api.github.com/graphql"

headers = {
    'Authorization': f"Bearer {GITHUB_TOKEN}",
    'Content-Type': 'application/json'
}

def create_github_issue(title, body, assignee, labels):
    """Creates an issue on GitHub"""
    url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Python Script'
    }
    
    data = {
        'title': title,
        'body': body,
        'assignees': assignee, 
        'labels': labels
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201 or response.status_code == 200:
        issue = response.json()
        # print(f'Successfully created issue: {title}')
        # print(f'Created issue number: {issue["number"]}')
        return issue['number'], issue['url']
    else:
        print(f'Failed to create issue: {title}. Response: {response.content}')
        print(f'Response Code: {response.status_code}')
        return None, None

def run_graphql_query(query, variables=None):
    response = requests.post(GRAPHQL_URL, headers=headers, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        result = response.json()
        if 'errors' in result:
            raise Exception(f"GraphQL query returned errors: {result['errors']}")
        return result
    else:
        raise Exception(f"GraphQL query failed with status code {response.status_code}, response: {response.content}")

def add_issue_to_project(project_id, issue_id):
    mutation = '''
    mutation($input: AddProjectV2ItemByIdInput!) {
        addProjectV2ItemById(input: $input) {
            item {
                id
            }
        }
    }
    '''
    variables = {
        'input': {
            'projectId': project_id,
            'contentId': issue_id
        }
    }
    result = run_graphql_query(mutation, variables)
    return result['data']['addProjectV2ItemById']['item']['id']

def get_issue_global_id(owner, repo, issue_number):
    query = '''
    query($owner: String!, $repo: String!, $issue_number: Int!) {
        repository(owner: $owner, name: $repo) {
            issue(number: $issue_number) {
                id
            }
        }
    }
    '''
    variables = {
        'owner': owner,
        'repo': repo,
        'issue_number': issue_number
    }
    result = run_graphql_query(query, variables)
    return result['data']['repository']['issue']['id']

def get_project_field_value_id(project_id, field_name, field_value_name):
    query = '''
    query($projectId: ID!) {
        node(id: $projectId) {
            ... on ProjectV2 {
                fields(first: 20) {
                    nodes {
                        ... on ProjectV2SingleSelectField {
                            id
                            name
                            options {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'projectId': project_id
    }
    result = run_graphql_query(query, variables)
    fields = result['data']['node']['fields']['nodes']
    # print("Fields response:", fields)  # Debugging print statement
    for field in fields:
        if field and 'name' in field and field['name'] == field_name:
            for option in field['options']:
                if option['name'] == field_value_name:
                    return field['id'], option['id']
    raise Exception(f"Field or value not found for {field_name} and {field_value_name}")


def set_project_field_value(item_id, field_id, value_id):
    mutation = '''
    mutation($input: UpdateProjectV2ItemFieldValueInput!) {
        updateProjectV2ItemFieldValue(input: $input) {
            projectV2Item {
                id
            }
        }
    }
    '''
    variables = {
        'input': {
            'projectId': GITHUB_PROJECT_ID,
            'itemId': item_id,
            'fieldId': field_id,
            'value': {
                'singleSelectOptionId': value_id
            }
        }
    }
    result = run_graphql_query(mutation, variables)
    return result['data']['updateProjectV2ItemFieldValue']['projectV2Item']['id']

def fetch_collaborators():
    """Fetch the list of collaborators for the repository"""
    url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/collaborators'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [collab['login'] for collab in response.json()]
    else:
        print(f'Failed to fetch collaborators. Response: {response.content}')
        return []

def update_github_issue_comment(issue_number: int, comment: str, slno: int) -> None:
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": comment
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(f"{slno}: Updated issue #{issue_number} with comment")


def get_issue_id(list_of_dicts, sl_number):
    for item in list_of_dicts:
        issue_number = item.get(sl_number)
        if issue_number == sl_number:
            print(issue_number)
            return issue_number
    return None

def read_issues_from_csv(csv_file):
    """Reads issues from a CSV file and creates them on GitHub"""
    collaborators = fetch_collaborators()
    issue_slno_array = []
    issue_id_array = []
    rows = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            slno = row.get('Sl_No', 'N/A')
            request_id = row.get('Request_ID', 'N/A')
            query = row.get('Query', 'N/A')
            title = row['Title']
            current_behavior = row.get('Current_Behavior', 'N/A')
            desired_behavior = row.get('Desired_Behavior', 'N/A')
            GITHUB_STATUS_COLUMN_NAME = row.get('Status', 'N/A')
            GITHUB_CUSTOMER_COLUMN_NAME = row.get('Customer', 'N/A')
            GITHUB_issue_type_COLUMN_NAME = row.get('issue_type', 'N/A')
            GITHUB_PRIORITY_COLUMN_NAME = row.get('Priority', 'N/A')
            GITHUB_ASSIGNEE_COLUMN_NAME = row.get('Assignee', 'N/A')
            GITHUB_REASONING_COLUMN_NAME = row.get('Reasoning', 'N/A')
            dev_eval = row.get('Dev_eval', 'N/A')
            # Setting labels
            # labels = [status, customer, issue_type, priority]
            labels = []
            
            body = f"""
                Request ID: {request_id}
                Query: {query}
                Current Behavior: {current_behavior}
                Desired Behavior: {desired_behavior}
                Reasoning: {GITHUB_REASONING_COLUMN_NAME}
                """
            assignee = GITHUB_ASSIGNEE_COLUMN_NAME
            if assignee not in collaborators:
                print(f"Assignee {assignee} is not a valid collaborator.")
                continue

            if dev_eval == 'x':
                issue_id, issue_url = create_github_issue(title, body, [GITHUB_ASSIGNEE_COLUMN_NAME], labels)
                if issue_id:
                    # print(f"Retrieved issue number: {issue_id}")  # Debugging print statement
                    issue_global_id = get_issue_global_id(GITHUB_OWNER, GITHUB_REPO, issue_id)
                    # print(f"Retrieved global issue ID: {issue_global_id}")
                    project_item_id = add_issue_to_project(GITHUB_PROJECT_ID, issue_global_id)
                    # print(f"Added issue with global ID {issue_global_id} to project {GITHUB_PROJECT_ID}")
                    field_id, value_id = get_project_field_value_id(GITHUB_PROJECT_ID, 'Status', GITHUB_STATUS_COLUMN_NAME)
                    set_project_field_value(project_item_id, field_id, value_id)
                    field_id, value_id = get_project_field_value_id(GITHUB_PROJECT_ID, 'Customer', GITHUB_CUSTOMER_COLUMN_NAME)
                    set_project_field_value(project_item_id, field_id, value_id)
                    field_id, value_id = get_project_field_value_id(GITHUB_PROJECT_ID, 'issue_type', GITHUB_issue_type_COLUMN_NAME)
                    set_project_field_value(project_item_id, field_id, value_id)
                    field_id, value_id = get_project_field_value_id(GITHUB_PROJECT_ID, 'priority', GITHUB_PRIORITY_COLUMN_NAME)
                    set_project_field_value(project_item_id, field_id, value_id)
                    print(f"{slno}: Issue created with id: {issue_id}")
                    issue_slno_array.append(slno)
                    issue_id_array.append(issue_id)
                    row['issue_id'] = issue_id
                    row['close_issue'] = 'N'
                    
        
            if dev_eval != 'x':
                for i in range(len(issue_slno_array)):
                    if dev_eval == issue_slno_array[i]:
                        issue_number = issue_id_array[i]
                        row['close_issue'] = 'N'
                        if issue_number:
                            # Update the comment of the corresponding GitHub issue
                            update_github_issue_comment(issue_number, f"New comment: {body}", slno)
                        else:
                            print(f"No GitHub issue found for sl_number {dev_eval}")

    # update the outputfile
    with open(output_file, mode='w', newline='') as csvfile:
        fieldnames = rows[0].keys()  # Get the fieldnames from the first row
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated CSV file has been saved as {output_file}")


if __name__ == '__main__':
    csv_file = '/Users/divyac/Downloads/GH task csv - 3_6_2024.csv'  
    output_file = '/Users/divyac/Downloads/GH task csv updated.csv'
    read_issues_from_csv(csv_file)

