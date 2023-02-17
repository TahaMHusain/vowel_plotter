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
    # MFA likes it when you name files based on speaker id, so all the temp files get this name
    temp_filename = 'speaker1'

    # The acoustic model and dictionary (both called english_us_arpa in MFA) are included in the data folder.
    # You can download your own using MFA's CLI, which is necessary to plot
    # any dialect besides the one english_us_arpa is trained on (General American English)
    if not dictionary_path:
        if os.path.exists('data/MFA/pretrained_models/dictionary/english_us_arpa.dict'):
            dictionary_path = 'data/MFA/pretrained_models/dictionary/english_us_arpa.dict'
        # In case someone runs this from the src folder
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
        # Create a corpus folder and give it a new random name
        # MFA won't rerun alignment unless the folder is a different name from last time it was run >:(
        randy = random.randint(1, 100)
        corpus_path = f'data/corpus_{randy}'
    if not os.path.exists(corpus_path):
        # Copy the transcript file into the newly created corpus folder
        # MFA needs the transcript file and audio file in the same folder
        os.makedirs(corpus_path)
        shutil.copy2('data/transcript.lab', os.path.join(corpus_path, f'{temp_filename}.lab'))

    # Copy the audio file into the same corpus folder
    if not os.path.exists(os.path.join(corpus_path, f'{temp_filename}.wav')):
        shutil.copy2(sound_path, os.path.join(corpus_path, f'{temp_filename}.wav'))

    # Make an output folder for the alignment TextGrid
    if not aligned_path:
        aligned_path = corpus_path + f'_aligned'
    if not os.path.exists(aligned_path):
        os.makedirs(aligned_path)

    # Runs equivalent of `mfa align` to generate alignment TextGrid
    align(corpus_path, dictionary_path, acoustic_path, aligned_path)

    # MFA outputs the alignment TextGrid to the alignment path
    textgrid_path = Path(aligned_path).joinpath(f'{temp_filename}.TextGrid')

    # Get start and end times of each vowel as a dict of lists
    vowel_times = parse_textgrid(textgrid_path, set(arpa2ipa.keys()))

    # Get list of tuples of lists of formants
    vowels_formants = extract_vowels(sound_path, vowel_times)

    # Set up empty data frame to plot vowels from
    table = pd.DataFrame(columns=['vowel', 'F1', 'F2'])

    # Iterate over all vowels
    for vowel, formants_tuple_list in vowels_formants.items():
        # Iterate over each repetition (default 3 reps per vowel)
        for formants_tuple in formants_tuple_list:
            formants_row = {}
            # Iterate over each formant (though right now only F1 and F2 are used)
            for i, formant_list in enumerate(formants_tuple):
                # Just use the median value of each formant, that's probably good enough
                median = np.nanmedian(formant_list, axis=0)
                formants_row[f'f{i}'] = median
            # Add row to data frame
            table = pd.concat([table, pd.Series(
                {'vowel': arpa2ipa[vowel], 'F1': formants_row['f1'], 'F2': formants_row['f2']}).to_frame().T],
                              ignore_index=True)

    # Delete the temporary corpus and alignment TextGrid
    shutil.rmtree(corpus_path)
    shutil.rmtree(aligned_path)

    # Draw the vowel plot (and save to data/vowel_plot.png)
    draw_plot(table)


if __name__ == '__main__':
    main('data/corpus')
