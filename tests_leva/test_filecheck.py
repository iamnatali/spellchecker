import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import file_spellchecker
import mock


text_data = "Красив и печален русский лис в ранние осенние дни."
wrong_right = [("лис", "лес")]


@mock.patch('interactive_spellchecker.is_word_right',
            side_effect=lambda x, y, z: False)
def test_start_end(word_right_function):
    a = mock.Mock()
    a.start.return_value = 1
    a.end.return_value = 2
    data = []
    data.append(a)
    assert file_spellchecker.form_start_end(data, [], 'virtualdict')[0][:2] ==\
        [1, 2]


def test_change():
    assert file_spellchecker.change_wrong_right(wrong_right, text_data) ==\
           "Красив и печален русский лес в ранние осенние дни."


def test_red_list():
    assert file_spellchecker.form_red_list("Красив и печален русский лес",
                                           [[0, 6]]) ==\
        "\x1b[31;40mКрасив\x1b[0m и печален русский лес"


def test_splitting():
    str = "Окуратно отодвигая дары мореь," \
          "\nя доставал с полок дениги, садился по-турецки в кресло."
    a = file_spellchecker.text_prerocessing(str, [])[0]
    my_list = []
    for e in a:
        word = e.group()
        my_list.append(word)
    list = ['Окуратно', 'отодвигая', 'дары', 'мореь', 'я', 'доставал',
            'с', 'полок', 'дениги', 'садился', 'по', 'турецки', 'в', 'кресло']
    assert list == my_list
