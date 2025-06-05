from scripts.cognitive_security.cognitive_security import analyze_text


def test_analyze_text_counts():
    text = (
        "This is a catastrophic event. Act now or you will miss out. "
        "Fear and uncertainty are everywhere."
    )
    counts = analyze_text(text)
    assert counts["loaded_language"] == 1
    assert counts["urgency"] == 1
    # "fear" and "uncertainty" should trigger FUD
    assert counts["fud"] == 2
