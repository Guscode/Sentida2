from .vaderSentiment_da import SentimentIntensityAnalyzer
from spacy.tokens import Doc

analyser = SentimentIntensityAnalyzer()


def polarity_getter(doc: Doc, lemmatization: bool = True) -> dict:
    """
    extract polarity using a Danish implementation of Vader.

    Example:
    Doc.set_extension("vader_da", getter=da_vader_getter)
    # fetch result
    doc._.vader_polarity
    """
    if lemmatization:
        polarity = analyser.polarity_scores(doc.text, tokenlist=[t.lemma_ for t in doc])
    else:
        polarity = analyser.polarity_scores(doc.text, tokenlist=[t.text for t in doc])
    return polarity
