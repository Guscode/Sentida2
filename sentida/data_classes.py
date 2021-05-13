from __future__ import annotations

from typing import List, Union
from pydantic import BaseModel

from spacy.tokens import Span, Token


class TokenPolarityOutput(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    polarity: float
    token: Token
    span: Span

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(
            repr(v) if a is None else f"{a}={v!r}"
            for a, v in [
                ("polarity", round(self.polarity, 3)),
                ("token", self.token),
                ("span", self.span),
            ]
        )

    def __lt__(self, other: Union[TokenPolarityOutput, float]):
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity < other

    def __gt__(self, other: Union[TokenPolarityOutput, float]):
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity > other


    def __bool__(self):
        return bool(self.polarity) 

    def __eq__(self, other: Union[TokenPolarityOutput, float]):
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity == other


class PolarityOutput(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    negative: float
    neutral: float
    positive: float
    compound: float
    span: Span
    polarities: List[TokenPolarityOutput]

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(
            repr(v) if a is None else f"{a}={v!r}"
            for a, v in [
                ("neg", round(self.negative, 3)),
                ("neu", round(self.neutral, 3)),
                ("pos", round(self.positive, 3)),
                ("compound", round(self.compound, 4)),
                ("span", self.span),
            ]
        )

    def __lt__(self, other: Union[PolarityOutput, float]):
        if isinstance(other, PolarityOutput):
            other = other.compound
        return self.compound < other

    def __gt__(self, other: Union[PolarityOutput, float]):
        if isinstance(other, PolarityOutput):
            other = other.compound
        return self.compound > other

    def __eq__(self, other: Union[PolarityOutput, float]) -> bool:
        if isinstance(other, PolarityOutput):
            other = other.compound
        return self.compound == other