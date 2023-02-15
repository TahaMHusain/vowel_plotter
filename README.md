# Vowel Plotter

Extract and plot the F1 and F2 frequencies from a recording of speech.

### How to Run

First, setup your Python environment

```commandline
git clone https://github.com/TahaMHusain/vowel_plotter.git
cd vowel_plotter
pip install -r requirements.txt  # An 'environment.yml' file is provided for conda users
```

You can then test the environment by running on sample data:
```commandline
python vowel_plotter.py data/sample_vowels.wav
```

After a minute or so, you should see a multicolored chart like this appear in a new window (and saved as `data/vowel_plot.png`):
![Pretty cool, right?](http://github.com/TahaMHusain/vowel_plotter/blob/main/data/sample_plot.png?raw=true)



To plot your own vowels, first record yourself saying the following words three times each.

|   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
| beat  |  bit | bait | bet | bat | bot | boat | but | book | boot |

Make sure to speak slowly and clearly, with pauses in between words. Listen to `data/sample_vowels.wav` for an example.

Save the recording as a `.wav` file, then run `vowel_plotter.py` :
```commandline
python vowel_plotter.py path/to/recording.wav
```


