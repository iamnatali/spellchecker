import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import pytest
import interactive_spellchecker


@pytest.mark.parametrize("wrd1, wrd2, initial",
                         [('болото', 'болоьо', True),
                          ('млекопитающее', 'млукопитающее', True),
                          ('хлеб', 'хдлеб', True),
                          ('зеленый', 'зилёный', True),
                          ('хлеб', 'хлема', False),
                          ('зеленый', 'зилёная', False)])
def test_simple_word_contained(wrd1, wrd2, initial):
    assert (wrd1 in interactive_spellchecker.
            GetVariants(wrd2, initial, "virtualdict")) is True
