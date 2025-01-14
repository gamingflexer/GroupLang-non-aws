import boto3, json
import os
from telegram import Bot

import sys
sys.path.insert(0, os.getcwd())

from chalicelib.credentials import PRIVATE_BUCKET as BUCKET

AWS_REGION = "eu-west-1"
ENDPOINT_URL = "http://localhost:4566"

def register_bot(bot_id, bot_token):
    # s3 = boto3.client("s3")
    s3 = boto3.client("s3", region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)

    # Construct the object key with the desired format
    object_key = "bots_id_to_token.json"

    # Retrieve the existing content (if any)
    try:
        response = s3.get_object(Bucket=BUCKET, Key=object_key)
        existing_content = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        existing_content = {}

    # Add the new sentence to the existing content
    existing_content[bot_id] = bot_token

    # Store the updated content in the object
    s3.put_object(Bucket=BUCKET, Key=object_key, Body=json.dumps(existing_content))
    print(f"Registered bot {bot_id} with token {bot_token}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python register_bot.py BOT_TOKEN")
        exit(1)
    bot_token = sys.argv[1]
    bot = Bot(bot_token)
    bot_username = bot.get_me().username

    register_bot(bot_username, bot_token)
    print("done")
