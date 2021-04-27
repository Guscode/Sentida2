from .vaderSentiment_da import SentimentIntensityAnalyzer
from .Model import PolarityModel
import spacy
try:
    nlp = spacy.load('da_core_news_lg')
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)", file=stderr)
    from spacy.cli import download
    download('da_core_news_lg')
