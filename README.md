# Project1: AI-Powered Application Builder

## Summary

This project is a sophisticated, AI-driven application that automates the entire lifecycle of building, deploying, and updating web applications. It's designed to streamline the development process by accepting a brief in JSON format, generating the necessary code with LLM assistance, and deploying it to GitHub Pages. The system also includes a robust evaluation mechanism for instructors to assess student submissions, making it an ideal tool for educational settings.

## Features

- **Automated Application Generation:** Leverages LLMs to generate minimal, functional web applications from a simple brief.
- **Seamless GitHub Integration:** Creates public repositories, pushes code, and enables GitHub Pages automatically.
- **Robust Evaluation Workflow:** Includes a secure API for instructors to send requests and an evaluation endpoint to track student progress.
- **Iterative Development:** Supports a "revise" workflow for updating applications with new features or refactoring code.
- **Secure and Scalable:** Built with Flask, the application is designed to be secure, scalable, and easy to maintain.

## Setup

To set up the application locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. **Install dependencies:**
    ```bash
    pip install -r student_app/requirements.txt
    ```
3. **Run the application:**
    ```bash
    python student_app/app.py
    ```
The application will be running at `http://127.0.0.1:5001`.

## Usage

To use the application, send a POST request to the `/api-endpoint` with a JSON payload containing the following:

- `secret`: Your predefined secret for authentication.
- `brief`: A description of the application to be generated.
- `task`: A unique name for the task.
- `evaluation_url`: The URL to which the evaluation results should be sent.

Here's an example `curl` command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "secret": "your_secret_here",
  "brief": "Create a simple webpage.",
  "task": "test-repo",
  "evaluation_url": "https://example.com/notify"
}' http://127.0.0.1:5001/api-endpoint
```
## Code Explanation

The application is built with Flask and is organized into the following components:

- **`app.py`:** The main application file, containing the Flask server, API endpoint, and all the core logic.
- **`generated_app/`:** The directory where the generated application code is stored.
- **`requirements.txt`:** A list of the Python dependencies required for the project.

The application works as follows:
1. The `/api-endpoint` receives a POST request with the application brief.
2. The `handle_request` function validates the secret and calls the `generate_code` function to create the application.
3. The `deploy_to_github` function initializes a Git repository, commits the code, and prepares it for pushing to GitHub.
4. The `notify_evaluation_service` function sends the repository details to the evaluation URL.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
