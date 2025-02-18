import os
import requests

# Get environment variables
repo = os.getenv("GITHUB_REPOSITORY")
sha = os.getenv("GITHUB_SHA")
token = os.getenv("GITHUB_TOKEN")
conclusion = os.getenv("CONCLUSION", "neutral")
summary = os.getenv("SUMMARY", "No summary provided.")

# GitHub API URL
url = f"https://api.github.com/repos/{repo}/check-runs"

# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Payload
payload = {
    "name": "Robot Framework Test Run",
    "head_sha": sha,
    "status": "completed",
    "conclusion": conclusion,
    "output": {
        "title": "Test Results Summary",
        "summary": summary
    }
}

# Make the request
response = requests.post(url, json=payload, headers=headers)

# Print response for debugging
print(f"GitHub API Response: {response.status_code}")
print(response.json())

# Exit with error if the request fails
if response.status_code >= 300:
    exit(1)
