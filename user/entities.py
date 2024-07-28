from dataclasses import dataclass

@dataclass
class UserDataServiceEntity:
    name: str
    email: str
    password: str
    phone: str


@dataclass
class UserUpdateDataServiceEntity:
    name: str
    email: str
    phone: str