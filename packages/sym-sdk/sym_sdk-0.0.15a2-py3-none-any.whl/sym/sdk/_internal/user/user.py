from typing import List, Optional

from sym.sdk import User, UserIdentity


class BaseUserIdentity(UserIdentity):
    def __init__(self, provider: str, user_id: str, external_service_identifier: str):
        self._provider = provider
        self._user_id = user_id
        self._external_service_identifier = external_service_identifier

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def external_service_identifier(self) -> str:
        return self._external_service_identifier


class BaseUser(User):
    def __init__(
        self,
        username: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        identities: Optional[List[UserIdentity]] = None,
    ):
        self._username = username
        self._email = email
        self._first_name = first_name or ""
        self._last_name = last_name or ""
        self._identities = identities or []

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    def identity(self, provider: str) -> Optional[UserIdentity]:
        return next((i for i in self._identities if i.provider == provider), None)
