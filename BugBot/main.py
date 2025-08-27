from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import subprocess
import json
import os
import ollama
import logging
from flask_cors import CORS
from flask import redirect, url_for


app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f').strftime(format)
    except ValueError:
        return value


HISTORY_FILE = "history.json"
UPLOAD_FOLDER = "uploads"
IGNORED_PYLINT_IDS = {"C0303", "C0304", "C0305", "C0114", "C0116"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

PREDEFINED_ERRORS = {
    "C0103": "Variable name should be in snake_case.",
    "W0612": "Unused variable. Remove or use it.",
    "W0621": "Redefining name from outer scope. Use a different name."
}

def init_history():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)

def run_pylint_analysis(file_path):
    try:
        result = subprocess.run(
            ["pylint", "--output-format=json", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20
        )
        if result.stderr:
            app.logger.warning(f"Pylint stderr: {result.stderr}")
        return json.loads(result.stdout.strip()) if result.stdout.strip() else []
    except subprocess.TimeoutExpired:
        app.logger.error("Pylint timed out")
        return []
    except Exception as e:
        app.logger.error(f"Pylint failed: {str(e)}")
        return []

def explain_error(error_type, error_msg, code_snippet):
    if error_type in PREDEFINED_ERRORS:
        return PREDEFINED_ERRORS[error_type]

    try:
        prompt = f"""Explain this Python error briefly:

Error type: {error_type}
Message: {error_msg}

What does it mean and how to fix it?"""

        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": prompt}],
            options={'timeout': 15}
        )
        return response["message"]["content"]
    except Exception as e:
        app.logger.error(f"LLM explanation failed: {str(e)}")
        return "Explanation service unavailable."

def save_to_history(entry):
    try:
        init_history()
        with open(HISTORY_FILE, 'r+') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

            history.append({
                "timestamp": datetime.now().isoformat(),
                **entry
            })
            f.seek(0)
            json.dump(history, f, indent=2)
    except Exception as e:
        app.logger.error(f"History save failed: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if 'code' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files['code']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400

            if not file.filename.lower().endswith('.py'):
                return jsonify({"error": "Only Python (.py) files allowed"}), 400

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()

            
            errors = run_pylint_analysis(filepath)
            grouped_errors = {}

            for error in errors:
                error_id = error.get("message-id", "")
                if error_id in IGNORED_PYLINT_IDS:
                    continue

                if error_id not in grouped_errors:
                    grouped_errors[error_id] = {
                        "type": error_id,
                        "message": error.get("message", ""),
                        "lines": [error.get("line")]
                    }
                else:
                    grouped_errors[error_id]["lines"].append(error.get("line"))

            results = []

            for error_id, error_data in grouped_errors.items():
                explanation = explain_error(
                    error_id,
                    error_data["message"],
                    code
                )

                result = {
                    "type": error_id,
                    "message": error_data["message"],
                    "lines": sorted(set(error_data["lines"])),
                    "explanation": explanation
                }

                results.append(result)
                save_to_history(result)

            return render_template('index.html', results=results, code=code)

        except Exception as e:
            app.logger.error(f"Analysis failed: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

        finally:
            try:
                if 'filepath' in locals() and os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                app.logger.warning(f"File deletion failed: {str(e)}")

    return render_template('index.html')

@app.route('/history')
def history():
    try:
        init_history()
        with open(HISTORY_FILE, 'r') as f:
            history_data = json.load(f)
        return render_template('history.html', history=reversed(history_data))
    except Exception as e:
        app.logger.error(f"History failed: {str(e)}")
        return render_template('history.html', error=str(e))
    
    
@app.route('/clear-history', methods=['POST'])
def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)
        return redirect(url_for('history'))
    except Exception as e:
        app.logger.error(f"Failed to clear history: {str(e)}")
        return render_template('history.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
