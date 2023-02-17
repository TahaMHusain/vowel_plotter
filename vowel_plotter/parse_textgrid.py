from pathlib import Path
from collections import defaultdict

from praatio import textgrid


def parse_textgrid(path: str, vowel_set: set) -> dict[str: list]:
    vowel_times = defaultdict(list)
    tg = textgrid.openTextgrid(Path(path), False)

    # Grab the TextGrid tier containing vowel sound times
    # If using an older version of praatio (<6.0), change getTier to tierDict
    vowel_tier = tg.getTier('phones')
    # If using an older version of praatio (<6.0), change vowel_tier.entries to something else - read the docs, geez
    for start, end, phone in vowel_tier.entries:
        # If the sound is in the list of vowels, add the start and end times to the list of start-end tuples
        if phone in vowel_set:
            vowel_times[phone].append((start, end))

    return vowel_times


if __name__ == '__main__':
    path = 'data/corpus_aligned/speaker1.TextGrid'
    parse_textgrid(path)
