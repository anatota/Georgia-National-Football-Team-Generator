import pytest
from unittest.mock import patch
from project import validate_sort, parse, check_format, valid_sum

def test_validate_sort():
    assert validate_sort('1') == '1'
    assert validate_sort('2') == '2'
    assert validate_sort('3') == '3'
    with pytest.raises(ValueError):
        validate_sort('4')
    with pytest.raises(ValueError):
        validate_sort('abc')

def test_parse():
    assert parse('4-3-3') == [1, 4, 3, 3]

    with patch('project.get_orientation', return_value='1'):
        assert parse('4-3-2-1') == [1, 4, 3, 3]
    with patch('project.get_orientation', return_value='2'):
        assert parse('4-3-2-1') == [1, 4, 5, 1]

def test_check_format():
    with pytest.raises(ValueError):
        check_format('4.4.2')
    with pytest.raises(ValueError):
        check_format('4x4x2')
    with pytest.raises(ValueError):
        check_format('4_4_2')
    with pytest.raises(ValueError):
        check_format('4 4 2')
    with pytest.raises(ValueError):
        check_format('4321')
    with pytest.raises(ValueError):
        check_format('4')

def test_valid_sum():
    assert valid_sum(['4', '4', '2']) == True
    assert valid_sum(['4', '3', '2', '1']) == True
    assert valid_sum(['3', '2', '2', '2', '1']) == True
    assert valid_sum(['4', '4', '5']) == False
