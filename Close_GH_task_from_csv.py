import csv
import requests


# Function to close a GitHub issue
def close_github_issue(issue_number, repo, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"state": "closed"}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"Issue #{issue_number} closed successfully.")
    else:
        print(f"Failed to close issue #{issue_number}. Response: {response.content}")

# Configuration
input_file = '/Users/divyac/Downloads/GH task csv updated.csv'
repo = 'slanglabs/polyglot'
token = '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'  

# Read from the CSV file
with open(input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        issue_id = row['issue_id']
        close = row['close_issue']
        
        if close == 'y' or close == 'Y':
            close_github_issue(issue_id, repo, token)
        elif close == 'n' or close == 'N':
            print(f"Issue #{issue_id} not closed (close column value is 'n').")
