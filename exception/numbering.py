class InvalidIdError(Exception):
    def __init__(self):
        super().__init__('ID must be int value or {str}-{int} format')
