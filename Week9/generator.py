"""This module provides an example function to generate passwords.
"""
__author__ = "Karsten Tolle"
__credits__ = "with some help of ChatGPT"

import random
import string

animal_emoji = [
    "🐶",  # Hund
    "🐱",  # Katze
    "🐭",  # Maus
    "🐹",  # Hamster
    "🐰",  # Hase
    "🦊",  # Fuchs
    "🐻",  # Bär
    "🐼",  # Panda
    "🦁",  # Löwe
    "🐯",  # Tiger
    "🐨",  # Koala
    "🐸",  # Frosch
    "🐵",  # Affe
    "🙈",  # Affe sieht nichts
    "🐔",  # Huhn
    "🐧",  # Pinguin
    "🐦",  # Vogel
    "🦆",  # Ente
    "🦉",  # Eule
    "🦅",  # Adler
    "🦇",  # Fledermaus
    "🐺",  # Wolf
    "🐗",  # Wildschwein
    "🐴",  # Pferd
    "🦄",  # Einhorn
    "🐝",  # Biene
    "🦋",  # Schmetterling
    "🐌",  # Schnecke
    "🐢",  # Schildkröte
    "🐍",  # Schlange
    "🦎",  # Eidechse
    "🦂",  # Skorpion
    "🦀",  # Krebs
    "🦑",  # Tintenfisch
    "🐙",  # Oktopus
    "🐠",  # Fisch
    "🐬",  # Delfin
    "🐳",  # Wal
    "🐋",  # Blauwal
    "🦈",  # Hai
]


def generate_password(
    length: int,
    use_lower=True,
    use_upper=True,
    use_digits=True,
    use_symbols=False,
    use_emojis=False
) -> str:
    """ Generates a password of a given length, based on different character sets as \
    defined during call of the function. 
        """
    chars = ""  # char sets will be added here

    # include the relevant char sets into: chars
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    if use_emojis:
        for i in animal_emoji:
            chars += i

    if len(chars) == 0:
        raise ValueError("Keine Zeichengruppe ausgewählt")

    password = ""  # contains the generated pw
    for _ in range(length):
        password += random.choice(chars)
    return password