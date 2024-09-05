class FileUploadError(Exception):
    """Base class for file upload related errors."""
    def __init__(self, message="An error occurred during file upload"):
        self.message = message
        super().__init__(self.message)

class FileNotFoundError(FileUploadError):
    """Exception raised when no file part is found in the request."""
    def __init__(self):
        super().__init__("No file part in the request")

class FileNameError(FileUploadError):
    """Exception raised when the uploaded file has no name."""
    def __init__(self):
        super().__init__("No selected file")

class InvalidFileFormatError(FileUploadError):
    """Exception raised when the uploaded file is not a .txt file."""
    def __init__(self):
        super().__init__("Invalid file format")

class FileReadError(FileUploadError):
    """Exception raised when there is an error reading the file."""
    def __init__(self, message):
        super().__init__(message)