import os
import boto3
from dotenv import load_dotenv
from datetime import date, datetime
import requests
import json
import time

load_dotenv()
API_KEY = os.getenv('API_KEY')
file_path = "data.json"

kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key'),
    region_name=os.getenv('region_name'),
)


def get_user_input():
    user_query = input("Enter your search: ")
    print(" ")
    print(f"Click Enter to search from today's date: {date.today()}")
    date_from = input("Enter a start date YYYY-MM-DD: ")
    return user_query, date_from


def validate_date(date_from):
    while True:
        if date_from == "":
            return date.today().strftime("%Y-%m-%d"), "newest"
        else:
            try:
                datetime.strptime(date_from, "%Y-%m-%d").date()
                return date_from, "newest"
            except ValueError:
                print(" ")
                print(f"{date_from} is not a valid date")
                print(f"Click Enter to search from today's date: {date.today()}")
                date_from = input("Please enter a valid date YYYY-MM-DD: ")


def make_api_request(user_query, date_from, order_by):
    BASE_URL = "https://content.guardianapis.com/search"

    params = {
        "api-key": API_KEY,
        "q": user_query,
        "from-date": date_from,
        "order-by": order_by,
        "show-fields": "all",
        "page-size": 10,
    }
    timeout_duration = 20
    try:
        return requests.get(BASE_URL, params=params, timeout=timeout_duration)
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        return None


def handle_response(response):
    if response.status_code == 200:
        data = response.json()
        return data.get("response", {}).get("results", [])
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


def update_json_file(article_data):
    try:
        with open(file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    if isinstance(existing_data, list):
        existing_data.append(article_data)
    else:
        print("Unexpected data format in the JSON file.")

    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def upload_to_kinesis(json_data, kinesis_client, stream_name):
    json_payload = json.dumps(json_data)

    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json_payload,
            PartitionKey=str(time.time())
        )

    except Exception as e:
        print(f"Error uploading to Kinesis: {e}")
        return None

    return response


def set_retention_period(stream_name, hours):
    response = kinesis_client.increase_stream_retention_period(
        StreamName=stream_name,
        RetentionPeriodHours=hours
    )
    return response


def main():
    stream_name = os.getenv('stream_name')
    set_retention_period(stream_name, 72)

    while True:
        user_query, date_from = get_user_input()
        date_from, order_by = validate_date(date_from)

        print(" ")
        print(f"...Searching Guardian for articles on {(user_query).upper()} "
              f"from {date_from}...")
        print(" ")

        response = make_api_request(user_query, date_from, order_by)
        results = handle_response(response)

        if not results:
            print("No data found...")
            print("")
        else:
            for article in results:
                print(article["webTitle"])
                print(article["webPublicationDate"])
                print(" ")

                upload_data = {
                    "webTitle": article["webTitle"],
                    "webPublicationDate": article["webPublicationDate"],
                    "webUrl": article["webUrl"],
                }
                update_json_file(upload_data)

            while True:
                response = input("Do you want to upload all data to the "
                                 "message board? (yes/no): ").strip().lower()

                if response == "yes":
                    print("")
                    print("uploading....")
                    print("")
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        for record in data:
                            response = upload_to_kinesis(
                                record, kinesis_client, stream_name
                            )

                    print("All Records uploaded")
                    with open(file_path, 'w') as json_file:
                        json.dump([], json_file)
                    break
                elif response == "no":
                    break
                else:
                    print("Incorrect input, please enter yes or no.")

            while True:
                user_input = input("Do you want to make another search "
                                   "(yes/no): ").strip().lower()

                if user_input == "yes":
                    print("")
                    break
                elif user_input == "no":
                    exit()
                else:
                    print("Incorrect input, please enter yes or no.")


if __name__ == "__main__":
    main()
