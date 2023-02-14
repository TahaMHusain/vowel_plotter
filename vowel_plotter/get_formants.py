from pathlib import Path

from parselmouth import praat, Sound


def get_formants(sound: Sound):

    f0min = 100 # 75 Hz default
    f0max = 500 # 300 Hz default
    timestep = 0.0025
    num_formants = 5
    formant_ceiling = 5000
    window_length = 0.025
    preemphasis = 50

    point_process = praat.call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    pitch_tier = praat.call(point_process, "To PitchTier", window_length)

    formants = praat.call(sound, "To Formant (burg)", timestep, num_formants, formant_ceiling, window_length, preemphasis)

    num_points = praat.call(point_process, "Get number of points")
    f0_list, f1_list, f2_list, f3_list = [], [], [], []
    for point in range(1, num_points + 1):
        t = praat.call(point_process, "Get time from index", point)

        f0 = praat.call(pitch_tier, "Get mean (points)", t - window_length / 2, t + window_length / 2)

        f1 = praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = praat.call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')

        f0_list.append(f0)

        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)

    return f0_list, f1_list, f2_list, f3_list


if __name__ == '__main__':
    path = './data/a.wav'
    f0_list, f1_list, f2_list, f3_list = get_formants(Sound(path))
    print(f'F0:\n{f0_list}'
          f'\n\nF1:\n{f1_list}'
          f'\n\nF2:\n{f2_list}')