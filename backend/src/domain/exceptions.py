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


class InvalidResetTokenError(DomainException):
    status_code = 400
    message = "Mã xác nhận không đúng hoặc đã hết hạn"


class UserNotFoundError(DomainException):
    status_code = 404
    message = "Không tìm thấy tài khoản với email này"


class AddressNotFoundError(DomainException):
    status_code = 404
    message = "Không tìm thấy địa chỉ"


class CustomerNotFoundError(DomainException):
    status_code = 404
    message = "Không tìm thấy khách hàng"


class StationNotFoundError(DomainException):
    status_code = 404
    message = "Không tìm thấy trạm"

    
class PackageReceiptNotFoundError(DomainException):
    status_code = 404
    message = "Không tìm thấy thông tin xác nhận package"


class PackageAlreadyReceivedError(DomainException):
    status_code = 400
    message = "Package đã được xác nhận đến trạm"


class InvalidStationStatusError(DomainException):
    status_code = 400
    message = "Trạng thái trạm không hợp lệ"

class AIServiceUnavailableError(DomainException):
    status_code = 503
    message = "Dịch vụ AI hiện không khả dụng, đã sử dụng ước tính mặc định"