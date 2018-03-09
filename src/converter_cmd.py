import os, click
from .converter_app import *


@click.command()
@click.argument('ingredient', nargs=-1)
@click.option('--interactive', '-i', default=False, is_flag=True, help="Will give options for each input.")
@click.option('--amount', '-a', type=float, help="Amount of ingredient to convert.")
@click.option('-f', default="", help="Measurement unit converting from.")
@click.option('-t', default="", help="Measurement unit converting to.")
def convert(ingredient, interactive, amount, f, t):

    """This is a unit converter for cooking ingredients."""

    ratio_file = os.path.join(os.path.dirname(__file__), 'conversion_ratios.json')
    with open(ratio_file) as ratios:
        conversion_ratios = json.load(ratios)

    get_input.first_time = False
    if ingredient:
        ingredient = ' '.join(ingredient)
        run_once(conversion_ratios, ingredient, amount, f, t, interactive)
    else:
        run_app(conversion_ratios, interactive=interactive)


if __name__ == '__main__':
    convert()