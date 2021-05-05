

# pos/neg words
# boosters
# caps
# negations
# idioms
# emoticons
# exclamation questionmarks amplyfication

# pos, neg, neu

from typing import Iterable
from spacy.tokens import Token
from sentida.constants import LEXICON

def word_sentiment(token: Token, lexicon=LEXICON) -> float:
    if token.lemma_ in lexicon:
        return LEXICON[token.lemma_]
    return 0.0
    
Token.set_extension("sentiment", getter=word_sentiment)

import spacy
nlp = spacy.load("da_core_news_sm")
doc = nlp("jeg er så glad")

doc[0]._.sentiment

from spacy import displacy
ex = [{"text": "But Google is starting from behind.",
       "ents": [{"start": 4, "end": 10, "label": "ORG"}],
       "title": None}]
displacy.render(ex, style="ent", manual=True)


import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("My name is Kenneth")
html = displacy.render(doc, style="ent")


colors = {
    '0': '#fdfebc',
    '1': '#ffeda0',
    '2': '#fed976',
    '3': '#feb24c',
    '4': '#fd8d3c',
    '5': '#fc4e2a',
    '6': '#e31a1c',
    '7': '#bd0026'}

TPL_TOK = """
<mark class="entity" style="background: {bg}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    {text}
</mark>
"""
ex = [{"text": "But Google is starting from behind.",
       "ents": [{"start": 1, "end": 5, "label": "2"}, {"start": 4, "end": 15, "label": "0"}],
       "title": None}]
html = displacy.render(ex, style="ent", manual=True, options={"colors": colors , 'template': TPL_TOK})


def make_colors(n=10, cmap="RdYlGn"):
    from pylab import cm, matplotlib

    cmap = cm.get_cmap(cmap, n)    # PiYG

    for i in range(cmap.N):
        rgba = cmap(i)
        # rgb2hex accepts rgb or rgba
        yield matplotlib.colors.rgb2hex(rgba)

def print_colors(HEX: Iterable) -> None:
    from IPython.core.display import HTML, display
    for color in HEX:
        display(HTML(f'<p style="color:{color}">{color}</p>'))

print_colors(make_colors())


def render_doc_extenstion(doc):
    colors = {
        '0': '#fdfebc',
        '1': '#ffeda0',
        '2': '#fed976',
        '3': '#feb24c',
        '4': '#fd8d3c',
        '5': '#fc4e2a',
        '6': '#e31a1c',
        '7': '#bd0026'}
    TPL_TOK = """
    <mark class="entity" style="background: {bg}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
        {text}
    </mark>
    """

    ex = [{"text": "But Google is starting from behind.",
        "ents": [{"start": 1, "end": 5, "label": "2"}, {"start": 4, "end": 15, "label": "0"}],
        "title": None}]
    html = displacy.render(ex, style="ent", manual=True, options={"colors": colors , 'template': TPL_TOK})
