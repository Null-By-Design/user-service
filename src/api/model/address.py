from typing import Optional


class Address:
    def __init__(
        self,
        id: Optional[int] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postal_code: Optional[str] = None,
    ):
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
