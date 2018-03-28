import click
from .converter_app import *


@click.command()
@click.argument('ingredient', nargs=-1)
@click.option('--interactive', '-i', default=False, is_flag=True, help="Will give options for each input.")
@click.option('--amount', '-a', type=float, help="Amount of ingredient to convert.")
@click.option('-f', default="", help="Measurement unit converting from.")
@click.option('-t', default="", help="Measurement unit converting to.")
@click.option('--converter', '-c', default="ratio", type=click.Choice(['ratio', 'density']),
              help="Type of converter")
def convert(ingredient, interactive, amount, f, t, converter):

    """This is a unit converter for cooking ingredients."""

    density_converter = False
    if converter == 'density':
        density_converter = True

    if density_converter:
        converter = DensityConverter()
    else:
        converter = RatioConverter()

    if ingredient:
        ingredient = ' '.join(ingredient)
        converter.run_once(ingredient, amount, f, t, interactive)
    else:
        converter.run_app(interactive)


if __name__ == '__main__':
    convert()