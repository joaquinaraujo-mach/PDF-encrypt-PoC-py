# Import Libraries
from PyPDF2 import PdfFileReader, PdfFileWriter

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