def getResistance(color_code):
    # {color: [digit, multiplier]}
    color_dict = {
        'black': [0, 1],
        'brown': [1, 10],
        'red': [2, 100],
        'orange': [3, 1_000],
        'yellow': [4, 10_000],
        'green': [5, 100_000],
        'blue': [6, 1_000_000],
        'violet': [7, 10_000_000],
        'gray': [8, 100_000_000],
        'white': [9, 1_000_000_000],
        'gold': [-1, .1],
        'silver': [-1, .01]
    }

    # var to hold result
    resistance = ''

    # color code only 3 -> 6 bands
    if len(color_code) > 6 or len(color_code) < 3:
        return 'Invalid color code'
    # 1st, 2nd, multiplier
    elif len(color_code) == 3:
        resistance = (color_dict[color_code[0]][0] * 10 + color_dict[color_code[1]][0]) * color_dict[color_code[2]][1]
    # 1st, 2nd, multiplier, tolerance
    elif len(color_code) == 4:
        color_code = color_code[:-1]
        resistance = (color_dict[color_code[0]][0] * 10 + color_dict[color_code[1]][0]) * color_dict[color_code[2]][1]

    # 1st, 2nd, 3rd, multiplier, tolerance
    elif len(color_code) == 5:
        color_code = color_code[:-1]
        resistance = ((color_dict[color_code[0]][0] * 100 + color_dict[color_code[1]][0] * 10
                       + color_dict[color_code[2]][0]) * color_dict[color_code[2]][1])
    # 1st, 2nd, 3rd, multiplier, tolerance, temp coefficient
    elif len(color_code) == 6:
        color_code = color_code[:-2]
        resistance = ((color_dict[color_code[0]][0] * 100 + color_dict[color_code[1]][0] * 10
                       + color_dict[color_code[2]][0]) * color_dict[color_code[2]][1])

    return formatResistance(resistance)


# takes int and turns to proper string
def formatResistance(value):
    if value >= 1_000_000_000:
        result = value / 1_000_000_000
        unit = 'GΩ'
    elif value >= 1_000_000:
        result = value / 1_000_000
        unit = 'MΩ'
    elif value >= 1_000:
        result = value / 1_000
        unit = 'kΩ'
    else:
        result = value
        unit = 'Ω'

    if result.is_integer():
        return f"{int(result)} {unit}"
    else:
        return f"{result:.2f} {unit}"