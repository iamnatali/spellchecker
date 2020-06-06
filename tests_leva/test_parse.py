import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import pytest
import main_spellchecker
import interactive_spellchecker
import mock


def test_analize1():
    args = mock.Mock()
    oops = "Интерактивный режим не поддерживает работу с файлами.\n" + \
           "Перейдите в пакетный режим."
    args.put_spaces = False
    args.dict = False
    args.imode = True
    args.file = True
    assert main_spellchecker.parser_analize(args, 'virtualdit', "path") ==\
        oops


def test_analize2():
    args = mock.Mock()
    oops = "Необходимо генерировать базу до запуска" +\
        " интерактивной проверки или пакетный режима\n" +\
        "или пользоваться базой по умолчанию"
    args.put_spaces = False
    args.dict = False
    args.imode = True
    args.file = False
    args.ubase = True
    assert main_spellchecker.parser_analize(args, 'virtualdit', "path") == \
        oops


def test_parse_():
    list = [r'-ps', r'--imode', r'--ubase', r'.\first_path', r'--ubase',
            r'.\second_path', r'--dict', r'some_dict', r'--file',
            r'.\first_file', r'.\first_res_file', r'--file',
            r'.\second_file', r'.\second_res_file']
    args = main_spellchecker.parseEnter('someDicts', list)
    assert args.put_spaces is True
    assert args.imode is True
    assert args.ubase == [r'.\first_path', r'.\second_path']
    assert args.dict == 'some_dict'
    assert args.file == [[r'.\first_file', r'.\first_res_file'],
                         [r'.\second_file', r'.\second_res_file']]


def test_list_converter():
    initiallist = [('first',), ('second',), ('third',)]
    reslist = ['first', 'second', 'third']
    assert interactive_spellchecker.appropriate_list(initiallist) == reslist


def test_initialstem():
    wrd = 'полный'
    assert interactive_spellchecker.initiality_stem(wrd, False) == 'полн'
    assert interactive_spellchecker.initiality_stem(wrd, True) == 'полный'
