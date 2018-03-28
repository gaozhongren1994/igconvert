from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json, os
from converter.src.converter_app import *


# with open('conversion_ratios.json', 'r') as f:
#     conversion_ratios = json.load(f)

# with open('../ratio/density.json', 'r') as d:
#     density = json.load(d)

# with open('../ratio/unit_ratios.json', 'r') as r:
#     unit_ratios = json.load(r)


# ingredient = list(conversion_ratios.keys())
# ingredient = list(density.keys())
#
# while True:
#     i = input('Target ingredient: ')
#     if i == 'q':
#         break
#     matches1 = process.extract(i, ingredient, scorer=fuzz.token_set_ratio, limit=5)
#     matches2 = process.extract(i, ingredient, scorer=fuzz.partial_ratio, limit=3)
#     print(matches1)
#     print(matches2)
#     print()


# measure = list(conversion_ratios['All purpose flour'].keys())
#
# while True:
#     m = input('Target measurement: ')
#     if m == 'q':
#         break
#     matches1 = process.extract(m, measure, scorer=fuzz.token_set_ratio, limit=3)
#     matches2 = process.extract(m, measure, scorer=fuzz.partial_ratio, limit=3)
#     print(matches1)
#     print(matches2)
#     print()



# c = get_converted_with_density(density['Almond butter'], unit_ratios, 'pound', 'cup [US]', 1.5)
# print(c)
print(os.getcwd())
