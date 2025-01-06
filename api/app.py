import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import csv
import json

app = Flask(__name__)
CORS(app)  # enable CORS 

# function to read and process the JSON file
def get_speech_ids(file_path, keyword):
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

# route for searching
@app.route('/api/search', methods=['POST'])
def search():
    request_data = request.json
    keyword = request_data.get("keyword", "").lower()  # convert keyword to lowercase
    period_dash = request_data.get("period", "").strip()  # remove extra whitespace
    period = period_dash.replace('-', ' ')
    start_date = request_data.get("startDate", "")
    end_date = request_data.get("endDate", "")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    # retrieve speech IDs from inverted index
    inverted_index_path = sys.argv[2]  # Get the inverted index file path
    speech_ids = get_speech_ids(inverted_index_path, keyword)

    if not speech_ids:
        return jsonify({"results": []})  # no matching speech IDs found

    filtered_data = []
    initial_csv_path = sys.argv[1]  # Get the inital.csv file path
    with open(initial_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # get the headers
        headers = [header.strip() for header in headers]
        for idx, row in enumerate(reader, start=0):
            if idx in speech_ids:
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
    app.run(port=5000, debug=True)
