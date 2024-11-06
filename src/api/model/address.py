from typing import Optional


class Address:
    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        country: str,
        postal_code: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
