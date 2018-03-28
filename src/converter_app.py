from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sys, getopt, operator
try:
    from .converter_obj import RatioConverter, DensityConverter
except ImportError:
    from converter.src.converter_obj import RatioConverter, DensityConverter


def get_matches(user_input, options):
    match1 = process.extract(user_input, options, scorer=fuzz.token_set_ratio, limit=4)
    match2 = process.extract(user_input, options, scorer=fuzz.partial_ratio, limit=4)

    match_score = {}
    for n, s in match1:
        if n not in match_score:
            match_score[n] = 0
        match_score[n] += s
    for n, s in match2:
        if n not in match_score:
            match_score[n] = 0
        match_score[n] += s

    sorted_matches = sorted(match_score.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_matches


def get_input(options, option_name, interactive=False, is_app=True):
    user_input = input("Please choose " + option_name + ": ").strip()
    if is_app:
        if user_input == 'q':
            sys.exit()
        if not user_input or user_input == 'h':
            return ""

    matches = get_matches(user_input, options)

    if not interactive:
        return matches[0][0]

    choices = [str(i+1) + ": " + m[0] for i, m in enumerate(matches)]
    print(', '.join(choices))

    user_input = input("Please choose an option from above: ").strip()
    if is_app:
        if user_input == 'q':
            sys.exit()
        if user_input == 'h':
            return ""
    try:
        i = int(user_input) - 1
        i = max(0, min(i, len(matches) - 1))
        return matches[i][0]
    except ValueError:
        return matches[0][0]


def get_converted_with_ratios(ratios, from_measure, to_measure, amount):
    if from_measure == to_measure:
        return str(amount)
    if float(ratios[from_measure]) == 0:
        return "infinite"
    return str(round(amount / float(ratios[from_measure]) * float(ratios[to_measure]), 2))


def get_converted_with_density(density, unit_ratios, from_unit, to_unit, amount):
    from_ratio = float(unit_ratios[from_unit])
    to_ratio = float(unit_ratios[to_unit])

    if from_ratio * to_ratio > 0:
        # convert weight to weight, or volume to volume
        return str(round(amount * from_ratio / to_ratio, 2))

    if from_ratio < 0:
        # convert volume to weight
        return str(round(-amount * from_ratio * float(density) / to_ratio, 2))

    # convert weight to volume
    return str(round(-amount * from_ratio / float(density) / to_ratio, 2))


def run_app(conversion_ratios, interactive=False):

    print("Enter 'q' to exit,", "'h' to reselect ingredient")
    print()

    while True:
        ingredient = get_input(list(conversion_ratios.keys()), "ingredient", interactive=interactive)

        while ingredient:
            ratios = conversion_ratios[ingredient]
            measurements = list(ratios.keys())

            from_measure = get_input(measurements, "measurement converting from", interactive=interactive)
            if not from_measure:
                break

            to_measure = get_input(measurements, "measurement converting to", interactive=interactive)
            if not to_measure:
                break

            user_input = input("Please enter the amount: ").strip()
            amount = 1
            try:
                amount = float(user_input)
            except ValueError:
                pass

            converted_amount = get_converted_with_ratios(ratios, from_measure, to_measure, amount)
            print(str(amount) + ' ' + from_measure + " of " + \
                  ingredient + " is " + converted_amount + ' ' + to_measure)
            print()


def run_once(conversion_ratios, ingredient, amount=1, from_measure="", to_measure="", interactive=False):
    options = list(conversion_ratios.keys())
    ingredient = get_matches(ingredient, options)[0][0]
    ratios = conversion_ratios[ingredient]
    options = list(ratios.keys())

    if not from_measure:
        from_measure = get_input(options, "measurement converting from", interactive=interactive, is_app=False)
    else:
        from_measure = get_matches(from_measure, options)[0][0]

    if not to_measure:
        to_measure = get_input(options, "measurement converting to", interactive=interactive, is_app=False)
    else:
        to_measure = get_matches(to_measure, options)[0][0]

    if not amount:
        amount = input("Please enter the amount: ").strip()
    try:
        amount = float(amount)
    except ValueError:
        amount = 1

    converted_amount = get_converted_with_ratios(ratios, from_measure, to_measure, amount)
    print(str(amount) + ' ' + from_measure + " of " + \
          ingredient + " is " + converted_amount + ' ' + to_measure)
    print()


def main():

    interactive = False
    density_converter = False

    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'hic:', ["help", "interactive", "converter="])
    except getopt.GetoptError:
        print("Illegal option")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print("Options")
            print("-h, --help", '\t\t', "Show help")
            print("-i, --interactive", '\t\t', "Interactive mode")
            print("-c, --converter", "[ratio|density]", '\t\t', "Use ratio (default) or density converter")
            sys.exit()
        elif opt in ('-i', "--interactive"):
            interactive = True
        elif opt in ('-c', "--converter"):
            if arg == "density":
                density_converter = True

    if density_converter:
        print("Using density converter")
        converter = DensityConverter()
    else:
        print("Using ratio converter")
        converter = RatioConverter()
    converter.run_app(interactive=interactive)



if __name__ == "__main__":
    main()