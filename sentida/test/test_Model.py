import sentida

def test_polarity():
    polarity = sentida.PolarityModel()

    p = polarity("jeg er glad")
    assert p["compound"] > 0
