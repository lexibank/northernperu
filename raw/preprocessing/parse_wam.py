import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader

data = []
mappings = defaultdict(list)

PATH = "cldf-data/concepticon-data/mappings/map-en.tsv"
with UnicodeDictReader(PATH, delimiter='\t') as reader:
    for concept in reader:
        gloss = concept['GLOSS'].split('///')[1]
        mappings[gloss].append((concept['ID'], int(concept['PRIORITY'])))

# Load concept list
BASE = "cldf-data/concepticon-data/concepticondata/conceptlists/"
SWAD_200 = BASE + "Swadesh-1952-200.tsv"

concepts = {}
with UnicodeDictReader(SWAD_200, delimiter='\t') as reader:
    for line in reader:
        concepts[line["CONCEPTICON_ID"]] = line['CONCEPTICON_GLOSS']

# Iterate through data and filter entries

filtered_data = [[
    "Doculect", "Concept", "Form", "Note", "Gloss"
]]
unmatched_glosses = []

with open('Wampis.csv', mode='r', encoding="utf-8") as f:
    data = csv.reader(f, delimiter=",")
    for row in data:
        if row[1] in mappings:
            for mapping in mappings[row[1]]:
                concept_id, priority = mapping
                if concept_id in concepts:
                    gloss = concepts[concept_id]
                    filtered_data.append([
                        "Wampis",
                        gloss,
                        row[2],
                        row[3],
                        row[1]
                    ])
        else:
            unmatched_glosses.append(row[1])
            print(f"No match found for gloss: {row[1]}")

with open('../prepared_data/Wampis.tsv', 'w', encoding="utf8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(filtered_data)
