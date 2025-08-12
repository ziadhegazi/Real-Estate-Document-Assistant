import sys
# from logger import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Generates a detailed error message including file name, line number, and error message.

    Args:
        error (Exception): The exception object.
        error_detail (sys): The sys module, used to get traceback info.

    Returns:
        str: A formatted string with the error details.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in python script name [{file_name}], line number [{exc_tb.tb_lineno}], error message [{str(error)}]"
    return error_message

class CustomException(Exception):
    """
    A custom exception class that captures detailed error information.
    """
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        Returns the detailed error message when the exception is printed.
        """
        return self.error_message

# Testing exception.py file /// python src/exception.py
"""
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomException(e, sys)
"""