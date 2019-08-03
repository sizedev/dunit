from __future__ import annotations
from typing import Any, Iterable
from decimal import Decimal


class Unit:
    __slots__ = ("_name", "_symbol", "_dimension", "_scale", "_aliases")

    def __init__(self, name: str, symbol: str, dimension: str, scale: Any = 1, aliases: Iterable = None):
        if aliases is None:
            aliases = []
        self._name = name
        self._symbol = symbol
        self._dimension = dimension
        self._scale = Decimal(scale)
        self._aliases = aliases

    @classmethod
    def from_dict(cls, u: dict) -> Unit:
        return Unit(
            name=u["name"],
            symbol=u["symbol"],
            dimension=u["dimension"],
            scale=u["scale"],
            aliases=u["aliases"]
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def dimension(self) -> str:
        return self._dimension

    @property
    def scale(self) -> Decimal:
        return self._scale

    @property
    def aliases(self) -> Iterable:
        return self._aliases.copy()

    def __repr__(self) -> str:
        params = ", ".join((
            f"name={self.name!r}",
            f"symbol={self.symbol!r}",
            f"dimension={self.dimension!r}",
            f"scale={self.scale!r}",
            f"aliases={self.aliases!r}"
        ))
        return f"Unit({params})"
