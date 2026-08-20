class DomainException(Exception):
    status_code = 400
    message = "Đã có lỗi xảy ra"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class EmailAlreadyExistsError(DomainException):
    status_code = 400
    message = "Email đã được sử dụng"


class RoleNotConfiguredError(DomainException):
    status_code = 500
    message = "Chưa cấu hình Role Customer trong hệ thống"


class InvalidCredentialsError(DomainException):
    status_code = 401
    message = "Email hoặc mật khẩu không đúng"


class AccountLockedError(DomainException):
    status_code = 403
    message = "Tài khoản đã bị khóa"