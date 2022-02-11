import re
import random
with open(r'C:\Users\asus\progrexp\lab_2_1\locations.list', 'r') as file:
    with open('locations_for_documentation.list', 'w') as file2:
        names= set()
        pat = '\([1-2][0-9][0-9][0-9]\)'
        for line in file:
            if re.search(pat, line):
                name = line[:(re.search(pat, line).start() - 1)].strip('"').strip("'")
                if name not in names and random.random() < 0.0001:
                    names.add(name)
                    file2.write(line)
