from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to read CSV file and load data
def load_data_from_csv():
    data = []
    with open('clean.csv', mode='r', encoding='utf-8') as file:
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
data = load_data_from_csv()

@app.route('/api/search', methods=['POST'])
def search():
    request_data = request.json

    keyword = request_data.get("keyword", "").lower()  # Convert keyword to lowercase
    period_dash = request_data.get("period", "").strip()  # Ensure no extra whitespace
    period = period_dash.replace('-', ' ')
    start_date = request_data.get("startDate", "")
    end_date = request_data.get("endDate", "")

    try:
        # Parse the dates if provided (only if not empty)
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    print("Keyword:", keyword)
    print("Period:", period)
    print("Start Date:", start_date_obj)
    print("End Date:", end_date_obj)

    filtered_data = []
    for item in data:
        # Check if the keyword exists in any of the fields
        if keyword and not any(keyword in str(item[field]).lower() for field in ["name", "period", "party", "speech"]):
            continue

        print("Checking keyword match for item:", item["name"])

        # Period filter
        if period and item["period"].strip() != period:  # Directly match without dash
            print(f"Expected period {period} but found period {item['period']}")
            continue

        print(f"Period match for {item['period']}")

        # Date range filter
        if item.get("date"):
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
            if start_date_obj and item_date < start_date_obj:
                print(f"Item date {item_date} is before start date {start_date_obj}")
                continue
            if end_date_obj and item_date > end_date_obj:
                print(f"Item date {item_date} is after end date {end_date_obj}")
                continue

        filtered_data.append(item)

    print(f"Total results found: {len(filtered_data)}")
    return jsonify({"results": filtered_data})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
