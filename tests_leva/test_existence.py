import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import interactive_spellchecker


@pytest.mark.parametrize("wrd,initial,expected",
                         [('хлеб', True, True),
                          ('самолёт', True, True),
                          ('прекрасного', False, True),
                          ('лайтовому', False, False),
                          ('рофл', True, False)])
def test_simple_word_contained(wrd, initial, expected):
    assert interactive_spellchecker.\
               is_word_right(wrd, initial, "virtualdict") is expected
