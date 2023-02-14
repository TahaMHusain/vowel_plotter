from montreal_forced_aligner.alignment.pretrained import PretrainedAligner
from montreal_forced_aligner.command_line.utils import check_databases, cleanup_databases


def align(corpus_path: str, dictionary_path: str, acoustic_model_path: str, output_directory: str):
    aligner = PretrainedAligner(
        corpus_directory=corpus_path,
        dictionary_path=dictionary_path,
        acoustic_model_path=acoustic_model_path)

    check_databases()
    aligner.align()
    aligner.export_files(output_directory, output_format='long_textgrid')
    aligner.cleanup()
    cleanup_databases()
