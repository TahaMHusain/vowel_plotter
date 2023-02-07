from collections import defaultdict
from pathlib import Path
import csv

import numpy as np

from get_formants import get_formants
from parse_textgrid import parse_textgrid
from extract_vowels import extract_vowels

ascii2ipa = {
    'IY1': 'i',
    'IH1': 'ɪ',
    'EY1': 'e',
    'EH1': 'ɛ',
    'AE1': 'æ',
    'AA1': 'ɑ',
    'OW1': 'o',
    'AH1': 'ʌ',
    'UH1': 'ʊ',
    'UW1': 'u',
}

def main(sound_path: str, textgrid_path: str, output_path: str = None, reps: int = 3):
    if not output_path:
        output_path = Path(f'data/{Path(sound_path).stem}.csv')
    vowel_times = parse_textgrid(textgrid_path)
    vowels_formants = extract_vowels(sound_path, vowel_times)

    median_formants = defaultdict(lambda: defaultdict(list))
    for vowel, formants_tuple_list in vowels_formants.items():
        for formants_tuple in formants_tuple_list:
            for i, formant_list in enumerate(formants_tuple):
                median = np.nanmedian(formant_list, axis=0)
                median_formants[vowel][f'f{i}'].append(median)



    with open(output_path, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)

        # Header row
        writer.writerow(['vowel', 'F1', 'F2'])

        for vowel, formant_dict in median_formants.items():
            for i in range(reps):
                writer.writerow([ascii2ipa[vowel], formant_dict['f1'][i], formant_dict['f2'][i]])

if __name__ == '__main__':
    main('data/corpus/speaker1.wav', 'data/corpus_aligned/speaker1.TextGrid')