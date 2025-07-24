import sys
from typing import Optional


class CustomException(Exception):
    """
    Custom exception class for detailed error tracking.
    Captures message, original exception, filename, and line number.
    """

    def __init__(self, message: str, error_detail: Optional[Exception] = None):
        """
        Initializes the CustomException.

        Args:
            message (str): Custom error message.
            error_detail (Optional[Exception]): Original exception object (optional).
        """
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(
        message: str, error_detail: Optional[Exception]
    ) -> str:
        """
        Generates a detailed error message including file name and line number.

        Args:
            message (str): Custom error message.
            error_detail (Optional[Exception]): Original exception object (optional).

        Returns:
            str: Formatted detailed error message.
        """
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown File"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown Line"
        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        Returns:
            str: Detailed error message.
        """
        return self.error_message
