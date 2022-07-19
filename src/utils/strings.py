import unicodedata


def normalize_text(text: str, upper=True, remove_extra_spaces=True):
    text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .strip()
    )
    if remove_extra_spaces:
        text = " ".join(text.split())

    return text.upper() if upper else text


def sanitize_attribute(attribute: str):
    if "220" in attribute or "200" in attribute:
        return "220"
    elif "110" in attribute or "127" in attribute:
        return "110"
    elif "BIVOLT" in attribute.upper():
        return "BIVOLT"
    return ""
