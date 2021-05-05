from typing import Optional

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from .vaderSentiment_da import SentimentIntensityAnalyzer
from .getters import polarity_getter
from .utils import spacy_download


class PolarityModel:
    def __init__(self, nlp: Optional[Language] = None):
        if nlp is None:
            spacy_download(("da_core_news_lg")
            self.nlp = spacy.load("da_core_news_lg")
        Doc.set_extension("polarity", getter=polarity_getter, force=True)

    def __call__(self, text: str) -> dict:
        doc = self.nlp(text)
        return doc._.polarity
