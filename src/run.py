from helpers.encrypt_pdf import EncryptPDF
from helpers.S3 import S3
from helpers.utils import Utils

# Import Libraries
from io import BytesIO
from datetime import datetime

S3_BUCKET_NAME = 'no-encrypted-pdf'
S3_DESTINATION_BUCKET_NAME = 'encrypt-pdf'
INPUT_FILE = 'without_password_d_19194798_asd.pdf'
OUTPUT_FILE = 'without_password_d_19194798_asd'

if __name__ == '__main__':
    #Get file from s3
    file_object = S3.get(S3_BUCKET_NAME, INPUT_FILE)

    if file_object['Body']:
        fs = file_object['Body'].read()
        #Encrypt PDF
        result, pdf_reader, pdf_writer = EncryptPDF.encrypt_pdf(
                input_file=BytesIO(fs), password=Utils.generate_password(INPUT_FILE))

        # Encryption completed successfully
        if result:
            # Save the new PDF on S3 directly
            with BytesIO() as bytes_stream:
                pdf_writer.write(bytes_stream)
                bytes_stream.seek(0)
                S3.upload(S3_DESTINATION_BUCKET_NAME, bytes_stream, f'{OUTPUT_FILE}_encrypted.pdf', 'application/pdf')
        