import os.path
import base64

def get_base64_pdf ():
  with open("/opt/app/src/helpers/doc.pdf", "rb") as doc:
    return base64.b64encode(doc.read())
