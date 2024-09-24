# Welcome to Atrium's AI Agent Development Platform

This guide will help you get started with running your AI agent using the Atrium platform. Below are the steps to set up and run your development server.

## Getting Started

Before you start, ensure you have the necessary environment set up. This includes having your AWS credentials configured correctly, as the AI agents you'll be working on will leverage AWS services like Bedrock.

## Running the Development Server

Follow these steps to run the server and start processing requests:

### 1. Navigate to Your Project Directory

First, ensure you're in the correct working directory where your project files are located.

```bash
cd /root/code_workspace
```

### 1.1. Install Required Dependencies
```
source /root/poetry-venv/bin/activate
```

### 2. Install Required Dependencies

If you haven't already installed the necessary dependencies, you can do so using `pip`. These dependencies include `FastAPI` and `Uvicorn`, which are essential for running the development server.

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fastapi uvicorn boto3
```

### 3. Start the Server

Now, run the `main.py` script to start the development server. Uvicorn will handle incoming requests and serve your AI agent.

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This command does the following:
- **`main:app`**: Specifies that Uvicorn should use the `app` object from the `main.py` file.
- **`--host 0.0.0.0`**: Makes the server accessible externally, which is useful if you're working within a container or remote environment.
- **`--port 8000`**: Sets the server to listen on port 8000. You can adjust this if needed.
- **`--reload`**: Enables automatic reloading of the server when changes to your code are detected. This is particularly useful during development.

### 4. Accessing the Server

Once the server is running, you can access it at:

```
http://localhost:8000
```

If you're running the server in a remote environment, replace `localhost` with the appropriate IP address.

### 5. Stopping the Server

To stop the server, press `CTRL+C` in the terminal where it's running.

## Important Notes

- **AWS Credentials**: Ensure your AWS credentials are set up correctly for the Bedrock client to function properly. This is crucial for your AI agent's interaction with AWS services.

---

This guide should help you quickly set up and run your development environment. If you encounter any issues or have questions, don't hesitate to reach out to our support team or consult our documentation.

Happy coding!

--- 

This README provides a friendly introduction and clear, step-by-step instructions, ensuring new developers can get started quickly.
