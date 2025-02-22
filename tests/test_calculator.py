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


def test_format_duration_sub_minute():
    """Test sub-minute durations (should format as seconds)"""
    calc = AvailabilityCalculator(99.99)  # Calculator instance for testing

    assert calc._format_duration(0.5) == "30.0 seconds"
    assert calc._format_duration(0.1) == "6.0 seconds"
    assert calc._format_duration(0.016667) == "1.0 seconds"


def test_format_duration_minutes_only():
    """Test minute-only durations"""
    calc = AvailabilityCalculator(99.99)

    assert calc._format_duration(1) == "1.0 minutes"
    assert calc._format_duration(30) == "30.0 minutes"
    assert calc._format_duration(59) == "59.0 minutes"


def test_format_duration_hours_only():
    """Test hour-only durations"""
    calc = AvailabilityCalculator(99.99)

    # 60 minutes = 1 hour
    assert calc._format_duration(60) == "1 hours"
    assert calc._format_duration(120) == "2 hours"
    assert calc._format_duration(180) == "3 hours"


def test_format_duration_hours_and_minutes():
    """Test combined hours and minutes"""
    calc = AvailabilityCalculator(99.99)

    assert calc._format_duration(90) == "1 hours 30.0 minutes"
    assert calc._format_duration(150) == "2 hours 30.0 minutes"
    assert calc._format_duration(61) == "1 hours 1.0 minutes"


def test_format_duration_edge_cases():
    """Test edge cases (0 minutes, 59.9 minutes, 60 minutes)"""
    calc = AvailabilityCalculator(99.99)

    assert calc._format_duration(0) == "0.0 seconds"
    assert calc._format_duration(59.9) == "59.9 minutes"
    assert calc._format_duration(60) == "1 hours"
    assert calc._format_duration(59.99999) == "60.0 minutes"
