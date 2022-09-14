# Import Libraries
import os
from io import BytesIO
from datetime import datetime
import urllib.parse

import boto3
from PyPDF2 import PdfFileReader, PdfFileWriter

S3_BUCKET_DESTINATION_NAME = os.environ['S3_BUCKET_DESTINATION_NAME']

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

class EncryptPDF:
    @staticmethod
    def is_encrypted(input_file: str) -> bool:
        """Checks if the inputted file is encrypted using PyPDF4 library"""
        with open(input_file, 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file, strict=False)
            return pdf_reader.isEncrypted

    @staticmethod
    def encrypt_pdf(input_file, password: str):
        """
        Encrypts a file using PyPDF4 library.
        Precondition: File is not encrypted.
        """
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(input_file)
        if pdf_reader.isEncrypted:
            print(f"PDF File {input_file} already encrypted")
            return False, None, None
        try:
            # To encrypt all the pages of the input file, you need to loop over all of them
            # and to add them to the writer.
            for page_number in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page_number))
        except PdfReadError as e:
            print(f"Error reading PDF File {input_file} = {e}")
            return False, None, None
        # The default is 128 bit encryption (if false then 40 bit encryption).
        pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
        return True, pdf_reader, pdf_writer

def generate_password(input_filename: str):
    """
    Generate password from filename by last 4 digits from the document number without DV in filename (####_d_11111111_####)
    """
    substr_start = input_filename.index('_d_')+3
    substr_end = input_filename.index('_', input_filename.index('_d_')+3)

    password = input_filename[substr_start:substr_end]
    return password[len(password)-4:]

def processFile(sourceBucket: str, sourceKey: str):
    #Get file from s3
    file_object = S3.get(sourceBucket, sourceKey)

    if file_object['Body']:
        fs = file_object['Body'].read()
        #Encrypt PDF
        result, pdf_reader, pdf_writer = EncryptPDF.encrypt_pdf(
                input_file=BytesIO(fs), password=generate_password(sourceKey))

        # Encryption completed successfully
        if result:
            # Save the new PDF on S3 directly
            with BytesIO() as bytes_stream:
                pdf_writer.write(bytes_stream)
                bytes_stream.seek(0)
                S3.upload(S3_BUCKET_DESTINATION_NAME, bytes_stream, f'{sourceKey}_encrypted.pdf', 'application/pdf')
                return true

def lambda_handler(event, context):
    sourceBucket = event['Records'][0]['s3']['bucket']['name']
    sourceKey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    result = processFile(sourceBucket, sourceKey)
    if result:
        return {
            'status': 200
        }
    else:
        return {
            'status': 500
        }
    
