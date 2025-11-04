import sys

def get_error_message(error,error_detail:sys):
    _,_,exc_info = error_detail.exc_info()
    filename = exc_info.tb_frame.f_code.co_filename

    error_message = f"Error occured in python script [{filename}] at line no [{exc_info.tb_lineno}] with message [{error}]"

    return error_message

class CustomException(Exception):
    def __init__(self,error,error_detail:sys):
        super().__init__(error)
        self.error_message = get_error_message(error,error_detail)

    def __str__(self):
        return self.error_message