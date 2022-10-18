
class Static:
    """Base class that enforces static class behavior"""
    def __init__(self):
        exception_string = f"Cannot instantiate static class: {self.__class__.__name__}"
        raise Exception(exception_string)