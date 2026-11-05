from __future__ import annotations

from pydantic import BaseModel


def compress(data: BaseModel) -> str:
    return data


def decompress(data: str) -> BaseModel:
    typeify(data)
    return data


def typeify(data: str) -> BaseModel:
    return data
