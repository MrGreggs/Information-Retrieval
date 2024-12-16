from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Example dataset
data = [
    {
        "name": "John Doe",
        "date": "2023-01-15",
        "period": "2021-2024",
        "party": "Party A",
        "speech": "We must work together to address these issues."
    },
    {
        "name": "Jane Smith",
        "date": "2022-05-10",
        "period": "2021-2024",
        "party": "Party B",
        "speech": "This is a pivotal moment in our nation's history."
    },
    {
        "name": "Sam Johnson",
        "date": "2018-11-22",
        "period": "2018-2021",
        "party": "Party C",
        "speech": "Innovation will drive our economy forward."
    },
]

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search():
    request_data = request.json
    keyword = request_data.get("keyword", "").lower()
    period = request_data.get("period", "")
    start_date = request_data.get("startDate", "")
    end_date = request_data.get("endDate", "")

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    filtered_data = []
    for item in data:
        if keyword and keyword not in item["speech"].lower():
            continue
        if period and item["period"] != period:
            continue
        if item.get("date"):
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
            if start_date_obj and item_date < start_date_obj:
                continue
            if end_date_obj and item_date > end_date_obj:
                continue
        filtered_data.append(item)

    response = {"results": filtered_data}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

