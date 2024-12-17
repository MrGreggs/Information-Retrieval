from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Example dataset
data = [
    {
        "name": "John Doe",
        "date": "2024-12-15",
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

@app.route('/api/search', methods=['POST'])
def search():
    request_data = request.json
    print("Request Data:", request_data)

    keyword = request_data.get("keyword", "").lower()  # Convert keyword to lowercase
    period = request_data.get("period", "")
    start_date = request_data.get("startDate", "")
    end_date = request_data.get("endDate", "")

    print("Search Keyword:", keyword)

    try:
        # Parse the dates if provided (only if not empty)
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    filtered_data = []
    for item in data:
        print("Checking item:", item)

        # Check if the keyword exists in any of the fields (name, period, party, speech)
        if keyword:
            if not any(
                keyword in str(item[field]).lower() for field in ["name", "period", "party", "speech"]
            ):
                print(f"Keyword '{keyword}' not found in any field for item: {item['name']}")
                continue

        # Period filter (ignore if blank)
        if period and item["period"] != period:
            print(f"Skipping item {item['name']} due to period mismatch.")
            continue

        # Date range filter (ignore if blank)
        if item.get("date"):
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
            print("Item date:", item_date)  # Debugging: Print item_date
            if start_date_obj and item_date < start_date_obj:
                print(f"Skipping item {item['name']} due to start date filter.")
                continue
            if end_date_obj and item_date > end_date_obj:
                print(f"Skipping item {item['name']} due to end date filter.")
                continue

        filtered_data.append(item)

    print("Filtered Data:", filtered_data)
    response = {"results": filtered_data}
    return jsonify(response)

# Function to read CSV file and load data
def load_data_from_csv():
    data = []
    with open('data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "name": row["member_name"],
                "date": row["sitting_date"],
                "period": row["parliamentary_period"],
                "party": row["political_party"],
                "speech": row["speech"]
            })
    return data

# Load data once at the start
#data = load_data_from_csv()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
