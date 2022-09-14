class Utils:
    @staticmethod
    def generate_password(input_filename: str):
        """
        Generate password from filename by last 4 digits from the document number without DV in filename (####_d_11111111_####)
        """
        substr_start = input_filename.index('_d_')+3
        substr_end = input_filename.index('_', input_filename.index('_d_')+3)

        password = input_filename[substr_start:substr_end]
        return password[len(password)-4:]