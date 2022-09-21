import base64
from run import encrypt_base64_pdf

def get_base64_pdf() -> str:
  with open("/opt/app/src/in-memory/doc.pdf", "rb") as doc:
    return base64.b64encode(doc.read())

def save_base64_pdf(base64Pdf: str):
  with open("/opt/app/src/in-memory/doc-encrypted.pdf", "wb") as doc:
    doc.write(base64.b64decode(base64Pdf))

encryptedBase64Pdf = encrypt_base64_pdf(
  base64Pdf=get_base64_pdf(),
  username="mach",
  password="1234"
)

save_base64_pdf(encryptedBase64Pdf)
