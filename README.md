## Streaming Data Project

This README.md file serves as a guide for the Streaming Data Project, which retrieves articles from the Guardian API and publishes them to AWS Kinesis.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Functions](#functions)
- [Non-functional Requirements](#non-functional-requirements)

## Requirements

The project requires the following:

- Python 3.x
- Boto3 library
- Requests library
- Python-dotenv library
- Access to the Guardian API with an API key
- AWS credentials with access to Kinesis

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Geno419/Streaming-Data-Project.git
   cd Streaming-Data-Project
   ```

2. **Install Dependencies:**

   Install dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a file named `.env` in the root directory. This file should contain sensitive information that won't be committed to version control. Add the following lines, replacing placeholders with your actual values:

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
   python script.py
   ```

2. **Input:**

   - The application will prompt you to enter a search term.
   - Optionally, you can enter a start date in YYYY-MM-DD format. Pressing Enter defaults to the start of the year.

3. **Output:**

   - The application retrieves and displays up to ten articles from the Guardian API matching your search criteria.
   - You will be prompted to choose whether you want to upload the retrieved data to AWS Kinesis.

### Example Input/Output:

**Input:**

```
Enter your search: climate change
Click Enter to search from today's date: 2024-09-25
Enter a start date YYYY-MM-DD:
```

**Output:**

```
...Searching Guardian for articles on CLIMATE CHANGE from 2024-09-25...
Article Title: The Impact of Climate Change
Publication Date: 2024-09-25
...

Do you want to upload retrieved data to Kinesis? (y/n):
```

## Functions

The project utilizes various functions to perform specific tasks:

- `get_user_input()`: Prompts the user for search term and optional date.
- `validate_date(date_from)`: Validates the provided date format.
- `make_api_request(user_query, date_from, order_by)`: Constructs and sends a GET request to the Guardian API with specified parameters.
- `handle_response(response)`: Processes the response from the API request and returns a list of articles if successful.
- `update_json_file(article_data)`: Updates a JSON file with retrieved article data (creates the file if it doesn't exist).
- `upload_to_kinesis(json_data, kinesis_client, stream_name)`: Uploads provided JSON data to the specified Kinesis stream.
- `set_retention_period(stream_name, hours)`: Sets the retention period for the Kinesis stream (in hours).
- `main()`: Controls the overall application flow, handling user interaction, API calls, and Kinesis uploads.

## Non-functional Requirements

The project adheres to the following non-functional requirements:

- Code adheres to PEP-8 style guidelines for Python.
- Critical functions are covered by unit tests.
- Sensitive credentials are stored and managed securely using environment variables.
- The total module size is designed to be compatible with AWS Lambda deployment size limitations.
