

---

Python Code Linter & Explainer (Flask + LLM)

This project is a Flask-based web application that analyzes Python code, detects issues using Pylint, and generates clear, beginner-friendly explanations with the help of a local Large Language Model (LLM) via Ollama (CodeLlama).
Unlike standard linters, which only output error codes and technical messages, this tool explains why the error occurred, how to fix it, and best practices to avoid it in the future.

---

Features

Static Code Analysis: Runs [Pylint](https://pylint.pycqa.org/) on submitted Python code to find errors, warnings, and style violations.
LLM-Powered Explanations:

Predefined explanations for common Pylint error codes.
AI-generated explanations (via Ollama + CodeLlama) for more complex errors.
Persistent History (No Database): Stores all past analysis sessions (code + results) in a simple `sessions.json` file.
Web Interface (Bootstrap-based):

Text area for entering code.
“Analyze” button to run Pylint + LLM explanations.
Results panel with detailed error breakdown.
History sidebar to revisit past analyses.

---

Core Workflow

1. User submits Python code through the web UI.
2. Flask backend saves the code temporarily and runs Pylint.
3. Each error is either:

Mapped to a predefined human-readable explanation, or
Sent to Ollama (CodeLlama) for a natural language explanation, fix, and best practices.
4. Results, along with the original code, are saved to `sessions.json`.
5. The frontend (HTML + Bootstrap + JS) displays current results and a clickable history panel to revisit old sessions.

---

Tech Stack

Backend: Python, Flask, Subprocess (Pylint integration)
LLM: [Ollama](https://ollama.ai) with CodeLlama model
Storage: JSON file (`sessions.json`)
Frontend: HTML, CSS, Bootstrap, JavaScript

---

Project Structure


project_root/
├── app.py             
├── explanations.py    
├── sessions.json      
├── templates/        
│   ├── base.html
│   └── index.html
└── static/           
    └── style.css



---

Example Use Case

Upload or paste a Python script.
See raw Pylint errors.
Get instant explanations for errors (why they occurred, how to fix them, and prevention tips).
Revisit past sessions from the history panel to track improvements in your code.

---

Why Use This?

This project is ideal for:

Students & Beginners → who want to learn from errors, not just fix them.

Educators → who want a teaching aid for code quality and debugging.

Developers → who want linting + AI explanations in a simple, local setup.

---

