class SpyneException(Exception):
    pass

class ClassMissingError(SpyneException):
    pass

class SerializerMissingError(ClassMissingError):
    pass