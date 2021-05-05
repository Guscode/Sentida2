
def spacy_download():
    try:
        import da_core_news_lg
    except ModuleNotFoundError:
        print('Downloading language model for the spaCy lemmatization\n'
            "(don't worry, this will only happen once)")
        from spacy.cli import download
        download('da_core_news_lg')


