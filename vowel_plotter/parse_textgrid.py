from pathlib import Path
from collections import defaultdict

from praatio import textgrid


DEFAULT_VOWELS = {'IY1', 'IH1', 'EY1', 'EH1', 'AE1', 'AA1', 'OW1', 'AH1', 'UH1', 'UW1'}

def parse_textgrid(path: str, vowel_set: set = None):
    vowel_times = defaultdict(list)
    if not vowel_set:
        vowel_set = DEFAULT_VOWELS
    tg = textgrid.openTextgrid(Path(path), False)
    vowel_tier = tg.tierDict['phones']
    for start, end, phone in vowel_tier.entryList:
        if phone in vowel_set:
            vowel_times[phone].append((start, end))

    print(vowel_times)

if __name__ == '__main__':
    path = 'data/corpus_aligned/speaker1.TextGrid'
    parse_textgrid(path)
