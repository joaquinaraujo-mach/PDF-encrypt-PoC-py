# Encrypt PDF with PyPDF2 (Fork)

## API to use script
The base64Pdf would be "PDF", encryptedBase64Pdf would be "Encrypted PDF"
````
from run import encrypt_base64_pdf

encryptedBase64Pdf = encrypt_base64_pdf(
  base64Pdf=get_base64_pdf(),
  username="mach",
  password="1234"
)
````
