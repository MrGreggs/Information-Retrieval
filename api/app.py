import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import csv
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# function to read and process the JSON file
def get_speech_ids(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        normalized_data = {k.lower().strip(): v for k, v in data.items()}
        keyword_normalized = keyword.lower().strip()

        if keyword_normalized in normalized_data:
            documents = normalized_data[keyword_normalized].get("documents", [])
            speech_ids = list({doc["speech_id"] for doc in documents})
            return speech_ids
        else:
            return []

    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# route for searching
@app.route('/api/search', methods=['POST'])
def search():
    request_data = request.json
    keyword = request_data.get("keyword", "").lower()  # convert keyword to lowercase
    period_dash = request_data.get("period", "").strip()  # remove no extra whitespace
    period = period_dash.replace('-', ' ')
    start_date = request_data.get("startDate", "")
    end_date = request_data.get("endDate", "")

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # retrieve speech IDs from inverted index
    inverted_index_path = sys.argv[1]  # Get the file path from command-line argument
    speech_ids = get_speech_ids(inverted_index_path, keyword)

    if not speech_ids:
        return jsonify({"results": []})  # no matching speech IDs found

    filtered_data = []
    with open('medium.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Get the headers
        headers = [header.strip() for header in headers]  
        for idx, row in enumerate(reader, start=0):  
            if idx in speech_ids:  
                if len(row) != len(headers):
                    print(f"Row length mismatch at index {idx}: {row}")
                data_row = dict(zip(headers, row))  
                filtered_data.append(data_row)

    if period:
        filtered_data = [item for item in filtered_data if item.get("parliamentary_period", "").strip() == period]

    if start_date_obj or end_date_obj:
        filtered_data = [
            item for item in filtered_data if
            (not start_date_obj or datetime.strptime(item.get("sitting_date", ""), "%d/%m/%Y") >= start_date_obj) and
            (not end_date_obj or datetime.strptime(item.get("sitting_date", ""), "%d/%m/%Y") <= end_date_obj)
        ]

    return jsonify({"results": filtered_data})

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Please provide the path to the inverted index JSON file as a command-line argument.")
        sys.exit(1)
    app.run(port=5000, debug=True)
