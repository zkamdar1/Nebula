import boto3
import os

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION")
)

BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

def upload_file_to_s3(file_path, s3_path):
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, s3_path)
        return f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{s3_path}"
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise

'''
def test_s3_connection():
    try:
        # Attempt to list objects in the bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        print(f"Connected to S3 bucket: {BUCKET_NAME}")

        if "Contents" in response:
            print("Files in the bucket:")
            for obj in response["Contents"]:
                print(f"- {obj['Key']}")
        else:
            print("The bucket is empty.")
        return True
    except Exception as e:
        print(f"Error connecting to S3: {e}")
        return False

if __name__ == "__main__":
    # Run the test
    is_connected = test_s3_connection()
    if is_connected:
        print("S3 connection is successful!")
    else:
        print("Failed to connect to S3.")
'''
