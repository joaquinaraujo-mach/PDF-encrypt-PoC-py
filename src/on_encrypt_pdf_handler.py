
import os
from helpers.get_base64_pdf import get_base64_pdf

def handler ():
  if os.path.isdir("/opt/app/src/in-memory") != True:
    os.mkdir("/opt/app/src/in-memory")

  base64Pdf = get_base64_pdf()
  print(base64Pdf)

handler()
