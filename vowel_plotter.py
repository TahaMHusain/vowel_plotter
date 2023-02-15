import click

from vowel_plotter.main import main


@click.command()
@click.argument('sound_path')
def vowel_plotter(sound_path):
    main(sound_path)


if __name__ == '__main__':
    vowel_plotter()