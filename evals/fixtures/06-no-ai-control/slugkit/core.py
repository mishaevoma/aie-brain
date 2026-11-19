"""Slug generation."""
import re
import unicodedata

_NOT_WORD = re.compile(r"[^a-z0-9]+")


def slugify(text: str, separator: str = "-", max_length: int | None = None) -> str:
    """Return a lower-case ASCII slug of `text`.

    Accents are removed, every run of other characters becomes one separator, and
    a slug cut to `max_length` never ends in the middle of a word or on a separator.
    """
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    words = [word for word in _NOT_WORD.split(ascii_text.lower()) if word]
    if max_length is None:
        return separator.join(words)
    kept: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (len(separator) if kept else 0)
        if length + extra > max_length:
            break
        kept.append(word)
        length += extra
    return separator.join(kept)
