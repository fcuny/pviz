import pytest
from pviz.main import AvailabilityCalculator


def test_calculator_initialization_valid_values():
    # Test boundary values and a middle value
    calc_zero = AvailabilityCalculator(0)
    calc_fifty = AvailabilityCalculator(50)
    calc_hundred = AvailabilityCalculator(100)

    assert calc_zero.availability == 0.0
    assert calc_fifty.availability == 0.5
    assert calc_hundred.availability == 1.0

    # Test typical SLA value
    calc_sla = AvailabilityCalculator(99.9)
    assert abs(calc_sla.availability - 0.999) < 0.0001


def test_calculator_initialization_invalid_values():
    # Test negative values
    with pytest.raises(ValueError, match="Availability must be between 0 and 100"):
        AvailabilityCalculator(-0.1)

    with pytest.raises(ValueError, match="Availability must be between 0 and 100"):
        AvailabilityCalculator(-100)

    # Test values over 100
    with pytest.raises(ValueError, match="Availability must be between 0 and 100"):
        AvailabilityCalculator(100.1)

    with pytest.raises(ValueError, match="Availability must be between 0 and 100"):
        AvailabilityCalculator(200)


def test_calculator_percentage_conversion():
    # Test common SLA values
    test_cases = [
        (99.9, 0.999),
        (99.99, 0.9999),
        (99.999, 0.99999),
        (99.0, 0.99),
    ]

    for input_value, expected in test_cases:
        calc = AvailabilityCalculator(input_value)
        assert abs(calc.availability - expected) < 0.0001
