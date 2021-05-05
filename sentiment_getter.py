from typing import Callable, DefaultDict, Dict, Iterable, List, Optional, Set
from spacy.tokens import Token, Doc, Span
from sentida.constants import (
    AFTER_BUT_SCALAR,
    BEFORE_BUT_SCALAR,
    BUT_WORDS,
    LEXICON,
    INTENSIFIER_DICT,
    C_INCR,
    NEGATIONS,
    N_SCALAR,
)
import math


def make_txt_getter(lemmatize: bool, lowercase: bool) -> Callable:
    def get_lower_lemma(token: Token) -> str:
        return getattr(token, "lemma_")

    def get_lemma(token: Token) -> str:
        return getattr(token, "lemma_")

    def get_lower_txt(token: Token) -> str:
        return getattr(token, "text").lower()

    def get_txt(token: Token) -> str:
        return getattr(token, "text")

    if lemmatize:
        if lowercase:
            return get_lower_lemma
        return get_lemma
    if lowercase:
        return get_lower_txt
    return get_txt


def make_intensifier_getter(
    lemmatize: bool = True, lowercase: bool = True, intensifiers=INTENSIFIER_DICT
):
    """"""
    t_getter = make_txt_getter(lemmatize, lowercase)

    if not Doc.has_extension("is_cap_diff"):
        Doc.set_extension("is_cap_diff", getter=allcap_differential_getter)

    def get_booster_scalar(token: Token):
        """
        get booster score for token.
        """
        t = t_getter(token)
        if t in INTENSIFIER_DICT:
            scalar = INTENSIFIER_DICT[t]
            if token.is_upper and token.doc.is_cap_diff:
                scalar += C_INCR
            return scalar
        else:
            return 0.0


def allcap_differential_getter(doc: Doc) -> bool:
    """
    Check whether just some words in the doc are ALL CAPS
    :returns: `True` if some but not all items in `words` are ALL CAPS
    """
    is_different = False
    allcap_words = 0
    for word in doc:
        if word.isupper():
            allcap_words += 1
    cap_differential = len(doc) - allcap_words
    if 0 < cap_differential < len(doc):
        is_different = True
    return is_different


def make_valance_getter(
    lemmatize: bool = True,
    lowercase: bool = True,
    lexicon=LEXICON,
    cap_differential: Optional[float] = C_INCR,
) -> Callable:

    t_getter = make_txt_getter(lemmatize, lowercase)

    def lemma_valence_getter(token: Token) -> float:
        valence = 0
        t = t_getter(token)
        if t in lexicon:
            return LEXICON[t]
        return 0.0

    def cap_diff_valence_getter(token: Token) -> float:
        valence = token._.raw_valence
        if token.is_upper and token.doc.is_cap_diff:
            if valence > 0:
                valence += cap_differential
            else:
                valence -= cap_differential
        return valence

    if cap_differential:
        if not Token.has_extension("raw_valence"):
            Token.set_extension("raw_valence", getter=lemma_valence_getter)
        if not Doc.has_extension("is_cap_diff"):
            Doc.set_extension("is_cap_diff", getter=allcap_differential_getter)
        return cap_diff_valence_getter
    else:
        return lemma_valence_getter


def make_is_negation(
    lemmatize: bool = True, lowercase: bool = True, negations=NEGATIONS
) -> Callable:
    t_getter = make_txt_getter(lemmatize, lowercase)

    def is_negatation(token: Token) -> bool:
        """
        Determine if token is negation words
        """
        t = t_getter(token)
        return t in negations


def make_contains_negatation_getter():
    if not Token.has_extension("is_negatation"):
        Token.set_extension("is_negatation", getter=make_contains_negatation_getter())

    def contains_negatation(span: Span) -> bool:
        """
        Determine if input contains negation words
        """
        for t in span:
            if t.is_negation is True:
                return True
        return False


def make_is_negated_getter(lookback: int = 3) -> Callable:
    if not Span.has_extension("contains_negatation"):
        Span.set_extension(
            "contains_negatation", getter=make_contains_negatation_getter()
        )

    def is_negated_getter(token: Token) -> bool:
        """
        Determine if token is negated
        """
        if token.doc[token.idx - lookback, token.idx]._.contains_negatation:
            return True

    return is_negated_getter


def make_token_polarity_getter(
    lemmatize: bool = True,
    lowercase: bool = True,
    lexicon: Dict[str] = LEXICON,
    intensifiers: Dict[str] = INTENSIFIER_DICT,
    negation_scalar: float = N_SCALAR,
    lookback_intensities: List[float] = [1.0, 0.95, 0.90],
    **kwargs
):
    """
    lookback_intensities (list): How long to look back for negations and boosters (length). Intensities indicate the how much to weight each booster.
    the intensities ([1.0, 0.95, 0.90]) and lookback distance (3) is emperically derived (Hutto and Gilbert, 2014).
    """
    t_getter = make_txt_getter(lemmatize, lowercase)
    lookback = len(lookback_intensities)

    if not Token.has_extension("valence"):
        Token.set_extension(
            "valence",
            getter=make_valance_getter(lemmatize, lowercase, lexicon, **kwargs),
        )
    if not Token.has_extension("is_negated"):
        Token.set_extension(
            "is_negated", getter=make_is_negated_getter(lookback=lookback)
        )

    def token_polarity_getter(
        token: Token,
    ) -> float:
        valence = token.valance

        if valence:
            for start_i in range(1, lookback + 1):
                # dampen the scalar modifier of preceding words and emoticons
                # (excluding the ones that immediately preceed the item) based
                # on their distance from the current item.
                if token.idx > start_i:
                    prev_token = token.doc[token.idx - start_i]
                    t = t_getter(prev_token)
                    if t not in lexicon:
                        b = prev_token.booster
                        if b != 0:
                            b = b * lookback_intensities[start_i - 1]
                        if valence > 0:
                            valence = valence + b
                        else:
                            valence = valence - b
                if token.is_negated:
                    valence = valence * negation_scalar
        return 0.0

    return token_polarity_getter


def normalize(score, alpha=15):
    """
    Normalize the score to be between -1 and 1 using an alpha that
    approximates the max expected value
    """
    norm_score = score / math.sqrt((score * score) + alpha)
    if norm_score < -1.0:
        return -1.0
    elif norm_score > 1.0:
        return 1.0
    else:
        return norm_score


def questionmark_amplification(text: str) -> float:
    # check for added emphasis resulting from question marks (2 or 3+)
    qm_count = text.count("?")
    qm_amplifier = 0
    if qm_count > 1:
        if qm_count <= 3:
            # (empirically derived mean sentiment intensity rating increase for
            # question marks)
            qm_amplifier = qm_count * 0.18
        else:
            qm_amplifier = 0.96
    return qm_amplifier


def exclamation_amplification(text: str) -> float:
    # check for added emphasis resulting from exclamation points (up to 4 of them)
    ep_count = text.count("!")
    if ep_count > 4:
        ep_count = 4
    # (empirically derived mean sentiment intensity rating increase for
    # exclamation points)
    ep_amplifier = ep_count * 0.292
    return ep_amplifier


def make_punctuation_emphasis_getter(
    questionmark_amplifier: Optional[Callable] = questionmark_amplification,
    exclamation_amplifier: Optional[Callable] = exclamation_amplification,
    **kwargs
):

    if questionmark_amplifier is None:
        questionmark_amplifier = lambda text: 0
    if exclamation_amplifier is None:
        exclamation_amplifier = lambda text: 0

    def punctuation_emphasis_getter(doc: Doc):
        # add emphasis from exclamation points and question marks
        amp = 0
        amp += questionmark_amplification(doc.text)
        amp += exclamation_amplification(doc.text)
        return amp

    return punctuation_emphasis_getter


def make_but_check(
    lemmatize: bool = True,
    lowercase: bool = True,
    but_dict: Set[str] = BUT_WORDS,
    before_but_scalar: float = BEFORE_BUT_SCALAR,
    after_but_scalar: float = AFTER_BUT_SCALAR,
    **kwargs
) -> Callable:

    t_getter = make_txt_getter(lemmatize, lowercase)

    def but_check(doc: Doc, sentiment):
        contains_but = False
        for token in doc:
            t = t_getter(token)
            if t in but_dict:
                but_idx = token.idx
                contains_but = True
        if doc.contains_but is not None:
            for i, s in enumerate(sentiment[0:but_idx]):
                sentiment[i] = s * before_but_scalar
            for i, s in enumerate(sentiment[but_idx:]):
                sentiment[i] = s * after_but_scalar
        return sentiment

    return but_check


def sift_sentiment_scores(sentiments):
    # want separate positive versus negative sentiment scores
    pos_sum = 0.0
    neg_sum = 0.0
    neu_count = 0
    for sentiment_score in sentiments:
        if sentiment_score > 0:
            pos_sum += (
                float(sentiment_score) + 1
            )  # compensates for neutral words that are counted as 1
        if sentiment_score < 0:
            neg_sum += (
                float(sentiment_score) - 1
            )  # when used with math.fabs(), compensates for neutrals
        if sentiment_score == 0:
            neu_count += 1
    return pos_sum, neg_sum, neu_count


def make_doc_polarity_getter(lemmatize: bool = True, lowercase: bool = True, **kwargs):
    """"""
    t_getter = make_txt_getter(lemmatize, lowercase)
    if not Token.has_extension("polarity"):
        Token.set_extension(
            "polarity",
            getter=make_token_polarity_getter(lemmatize, lowercase, **kwargs),
        )

    but_check = make_but_check(lemmatize, lowercase, **kwargs)
    punctuation_emphasis_getter = make_punctuation_emphasis_getter(**kwargs)

    def polarity_getter(
        doc: Doc,
        but_check: Optional[Callable] = but_check,
    ) -> float:
        sentiment = [token.polarity for token in doc]
        sentiment = but_check(doc, sentiment)
        sum_s = float(sum(sentiment))

        if sum_s:
            # compute and add emphasis from punctuation in text
            punct_emph_amplifier = punctuation_emphasis_getter(doc.text)
            if sum_s > 0:
                sum_s += punct_emph_amplifier
            elif sum_s < 0:
                sum_s -= punct_emph_amplifier

            compound = normalize(sum_s)
            # discriminate between positive, negative and neutral sentiment scores
            pos_sum, neg_sum, neu_count = sift_sentiment_scores(sentiment)

            if pos_sum > math.fabs(neg_sum):
                pos_sum += punct_emph_amplifier
            elif pos_sum < math.fabs(neg_sum):
                neg_sum -= punct_emph_amplifier

            total = pos_sum + math.fabs(neg_sum) + neu_count
            pos = math.fabs(pos_sum / total)
            neg = math.fabs(neg_sum / total)
            neu = math.fabs(neu_count / total)
        else:
            compound = 0.0
            pos = 0.0
            neg = 0.0
            neu = 0.0

        sentiment_dict = {
            "neg": round(neg, 3),
            "neu": round(neu, 3),
            "pos": round(pos, 3),
            "compound": round(compound, 4),
        }
        return sentiment_dict

    return polarity_getter
