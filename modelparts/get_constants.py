"""Extracts constants from a file.
Expected a text format separated with colons, e.g.
this_constant:0.2
that_constant:0.25  #not the same as this_constant
Any character can be used in a constant name except whitespace, colon and #.
"""

def extract(filename):
    """
Returns a dictionary of constants and their values.
All values converted to floats if possible.
    """
    constants = {}
    conslin = None
    with open(filename, "r") as conf:
        conslin = conf.readlines()
    for line in conslin:
        if len(line):
            parts = line.split()
            if len(parts) and parts[0][0] != "#":
                item = parts[0].split(":")
                try:
                    constants[item[0]] = float(item[1])
                except ValueError:
                    constants[item[0]] = item[1]
    return constants
