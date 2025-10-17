class EmailTakenError(Exception): pass
class NotFoundError(Exception): pass
class UserNotFoundError(NotFoundError): pass
class PlaceNotFoundError(NotFoundError): pass
class AmenityNotFoundError(NotFoundError): pass
class ReviewNotFoundError(NotFoundError): pass
