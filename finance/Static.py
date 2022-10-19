
class Static:
    """Base class that enforces static class behavior"""
    def __new__(cls):
        exception_string = f"Cannot instantiate static class: {cls.__name__}"
        raise Exception(exception_string)