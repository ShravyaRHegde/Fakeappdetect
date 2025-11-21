from flask import Flask, render_template_string, send_file
from detect import get_app_risks
import json

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Fake App Detector</title>
    <style>
        body {
            font-family: 'Times New Roman', Times, serif;
            margin: 0;
            padding: 30px;
            background: linear-gradient(135deg, #e0f7fa, #f9f9f9);
            color: #222;
        }

        h2 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 30px;
            color: #2c3e50;
        }

        .download-btn {
            position: fixed;
            top: 20px;
            right: 30px;
            padding: 12px 18px;
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
        }
        .download-btn:hover { background-color: #0056b3; }

        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 25px;
            justify-content: center;
        }

        .card {
            border-radius: 15px;
            padding: 20px;
            width: 400px;
            color: #222;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            background-color: #fdfdfd;
        }
        .card:hover { transform: translateY(-8px); box-shadow: 0 15px 25px rgba(0,0,0,0.25); }

        .risk-high { background-color: #ffcccc; color: #721c24; }
        .risk-medium { background-color: #fff2b3; color: #856404; }
        .risk-low { background-color: #b3ffcc; color: #155724; }

        .card p { margin: 6px 0; font-size: 1rem; }
        .card p b { font-weight: 700; }
        .reasons { font-style: italic; margin-bottom: 10px; }

        table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Times New Roman', Times, serif;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #999;
            padding: 6px 8px;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background-color: #a8d0e6; /* pastel blue */
            color: #222;
        }

        td {
            background-color: #d7ebf7; /* lighter pastel blue */
            color: #222;
        }
    </style>
</head>
<body>
    <h2>Fake App Detector</h2>
    <a href="/download" class="download-btn">Download JSON Evidence</a>
    <div class="container">
        {% for entry in results %}
        <div class="card {% if entry.risk_level=='High' %}risk-high{% elif entry.risk_level=='Medium' %}risk-medium{% else %}risk-low{% endif %}">
            <p><b>App:</b> {{ entry.app_name }}</p>
            <p><b>Package:</b> {{ entry.package_name }}</p>
            <p><b>Publisher:</b> {{ entry.publisher }}</p>
            <p><b>Risk Score:</b> {{ entry.risk_score }}</p>
            <p><b>Risk Level:</b> {{ entry.risk_level }}</p>
            <p class="reasons"><b>Reasons:</b> {{ entry.reasons|join(', ') if entry.reasons else '-' }}</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Signal</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {% for k,v in entry.details.items() %}
                    <tr>
                        <td>{{ k.replace('_',' ').title() }}</td>
                        <td>{{ v }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    results = get_app_risks("candidates.csv")
    return render_template_string(HTML_PAGE, results=results)

@app.route("/download")
def download():
    data = get_app_risks("candidates.csv")
    with open("evidence.json", "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)
    return send_file("evidence.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
