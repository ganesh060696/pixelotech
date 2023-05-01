class UserUtils:

    @classmethod
    def strip_phone_number(cls, ph_no: str):
        return ph_no.replace(" ", "")
