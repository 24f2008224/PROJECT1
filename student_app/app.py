from flask import Flask, request, jsonify
import os
import subprocess
import requests
import time

app = Flask(__name__)

# This should be stored securely, e.g., as an environment variable
SECRET = "your_secret_here"

def generate_code(brief, round_num):
    """
    Placeholder for LLM-assisted code generation.
    Generates a simple index.html file based on the brief.
    """
    if not os.path.exists('student_app/generated_app'):
        os.makedirs('student_app/generated_app')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App - Round {round_num}</title>
</head>
<body>
    <h1>Generated Application - Round {round_num}</h1>
    <p>Brief: {brief}</p>
</body>
</html>
"""
    with open('student_app/generated_app/index.html', 'w') as f:
        f.write(html_content)
    print(f"Generated index.html for round {round_num}")


def deploy_to_github(task_name, github_username):
    """
    Initializes a git repository and commits the generated code.
    """
    repo_dir = 'student_app/generated_app'
    repo_name = f"{task_name}"

    if os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository already exists. Skipping initialization.")
    else:
        subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Jules'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.email', 'jules@example.com'], cwd=repo_dir, check=True)

    subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)

    # Check if there are changes to commit
    status_process = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_dir, capture_output=True, text=True, check=True)
    if status_process.stdout:
        subprocess.run(['git', 'commit', '-m', 'Update code based on new brief'], cwd=repo_dir, check=True)
    else:
        print("No changes to commit.")

    commit_sha_process = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo_dir, capture_output=True, text=True, check=True)
    commit_sha = commit_sha_process.stdout.strip()

    repo_url = f"https://github.com/{github_username}/{repo_name}"
    pages_url = f"https://{github_username}.github.io/{repo_name}/"
    return repo_url, commit_sha, pages_url


def notify_evaluation_service(evaluation_url, email, task, round_num, nonce, repo_url, commit_sha, pages_url):
    """
    Sends a POST request to the evaluation service with the repository details.
    """
    payload = {
        "email": email,
        "task": task,
        "round": round_num,
        "nonce": nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    retries = 5
    delay = 1
    for i in range(retries):
        try:
            response = requests.post(evaluation_url, json=payload, timeout=10)
            response.raise_for_status()
            with open("notification.log", "a") as f:
                f.write(f"Successfully notified evaluation service for round {payload['round']}. Status code: {response.status_code}\n")
            return
        except requests.exceptions.RequestException as e:
            with open("notification.log", "a") as f:
                f.write(f"Error notifying evaluation service for round {payload['round']}: {e}\n")
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                with open("notification.log", "a") as f:
                    f.write("Failed to notify evaluation service after multiple retries.\n")


@app.route('/api-endpoint', methods=['POST'])
def handle_request():
    data = request.get_json()
    if not data or 'secret' not in data or data['secret'] != SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    round_num = data.get('round', 1)

    if 'brief' in data:
        generate_code(data['brief'], round_num)

    if 'task' in data:
        repo_url, commit_sha, pages_url = deploy_to_github(data['task'], "24f2008224")

        if 'evaluation_url' in data:
            notify_evaluation_service(
                data['evaluation_url'],
                data.get('email', '24f2008224@ds.study.iitm.ac.in'),
                data['task'],
                round_num,
                data.get('nonce'),
                repo_url,
                commit_sha,
                pages_url
            )

    return jsonify({"message": "Request received successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
