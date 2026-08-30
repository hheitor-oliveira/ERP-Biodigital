from __future__ import annotations

from domain.enums.status import StatusEnum


class Category:
    def __init__(
        self,
        name: str,
        id: int | None = None,
        status: StatusEnum = StatusEnum.ACTIVE,
    ):
        self._id = id
        self._name = self._normalize_name(name)
        self._status = status

    @staticmethod
    def _normalize_name(name: str) -> str:
        return " ".join(name.strip().split()).upper()

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def status(self) -> StatusEnum:
        return self._status

    @property
    def normalized_name(self) -> str:
        return self._name

    def change_name(self, new_name: str) -> None:
        self._name = self._normalize_name(new_name)

    def change_status(self, new_status: StatusEnum) -> None:
        self._status = new_status

    def is_same_business_name(self, other_name: str) -> bool:
        return self._name == self._normalize_name(other_name)

    @classmethod
    def restore(
        cls,
        name: str,
        id: int | None,
        status: StatusEnum = StatusEnum.ACTIVE,
    ) -> Category:
        category = object.__new__(cls)
        category._name = cls._normalize_name(name)
        category._id = id
        category._status = status
        return category