from collections import defaultdict
from pathlib import Path
import csv
import subprocess
from io import BytesIO
from PIL import Image

from cairosvg import svg2png
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

from align import align
from parse_textgrid import parse_textgrid
from extract_vowels import extract_vowels

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


def main(output_path: str = None,
         reps: int = 3,
         corpus_path: str = None,
         dictionary_path: str = '/home/Mark/Documents/MFA/pretrained_models/dictionary/english_us_arpa.dict',
         acoustic_path: str = '/home/Mark/Documents/MFA/pretrained_models/acoustic/english_us_arpa.zip',
         aligned_path: str = None):
    speaker = '2'

    if not corpus_path:
        corpus_path = f'data/corpus{speaker}'
    if not aligned_path:
        aligned_path = corpus_path + f'{speaker}_aligned'

    align(corpus_path, dictionary_path, acoustic_path, aligned_path)



    sound_path = Path(corpus_path).joinpath(f'speaker{speaker}.wav')
    textgrid_path = Path(aligned_path).joinpath(f'speaker{speaker}.TextGrid')

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
                writer.writerow([arpa2ipa[vowel], formant_dict['f1'][i], formant_dict['f2'][i]])

    subprocess.call(f'/usr/bin/Rscript vowel_plotter.R data/speaker{speaker}.csv', shell=True)

    img = cv2.imread(f'data/speaker{speaker}.png')
    # img = cv2.resize(img, (960, 540))
    cv2.imshow('image', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
