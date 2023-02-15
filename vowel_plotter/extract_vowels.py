from pathlib import Path
from collections import defaultdict

from parselmouth import Sound

from vowel_plotter.get_formants import get_formants

def extract_vowels(path:str, vowel_times: dict) -> dict[str: list]:
    all_vowel_formants = defaultdict(list)
    sound = Sound(str(Path(path).resolve()))
    for vowel in vowel_times:
        for start, end in vowel_times[vowel]:
            vowel_segment = sound.extract_part(start, end)
            vowel_formants = get_formants(vowel_segment)
            all_vowel_formants[vowel].append(vowel_formants)

    return all_vowel_formants
