import os
import shutil
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from vowel_plotter.align import align
from vowel_plotter.parse_textgrid import parse_textgrid
from vowel_plotter.extract_vowels import extract_vowels
from vowel_plotter.draw_plot import draw_plot

# Translate ARPA symbols to IPA
arpa2ipa = {
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


def main(sound_path: str,
         corpus_path: str = None,
         dictionary_path: str = None,
         acoustic_path: str = None,
         aligned_path: str = None):
    if not dictionary_path:
        if os.path.exists('data/MFA/pretrained_models/dictionary/english_us_arpa.dict'):
            dictionary_path = 'data/MFA/pretrained_models/dictionary/english_us_arpa.dict'
        elif os.path.exists('../data/MFA/pretrained_models/dictionary/english_us_arpa.dict'):
            dictionary_path = '../data/MFA/pretrained_models/dictionary/english_us_arpa.dict'
        else:
            raise ValueError('Dictionary not found')

    if not acoustic_path:
        if os.path.exists('data/MFA/pretrained_models/acoustic/english_us_arpa.zip'):
            acoustic_path = 'data/MFA/pretrained_models/acoustic/english_us_arpa.zip'
        elif os.path.exists('../data/MFA/pretrained_models/acoustic/english_us_arpa.zip'):
            acoustic_path = '../data/MFA/pretrained_models/acoustic/english_us_arpa.zip'
        else:
            raise ValueError('Acoustic model not found')

    if not corpus_path:
        # MFA won't rerun alignment unless the folder is a different name from last time >:(
        randy = random.randint(1, 100)
        corpus_path = f'data/corpus_{randy}'
    if not os.path.exists(corpus_path):
        os.makedirs(corpus_path)
        shutil.copy2('data/transcript.lab', os.path.join(corpus_path, 'speaker1.lab'))

    if not os.path.exists(os.path.join(corpus_path, 'speaker1.wav')):
        shutil.copy2(sound_path, os.path.join(corpus_path, 'speaker1.wav'))

    if not aligned_path:
        aligned_path = corpus_path + f'_aligned'
    if not os.path.exists(aligned_path):
        os.makedirs(aligned_path)

    align(corpus_path, dictionary_path, acoustic_path, aligned_path)

    textgrid_path = Path(aligned_path).joinpath(f'speaker1.TextGrid')

    vowel_times = parse_textgrid(textgrid_path)
    vowels_formants = extract_vowels(sound_path, vowel_times)
    table = pd.DataFrame(columns=['vowel', 'F1', 'F2'])

    median_formants = defaultdict(lambda: defaultdict(list))
    for vowel, formants_tuple_list in vowels_formants.items():
        for formants_tuple in formants_tuple_list:
            formants_row = {}
            for i, formant_list in enumerate(formants_tuple):
                median = np.nanmedian(formant_list, axis=0)
                median_formants[vowel][f'f{i}'].append(median)
                formants_row[f'f{i}'] = median
            table = pd.concat([table, pd.Series(
                {'vowel': arpa2ipa[vowel], 'F1': formants_row['f1'], 'F2': formants_row['f2']}).to_frame().T],
                              ignore_index=True)

    shutil.rmtree(corpus_path)
    shutil.rmtree(aligned_path)
    draw_plot(table)


if __name__ == '__main__':
    main('data/corpus')
