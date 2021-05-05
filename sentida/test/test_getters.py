import pytest

import spacy
from spacy.tokens import Token
from .utils import spacy_download

from sentida.getters import make_valance_getter

@pytest.fixture
def nlp_model():
    spacy_download("da_core_news_sm")
    nlp = spacy.load("da_core_news_sm")
    return nlp


EXAMPLE = ["jeg er glad", "jeg er GLAD", "jeg er sur"]


@pytest.fixture()
def test_valence_getter():
    Token.set_extension("valence", make_valance_getter())
    
    docs = [nlp_model(e) for e in EXAMPLE[:3]]

    assert docs[0][2].valence
    assert docs[0][2].valence < docs[1][2].valence
    assert docs[2][2].valence < docs[0][2].valence