import boto3

import logging

log_file_name = f'encrypt_pdf_results.log'
logging.basicConfig(format='%(asctime)s - %(message)s',
                    level=logging.INFO, filename=log_file_name)

class S3:
    @staticmethod
    def upload(bucket_name: str, file_binary, file_uploaded_name: str, content_type=''):
        """
        Upload binary to S3
        :param bucket_name: the bucket name to upload the file
        :param file_binary: the binary of the file that you need to upload in S3
        :param file_uploaded_name: the name of the file saved in s3
        :param content_type: the content type or mime type of the file
        :return:
        """
        logging.info(f'Stating upload_s3 {file_uploaded_name}')
        s3 = boto3.client('s3')
        s3.put_object(Body=file_binary, Bucket=bucket_name, Key=file_uploaded_name, ContentType=content_type)
        logging.info(f'Finishing upload_s3 {file_uploaded_name}')

    @staticmethod
    def get(bucket_name: str, file_name: str):
        """
        Get file from S3
        :param bucket_name: the name of the bucket that you need to get file
        :param file_name: the name of the file that you need to get file in S3
        :return dict with binary on Body field
        """
        logging.info(f'Stating get_s3 {file_name}')
        s3 = boto3.client('s3')
        file = s3.get_object(Bucket=bucket_name, Key=file_name)
        logging.info(f'Finishing get_s3 {file_name}')
        return file