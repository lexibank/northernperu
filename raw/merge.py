import csv
from glob import glob


final_data = [[
    "Doculect", "Concept", "Form", "Notes"
]]

data = list(sorted(glob("prepared_data/*.tsv")))

# Load manually digitized data
def add_wl(language):
    """Adds data from languages in folder."""
    with open(language, mode='r', encoding="utf8") as f:
        wl = csv.reader(f, delimiter="\t")
        next(wl)
        for entry in wl:
            print(entry)
            if entry[2] != "":
                final_data.append(entry)


# Load Iquito data
with open("preprocessing/imported/iquito.tsv", mode='r', encoding="utf8") as file:
    d = csv.reader(file, delimiter="\t")
    next(d)
    for lines in d:
        final_data.append([
            "Iquito",
            lines[2],  # Gloss
            lines[3],  # Form
            lines[5]   # Note --> SENSE in dictionary
    ])

# Check that everything is alright
for lang in data:
    add_wl(lang)

with open("raw.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(final_data)
