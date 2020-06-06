import os
import sqlite3
import pytest
import sys
import mock
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import interactive_spellchecker


@pytest.fixture(scope='function')
def case_data():
    yield
    conn = sqlite3.connect(os.path.join(os.path.dirname
                           (os.path.dirname
                            (os.path.abspath(__file__))), r'speller.db'))
    cursor = conn.cursor()
    cursor.execute('delete from virtualdict where virtwords="лайт"')
    conn.commit()
    conn.close()


@mock.patch("interactive_spellchecker.GetVariants",
            return_value=["кошка", "кашка"])
@mock.patch("interactive_spellchecker.input", return_value="В")
def test_user_asking(a, b):
    assert interactive_spellchecker.user_asking("китька",
                                                True, 'virtualdict') ==\
                                                ["кошка", "кашка"]


def test_entry_creation(case_data):
    interactive_spellchecker.AddToBase('лайт', True, 'virtualdict')
    assert interactive_spellchecker.is_word_right('лайт',
                                                  True, 'virtualdict') is True
