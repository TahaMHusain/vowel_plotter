from montreal_forced_aligner.alignment.pretrained import PretrainedAligner


def align(corpus_path: str, dictionary_path: str, acoustic_model_path: str, output_directory: str):
    """
    Runs the equivalent of `mfa align path/to/corpus english_us_arpa english_us_arpa path/to/output`
    :param corpus_path: Temporary corpus path
    :param dictionary_path: Dict path (set in main.py)
    :param acoustic_model_path: Acoustic model path (set in main.py)
    :param output_directory: Temp output path
    :return:
    """
    aligner = PretrainedAligner(
        corpus_directory=corpus_path,
        dictionary_path=dictionary_path,
        acoustic_model_path=acoustic_model_path)
    

    aligner.align()
    aligner.export_files(output_directory, output_format='long_textgrid')
    aligner.cleanup()