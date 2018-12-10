class InvalidStatusChangeException(Exception):

    def __init__(self, message='Invalid status for the order'):
        super().__init__(message)
