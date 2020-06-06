import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import pytest
import generate_base
import sqlite3
import interactive_spellchecker


@pytest.fixture(scope='function')
def base_clearing():
    # нужно не добавлять базы с таким именем(подказка пользователю)
    yield
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.dirname(os.path.abspath(__file__))), st))
    cursor = conn.cursor()
    cursor.execute('drop table first')
    cursor.execute('delete from tablenames where names="first"')
    conn.commit()
    conn.close()


@pytest.fixture(scope='function')
def line_clearing():
    yield
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.dirname(os.path.abspath(__file__))), st))
    cursor = conn.cursor()
    cursor.execute('delete from virtualdict where virtwords="ффффф"')
    conn.commit()
    conn.close()


def test_adding_base(base_clearing):
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.dirname(os.path.abspath(__file__))), st))
    cursor = conn.cursor()
    generate_base.virt_table_creation('first', 'second')
    availab = generate_base.getavailabledicts()
    res_test = interactive_spellchecker.appropriate_list(availab)
    assert ('first' in res_test) is True
    conn.commit()
    conn.close()


def test_init(line_clearing):
    list = ['ффффф']
    generate_base.virtualdictinit(list, 'virtualdict')
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.dirname(os.path.abspath(__file__))),
                            r'speller.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT virtwordsfull FROM virtualdict'
                   ' WHERE virtualdict MATCH "ффффф"')
    list = cursor.fetchall()
    conn.commit()
    conn.close()
    res_test = interactive_spellchecker.appropriate_list(list)
    assert 'ффффф' in res_test


def test_available():
    av_dicts = generate_base.getavailabledicts()
    test_data = interactive_spellchecker.appropriate_list(av_dicts)
    assert ('virtualdict' in test_data) is True


def test_adding_existing_base(capsys):
    generate_base.virt_table_creation('virtualdict', 'virtwords')
    captured = capsys.readouterr()
    assert captured.out == 'Base with this name already exists.' \
                           'Please,' \
                           ' try generate base with another name again.\n'


def test_file_in_words():
    st = r'test_file.txt'
    path = os.path.join(os.path.dirname
                        (os.path.dirname
                         (os.path.abspath(__file__))), st)
    assert generate_base.gen_file_into_words(path) == []
