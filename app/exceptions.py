class AppException(Exception):
    status_code: int = 400
    detail: str = "Application error"


class NotFoundError(AppException):
    status_code = 404
    detail = "Resource not found"


class CustomerNotFoundError(NotFoundError):
    detail = "Customer not found"


class RestaurantNotFoundError(NotFoundError):
    detail = "Restaurant not found"


class DishNotFoundError(NotFoundError):
    detail = "Dish not found"


class OrderNotFoundError(NotFoundError):
    detail = "Order not found"


class CategoryNotFoundError(NotFoundError):
    detail = "Category not found"


class ReviewNotFoundError(NotFoundError):
    detail = "Review not found"


class ValidationError(AppException):
    status_code = 400
    detail = "Validation error"


class DishNotAvailableError(ValidationError):
    detail = "Dish is not available"


class DishRestaurantMismatchError(ValidationError):
    detail = "Dish does not belong to this restaurant"


class InvalidOrderStatusError(ValidationError):
    detail = "Invalid order status transition"


class InvalidDateRangeError(ValidationError):
    detail = "date_from must be earlier than date_to"


class ReviewNotAllowedError(ValidationError):
    detail = "Customer cannot review this restaurant"