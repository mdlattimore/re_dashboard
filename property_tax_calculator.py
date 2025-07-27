


def calculate_property_tax(assessed_value: float, millage: float,
                           fees: float=0) -> float:
    return ((assessed_value / 100) * millage) + fees