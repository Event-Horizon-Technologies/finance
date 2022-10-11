"""
Base class that if you inhert it and call super__init__, will force that class to be non-instantiable
"""
class Static:
    def __init__(self):
        exception_string = f"Cannot instantiate static class: {self.__class__.__name__}"
        raise Exception(exception_string)