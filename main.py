from io import BytesIO
import base64
from PyPDF2 import PdfFileReader, PdfFileWriter

class EncryptPDF:
  @staticmethod
  def encrypt_pdf(file, username: str, password: str):
    writer = PdfFileWriter()
    reader = PdfFileReader(file)

    if reader.isEncrypted:
        print(f"PDF File already encrypted")
        return True, None
    try:
        # To encrypt all the pages of the input file, you need to loop over all of them
        # and to add them to the writer.
        for page_number in range(reader.numPages):
            writer.addPage(reader.getPage(page_number))
    except PdfReadError as e:
        print(f"Error reading PDF File = {e}")
        return True, None
    # The default is 128 bit encryption (if false then 40 bit encryption).
    writer.encrypt(user_pwd=username, owner_pwd=password, use_128bit=True)

    return False, writer

def encrypt_base64_pdf(base64Pdf: str, username: str, password: str) -> str:
  err, encrypted_pdf = EncryptPDF.encrypt_pdf(
    file=BytesIO(base64.b64decode(base64Pdf)),
    username=username,
    password=password
  )

  if err:
    return ""

  with BytesIO() as stream:
    encrypted_pdf.write_stream(stream)
    stream.seek(0)
    return base64.b64encode(stream.read())

def handler (base64Pdf: str, username: str, password: str) -> str:
  encryptedBase64Pdf = encrypt_base64_pdf(
    base64Pdf=base64Pdf,
    username=username,
    password=password
  )

  return encryptedBase64Pdf
