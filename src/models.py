from dataclasses import dataclass


@dataclass
class Document:
    filename: str
    content: str


@dataclass
class Chunk:
    filename: str
    text: str