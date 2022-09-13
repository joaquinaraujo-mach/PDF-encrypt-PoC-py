from encrypt_pdf import EncryptPDF
from S3 import S3

# Import Libraries
from io import BytesIO
from datetime import datetime

S3_BUCKET_NAME = 'encrypt-pdf'
INPUT_FILE = 'without_password.pdf'
PASSWORD = '123asd'
OUTPUT_FILE = 'encrypted'

if __name__ == '__main__':
    #Get file from s3
    file_object = S3.get(S3_BUCKET_NAME, INPUT_FILE)

    if file_object['Body']:
        fs = file_object['Body'].read()
        #Encrypt PDF
        result, pdf_reader, pdf_writer = EncryptPDF.encrypt_pdf(
                input_file=BytesIO(fs), password=PASSWORD)

        # Encryption completed successfully
        if result:
            # Save the new PDF on S3 directly
            with BytesIO() as bytes_stream:
                pdf_writer.write(bytes_stream)
                bytes_stream.seek(0)
                S3.upload(S3_BUCKET_NAME, bytes_stream, f'{OUTPUT_FILE}_{datetime.now().isoformat()}.pdf', 'application/pdf')
        