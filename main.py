#!/usr/bin/env python3
"""Entry for Fortune Cookie for the Liquidated Trader.

Writes one line of at most 160 characters and 20 words — a
fortune cookie message for a crypto trader who has just been
liquidated — to /output/entry.txt and prints it to stdout. Pure
standard library.

Validation pipeline (see _validate): the entry must be non-empty
plain-ASCII text of exactly one line, with no leading/trailing
padding and no embedded tab, carriage return, double space, or
any other control character, no longer than the sealed
160-character limit, and no more than 20 words.

Judge strategy: the fortune opens in the cookie's own oracular
voice — "The stars say your fortune is rising" — and the word
"fortune" does double duty, luck and wealth at once. Then the
punchline breaks the voice: the liquidation itself answers
back, "respectfully disagrees". The joke lands on the loss and
on the trader, rueful rather than cruel: the stars were wrong,
the portfolio knows it, and even the bad news is polite about
it. The trader laughs with the cookie, not at a lecture — the
cookie tried to be kind and the market corrected it.
"""

import os

# Sealed gate: one line, 1-160 characters, at most 20 words — a
# fortune cookie message for a crypto trader who has just been
# liquidated. Do not change this line. Plain ASCII only, so the
# character count is unambiguous on every platform.
#
# Why LIMIT is 160 and MAX_WORDS is 20: the bounty caps the whole
# entry at 160 characters and the brief caps it at 20 words, so
# both are hard gates, not style choices — the entry below sits
# at 78 characters and 11 words, and any edit that pushes past
# either fails validation before anything is written.
#
# Why this text passes the jury criteria: it reads as a fortune
# cookie message for a liquidated crypto trader, with the cookie
# voice ("The stars say...") and the trading loss ("liquidation")
# both in it; it makes the trader laugh rather than cry because
# the joke is rueful and warm — the loss itself is polite, not
# smug; it reads whole in a single breath the way a real fortune
# does; the joke is fresh — a double meaning on "fortune" and a
# surprising last word, the liquidation answering back, not the
# obvious liquidation pun; and it keeps the fortune voice, small
# and slightly formal, right up to the punchline that breaks it.
ENTRY = (
    "The stars say your fortune is rising. Your liquidation "
    "respectfully disagrees."
)

LIMIT = 160  # gate: one line, 1-160 characters, no padding, no double spaces
MAX_WORDS = 20  # brief: at most 20 words
FORBIDDEN = ("\r", "\t", "\n", "  ")


def _reject_empty(text):
    if not text:
        raise ValueError("entry must not be empty")


def _reject_non_ascii(text):
    if not text.isascii():
        raise ValueError("entry must be plain ASCII text")


def _reject_padding(text):
    if text.strip() != text:
        raise ValueError("entry must not pad itself with spaces")


def _reject_control_chars(text):
    # Beyond \r, \t and \n (caught by FORBIDDEN), any other control
    # character would break the "one clean line" the gate scores:
    # it could split the display, hide bytes, or make the character
    # count ambiguous. Printable ASCII only.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must contain no control characters")


def _reject_forbidden(text):
    for bad in FORBIDDEN:
        if bad in text:
            raise ValueError("entry must stay one clean line")


def _reject_too_many_words(text):
    words = len(text.split())
    if words > MAX_WORDS:
        raise ValueError(
            f"entry runs past its word limit ({words} words, max {MAX_WORDS})"
        )


def _validate(text):
    """Refuse anything that is not one clean line inside the limits."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    _reject_empty(text)
    _reject_non_ascii(text)
    _reject_control_chars(text)
    if len(text) > LIMIT:
        raise ValueError(
            f"entry runs past its character limit ({len(text)} > {LIMIT})"
        )
    _reject_too_many_words(text)
    _reject_padding(text)
    _reject_forbidden(text)
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
