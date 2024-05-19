import boto3
import os
import math

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')
endpoint_url = os.getenv('AWS_ENDPOINT_URL')
signature_version = os.getenv('AWS_S3_SIGNATURE_VERSION')

s3 = boto3.client(
        's3', 
        aws_access_key_id=access_key_id, 
        aws_secret_access_key=secret_key, 
        region_name=region, 
        config=boto3.session.Config(signature_version=signature_version), 
        endpoint_url=endpoint_url
    )

def upload_progress_callback(bytes_uploaded, file_size, progress_callback):
    percentage = math.ceil((bytes_uploaded / file_size) * 100)
    progress_callback(percentage)

def upload_video_to_s3(file_name, object_name=None, bucket_name="loc8-tech-processed-videos", content_type='video/mp4', progress_callback=None):
    if object_name is None:
        object_name = file_name

    file_size = os.path.getsize(file_name)

    s3.upload_file(file_name, bucket_name, object_name, Callback=lambda bytes_transferred: upload_progress_callback(bytes_transferred, file_size, progress_callback))
    print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' as '{object_name}'")

    signed_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name, 'ResponseContentType': content_type},
        HttpMethod='GET'
    )
    print(signed_url)
    return signed_url

def get_presigned_url(object_name=None, bucket_name="loc8-tech-processed-videos", content_type='video/mp4'):
    signed_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name, 'ResponseContentType': content_type},
        HttpMethod='GET'
    )
    print(signed_url)
    return signed_url
