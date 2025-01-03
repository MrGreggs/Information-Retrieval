from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import csv
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_speech_ids(keyword):
    file_path = "inverted_index.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if keyword in data:
            documents = data[keyword].get("documents", [])
            speech_ids = list({doc["speech_id"] for doc in documents})
            return speech_ids
        else:
            return []  # Keyword not found
    
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

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

    # Retrieve speech IDs from inverted index
    speech_ids = get_speech_ids(keyword)

    if not speech_ids:
        return jsonify({"results": []})  # No matching speech IDs found

    # Load data from medium.csv and match rows based on speech IDs
    filtered_data = []
    with open('medium.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Get the headers
        headers = [header.strip() for header in headers]  # Strip any whitespace
        for idx, row in enumerate(reader, start=0):  # Enumerate rows with 0-based index
            if idx in speech_ids:  # Check if the current row index matches a speech ID
                if len(row) != len(headers):
                    print(f"Row length mismatch at index {idx}: {row}")
                data_row = dict(zip(headers, row))  # Convert row to dictionary with headers as keys
                filtered_data.append(data_row)

    # Filter based on the period if provided
    if period:
        filtered_data = [item for item in filtered_data if item.get("parliamentary_period", "").strip() == period]

    # Filter based on date range if provided
    if start_date_obj or end_date_obj:
        filtered_data = [
            item for item in filtered_data if
            (not start_date_obj or datetime.strptime(item.get("sitting_date", ""), "%d/%m/%Y") >= start_date_obj) and
            (not end_date_obj or datetime.strptime(item.get("sitting_date", ""), "%d/%m/%Y") <= end_date_obj)
        ]

    return jsonify({"results": filtered_data})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
