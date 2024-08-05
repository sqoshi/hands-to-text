from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


class HandBox(NamedTuple):
    lt: Point
    rd: Point


class ClassedHandBox(NamedTuple):
    box: HandBox
    class_name: str
