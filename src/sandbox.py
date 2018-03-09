from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
from converter.src.converter_app import get_matches


with open('conversion_ratios.json', 'r') as sites:
    conversion_ratios = json.load(sites)

# ingredient = list(conversion_ratios.keys())
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


measure = list(conversion_ratios['All purpose flour'].keys())

while True:
    m = input('Target measurement: ')
    if m == 'q':
        break
    matches1 = process.extract(m, measure, scorer=fuzz.token_set_ratio, limit=3)
    matches2 = process.extract(m, measure, scorer=fuzz.partial_ratio, limit=3)
    print(matches1)
    print(matches2)
    print()