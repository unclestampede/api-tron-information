from app import models

ADDRESS_EXAMPLE = "TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC"
NOT_EXIST_ADDRESS_EXAMPLE = "TNoAuE6JPbXY1VWhZyV2kVqKTyZaU9dddd"
INVALID_ADDRESS_EXAMPLE = "invalidadress"

ADD_INFO_EXAMPLE = models.TronInfoCreate(address=NOT_EXIST_ADDRESS_EXAMPLE, balance=1.234, energy=2000, bandwidth=600)
