"""
Definition of equations used
"""


def drag_equation(drag_coefficient: float, velocity: float, reference_area: float):
    return drag_coefficient * reference_area * 0.5 * 1.225 * velocity**2


def drag_coefficient_function(reynolds_number: int, drag_range: tuple):
    slope = (drag_range[1] - drag_range[0]) / ((4.2 - 0.7) * 10**6)
    return slope * reynolds_number + drag_range[0]
