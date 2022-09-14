# Encrypt PDF with PyPDF2

This POC create a encrypted PDF file from S3 original file (no protected file) and upload to same S3 bucket

- [PyPDF2](https://github.com/py-pdf/PyPDF2)

## Installation locally

Please check `src/run.py` file

### With Virtualenv

- Activate virtualenv `source ./virtualenv/bin/active`
- `pip install -r requeriments.txt`
- `python run.py`

### With docker

- Set in `dockerfile` AWS envs (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
- `docker build -t python-encode-pdf .`
- `docker run python-encode-pdf`

## Lambda

- Lambda file is `run_lambda.py`
- Set env `S3_BUCKET_DESTINATION_NAME` with encrypted PDF destination bucket name
- When you upload a file in `no-encrypted-pdf` bucket trigger a event to this lambda and encrypt pdf and upload to `encrypt-pdf` bucket with the same filename but added `_encrypyted.pdf`
  anything- The filename format needed is: `####_d_11111111_####.pdf` where 11111111 is document number without DV and #### is anything

PDF upload to S3 bucket 'encrypt-pdf' (change in run.py)
