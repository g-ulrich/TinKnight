def percent_of_two_numbers(base, current, round_to=4):
    if base < current:
        try:
            return round((abs(base - current) / base) * 100, round_to)
        except:
            return 0.0
    else:
        try:
            return -round(((base - current) / base) * 100, round_to)
        except:
            return -0.0


def percent_number_of_another_number(a, b):
    if a > b:
        return round((b / a) * 100, 2)
    else:
        return round((a / b) * 100, 2)