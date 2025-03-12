# app.py - Flask application to serve the Market Analysis Dashboard

# [1] Import and configure Flask
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Define the path to the data directory (where JSON files are stored)
DATA_DIR = os.path.join('.', 'data')
TEMPLATE_DIR = os.path.join('.', 'templates')

# [2] Serve the main dashboard page at the root route ("/")
@app.route("/")
def dashboard():
    """
    Route for the root URL ("/").
    Renders the index.html template from the /templates folder.
    This is the main page of the Market Analysis Dashboard.
    """
    return render_template('index.html')

# [3] API endpoints to serve JSON data

@app.route("/api/marketShare")
def market_share_data():
    """
    API endpoint for /api/marketShare.
    Reads and returns the contents of data/marketShare.json as JSON.
    """
    try:
        with open(os.path.join(DATA_DIR, 'marketShare.json'), 'r') as f:
            market_share_json = f.read()
            return jsonify(eval(market_share_json)) #eval is used to parse the json which is in string format
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

@app.route("/api/revenueTrends")
def revenue_trends_data():
    """
    API endpoint for /api/revenueTrends.
    Reads and returns the contents of data/revenueTrends.json as JSON.
    """
    try:
        with open(os.path.join(DATA_DIR, 'revenueTrends.json'), 'r') as f:
            revenue_trends_json = f.read()
            return jsonify(eval(revenue_trends_json)) #eval is used to parse the json which is in string format
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

@app.route("/api/marketSegmentation")
def market_segmentation_data():
    """
    API endpoint for /api/marketSegmentation.
    Reads and returns the contents of data/marketSegmentation.json as JSON.
    """
    try:
        with open(os.path.join(DATA_DIR, 'marketSegmentation.json'), 'r') as f:
            market_segmentation_json = f.read()
            return jsonify(eval(market_segmentation_json)) #eval is used to parse the json which is in string format
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

# [4] Serve static files (optional - if you have files in a /static folder)
# Flask automatically serves files from a 'static' folder in the same directory as app.py
# No explicit route definition needed unless you want to customize static URL path

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode for development

"""
Recommended Repository Structure for the Market Analysis Dashboard Project:

market-analysis-dashboard/  (Root directory of the repository)
├── app.py                  (Flask application file)
├── templates/              (Folder for HTML templates)
│   └── index.html          (Main dashboard HTML file)
├── data/                   (Folder for JSON data files)
│   ├── marketShare.json        (Market share data)
│   ├── revenueTrends.json      (Revenue trends data)
│   └── marketSegmentation.json (Market segmentation data)
├── static/                 (Optional folder for static assets like CSS, images, JS files)
│   └── (Optional static files here, e.g., style.css, script.js, images/)
└── README.md               (Optional README file for project description and instructions)

Explanation of the structure:

- `market-analysis-dashboard/`: This is the main project folder. You would initialize your Git repository in this folder.
- `app.py`: This file contains the Python Flask application code that sets up the routes, serves the HTML template, and provides the API endpoints for the JSON data.
- `templates/`: This folder stores all HTML templates for your Flask application. In this case, it contains `index.html`, which is the main dashboard page. Flask will look for HTML templates in this folder by default.
- `data/`: This folder is dedicated to storing your data files. We place the JSON files (`marketShare.json`, `revenueTrends.json`, `marketSegmentation.json`) here to keep data separate from the application code.
- `static/`: This folder is for static files like CSS stylesheets, JavaScript files, images, or any other files that the web application might need to serve directly to the browser. While not strictly necessary for the current setup, it's good practice to have it for potential future expansion (e.g., if you want to add custom CSS to style your dashboard further or add more client-side JavaScript).
- `README.md`: A good practice to include a README file at the root of your project. This file can contain information about your project, how to set it up, how to run it, etc. It's helpful for anyone (including yourself in the future) who needs to understand and use your project.

This structure helps to keep your project organized, making it easier to manage and maintain as it grows. It clearly separates the application logic (in `app.py`), presentation layer (`templates/index.html`), data (`data/`), and static assets (`static/`).
"""
