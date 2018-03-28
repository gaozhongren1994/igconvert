from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sys, json, operator, os



class Converter:

    def __init__(self, ingredients = list()):
        self.ingredients = ingredients


    def get_matches(self, user_input, options):
        return list(map((lambda o: (o, 1)), options))


    def get_input(self, options, option_name, interactive=False, is_app=True):
        user_input = input("Please choose " + option_name + ": ").strip()
        if is_app:
            if user_input == 'q':
                sys.exit()
            if not user_input or user_input == 'h':
                return ""

        matches = self.get_matches(user_input, options)

        if not interactive:
            return matches[0][0]

        choices = [str(i + 1) + ": " + m[0] for i, m in enumerate(matches)]
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


    def get_measurements(self, ingredient=""):
        return []


    def get_converted(self, ingredient, from_measure, to_measure, amount):
        return 'unknown'


    def run_app(self, interactive=False):

        print("Enter 'q' to exit,", "'h' to reselect ingredient")
        print()

        while True:
            ingredient = self.get_input(self.ingredients, "ingredient", interactive=interactive)

            while ingredient:
                measurements = self.get_measurements(ingredient=ingredient)

                from_measure = self.get_input(measurements, "measurement converting from", interactive=interactive)
                if not from_measure:
                    break

                to_measure = self.get_input(measurements, "measurement converting to", interactive=interactive)
                if not to_measure:
                    break

                user_input = input("Please enter the amount: ").strip()
                amount = 1
                try:
                    amount = float(user_input)
                except ValueError:
                    pass

                converted_amount = self.get_converted(ingredient, from_measure, to_measure, amount)
                print(str(amount) + ' ' + from_measure + " of " + \
                      ingredient + " is " + converted_amount + ' ' + to_measure)
                print()


    def run_once(self, ingredient, amount=1, from_measure="", to_measure="", interactive=False):
        ingredient = self.get_matches(ingredient, self.ingredients)[0][0]

        measurements = self.get_measurements(ingredient=ingredient)
        if not from_measure:
            from_measure = self.get_input(measurements,
                                          "measurement converting from", interactive=interactive, is_app=False)
        else:
            from_measure = self.get_matches(from_measure, measurements)[0][0]

        if not to_measure:
            to_measure = self.get_input(measurements,
                                        "measurement converting to", interactive=interactive, is_app=False)
        else:
            to_measure = self.get_matches(to_measure, measurements)[0][0]

        if not amount:
            amount = input("Please enter the amount: ").strip()
        try:
            amount = float(amount)
        except ValueError:
            amount = 1

        converted_amount = self.get_converted(ingredient, from_measure, to_measure, amount)
        print(str(amount) + ' ' + from_measure + " of " + \
              ingredient + " is " + converted_amount + ' ' + to_measure)
        print()



class RatioConverter(Converter):

    def __init__(self):
        ratio_file = os.path.join(os.path.dirname(__file__), 'conversion_ratios.json')
        with open(ratio_file, 'r') as ratios:
            self.conversion_ratios = json.load(ratios)
        super().__init__(self.conversion_ratios.keys())


    def get_matches(self, user_input, options):
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


    def get_measurements(self, ingredient=""):
        ratios = self.conversion_ratios[ingredient]
        return list(ratios.keys())


    def get_converted(self, ingredient, from_measure, to_measure, amount):
        if from_measure == to_measure:
            return str(amount)

        ratios = self.conversion_ratios[ingredient]
        if float(ratios[from_measure]) == 0:
            return "infinite"
        return str(round(amount / float(ratios[from_measure]) * float(ratios[to_measure]), 2))



class DensityConverter(Converter):

    def __init__(self):
        density_file = os.path.join(os.path.dirname(__file__), 'density.json')
        with open(density_file, 'r') as d:
            self.density = json.load(d)
        unit_file = os.path.join(os.path.dirname(__file__), 'unit_ratios.json')
        with open(unit_file, 'r') as u:
            self.unit_ratios = json.load(u)
        self.measurements = list(self.unit_ratios.keys())
        super().__init__(self.density.keys())


    def get_matches(self, user_input, options):
        matches = process.extract(user_input, options, scorer=fuzz.token_set_ratio, limit=5)
        match_score = {}
        for n, s in matches:
            if n not in match_score:
                match_score[n] = 0
            match_score[n] += s
        sorted_matches = sorted(match_score.items(), key=lambda m: (m[1], -len(m[0])), reverse=True)
        return sorted_matches


    def get_measurements(self, ingredient=""):
        return self.measurements


    def get_converted(self, ingredient, from_measure, to_measure, amount):
        if from_measure == to_measure:
            return str(amount)

        density = float(self.density[ingredient])
        from_ratio = float(self.unit_ratios[from_measure])
        to_ratio = float(self.unit_ratios[to_measure])

        if from_ratio * to_ratio > 0:
            # convert weight to weight, or volume to volume
            return str(round(amount * from_ratio / to_ratio, 2))

        if from_ratio < 0:
            # convert volume to weight
            return str(round(-amount * from_ratio * density / to_ratio, 2))

        # convert weight to volume
        return str(round(-amount * from_ratio / density / to_ratio, 2))