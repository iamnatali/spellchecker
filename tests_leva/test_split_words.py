import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import pytest
import spaces


@pytest.mark.parametrize("res, wrd",
                         [(" кошка хлеб лукошко ", "кошкахлеблукошко"),
                          (" каша стол стул ", "кашастолстул")])
def test_the_only(res, wrd):
    assert (res in spaces.process_word(wrd)) is True
