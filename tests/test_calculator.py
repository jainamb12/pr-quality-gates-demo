import pytest

from quality_demo.calculator import calculate_statistics


def test_calculate_statistics_with_positive_numbers():
    result = calculate_statistics([10, 20, 30, 40])

    assert result == {
        "count": 4,
        "total": 100.0,
        "mean": 25.0,
        "minimum": 10.0,
        "maximum": 40.0,
    }


def test_calculate_statistics_with_one_number():
    result = calculate_statistics([15])

    assert result == {
        "count": 1,
        "total": 15.0,
        "mean": 15.0,
        "minimum": 15.0,
        "maximum": 15.0,
    }


def test_calculate_statistics_with_negative_numbers():
    result = calculate_statistics([-10, -20, -30])

    assert result["total"] == -60.0
    assert result["mean"] == -20.0
    assert result["minimum"] == -30.0
    assert result["maximum"] == -10.0


def test_calculate_statistics_with_decimal_numbers():
    result = calculate_statistics([1.5, 2.5, 3.0])

    assert result["total"] == 7.0
    assert result["mean"] == pytest.approx(7.0 / 3.0)


def test_calculate_statistics_rejects_empty_input():
    with pytest.raises(ValueError, match="cannot be empty"):
        calculate_statistics([])


def test_calculate_statistics_rejects_non_numeric_input():
    with pytest.raises(TypeError, match="real numbers"):
        calculate_statistics([10, "20", 30])


def test_calculate_statistics_rejects_boolean_values():
    with pytest.raises(TypeError, match="real numbers"):
        calculate_statistics([10, True, 30])
