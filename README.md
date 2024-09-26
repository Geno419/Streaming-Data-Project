# Streaming Data Project

## Overview

This project retrieves articles from the Guardian API based on user-defined search terms and dates, then publishes the results to AWS Kinesis. It serves as a proof of concept for a media content retrieval application.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Functions](#functions)
- [Non-functional Requirements](#non-functional-requirements)
- [Performance Criteria](#performance-criteria)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Requirements

- Python 3.x
- Boto3
- Requests
- Python-dotenv
- Access to the Guardian API
- AWS credentials for Kinesis

## Setup

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

   ```

2. **Install Dependencies:**
   Ensure that a `requirements.txt` file is present. Install dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   API_KEY=<your_guardian_api_key>
   aws_access_key_id=<your_aws_access_key>
   aws_secret_access_key=<your_aws_secret_key>
   region_name=<your_aws_region>
   stream_name=<your_kinesis_stream_name>
   ```

## Usage

1. **Run the Application:**

   ```bash
   python your_script_name.py
   ```

2. **Input:**

   - Enter a search term when prompted.
   - Optionally, enter a start date in the format `YYYY-MM-DD`. Press Enter to default to today's date.

3. **Output:**
   - The application retrieves and displays up to ten articles from the Guardian API.
   - Users can choose to upload the data to AWS Kinesis.

### Example Input/Output:

- **Input**:
  ```
  Enter your search: climate change
  Click Enter to search from today's date: 2024-09-25
  Enter a start date YYYY-MM-DD:
  ```
- **Output**:
  ```
  ...Searching Guardian for articles on CLIMATE CHANGE from 2024-09-25...
  Article Title: The Impact of Climate Change
  Publication Date: 2024-09-25
  ```

## Functions

### `get_user_input()`

_Prompts the user for a search term and an optional date._

### `validate_date(date_from)`

_Validates the provided date. If invalid, prompts the user to enter a valid date._

### `make_api_request(user_query, date_from, order_by)`

_Makes a GET request to the Guardian API with the specified parameters._

### `handle_response(response)`

_Handles the response from the API request. Returns the list of articles if successful._

### `update_json_file(article_data)`

_Updates a JSON file with the retrieved article data. If the file doesn't exist, it creates one._

### `upload_to_kinesis(json_data, kinesis_client, stream_name)`

_Uploads the provided JSON data to the specified Kinesis stream._

### `set_retention_period(stream_name, hours)`

_Sets the retention period for the Kinesis stream._

### `main()`

_Controls the flow of the application. Handles user input, API requests, and data uploads to Kinesis._

## Non-functional Requirements

- The code is PEP-8 compliant.
- Unit tests are implemented for critical functions.
- Sensitive credentials are managed via environment variables.
- The total size of the module is designed to fit within the limits of AWS Lambda dependencies.

## Performance Criteria

The tool is optimized to handle a maximum of 50 requests per day. Data uploaded to Kinesis is subject to a retention period of three days.
#   S t r e a m i n g - D a t a - P r o j e c t 
 
 #   S t r e a m i n g - D a t a - P r o j e c t 
 
 
