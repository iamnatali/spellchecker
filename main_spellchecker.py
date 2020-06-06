import interactive_spellchecker
import file_spellchecker
import generate_base
from os import path as pth
import argparse
import sys
import spaces

_old_excepthook = sys.excepthook


def myexcepthook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("Программа была прервана Ctrl+C.\n"
              "Для завершения работы в интерактивном"
              " режиме предпочтительнее использовать Enter\n"
              "Спасибо за использование нашего продукта!")
    else:
        _old_excepthook(exctype, value, traceback)


def parser_analize(args, dict1, res_path):
    if args.put_spaces:
        spaces.main()
    elif args.dict:
        dict1 = args.dict
    elif args.imode and args.file:
        oops = "Интерактивный режим не поддерживает работу с файлами.\n" +\
              "Перейдите в пакетный режим."
        print(oops)
        return oops
    elif args.ubase and (args.imode or args.file):
        oops1 = "Необходимо генерировать базу до запуска" +\
              " интерактивной проверки или пакетный режима\n" +\
              "или пользоваться базой по умолчанию"
        print(oops1)
        return oops1
    elif args.ubase:  # !=None
        work_with_file(args.ubase[0], 'generate', dict1, res_path)
    elif args.file:
        rpath = pth.join(r".", r'res1.txt')
        if len(args.file[0]) == 2:
            rpath = args.file[0][1]
        elif len(args.file[0]) > 2:
            oops3 = "Передайте ДВА агрумента"
            print(oops3)
            return oops3
        work_with_file(args.file[0][0], 'filespell',
                       dict1, rpath, args.j)
    else:
        interactive_spellchecker.main(dict1)


def main():
    sys.excepthook = myexcepthook
    if len(sys.argv) == 1:
        print("print -h/--help to get helper")
    else:
        dict1 = 'virtualdict'
        nlist = generate_base.getavailabledicts()
        res_path = r"res.txt"
        s = ''
        for elem in nlist:
            s += elem[0] + ' '
        args = parseEnter(s)
        parser_analize(args, dict1, res_path)


def parseEnter(s, list=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--put_spaces', '-ps', action='store_true',
                        help='Интерактивный режим разделения'
                             ' текста по пробелам')
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='Показать это сообщение и закончить работу')
    parser.add_argument(
        '--imode',
        action='store_true',
        help='Запуск в интерактивном режиме')
    parser.add_argument('--ubase', action='append', type=str,
                        help='Использование данного файла'
                             ' для генерации базы(словаря)')
    parser.add_argument(
        '--dict', type=str, help='Выбор уже сгенерированного словаря,'
                                 ' отличного от стандартного'
        'Возможные словари:\n' + s)
    parser.add_argument('--file', '-f', action='append', nargs="+", type=str,
                        help='Запуск в пакетном режиме(для работы с файлами)\n'
                             'Введите путь к файлу, который нужно'
                             ' проанализировать'
                             ' и путь к файлу для помещения результата\n'
                             'По умолчанию создается новый файл res.txt')
    parser.add_argument('-j', action='store_true',
                        help='В сочетании с --file(передается'
                             ' как отдельный аргумент'
                             'НЕ после --file или может образовывать'
                             ' префикс -jf) \n'
                             'позволяет пропустить шаги'
                             ' взаимодействия с программой.\n'
                             'Текст будет без изменений записан'
                             ' в результирующий файл,\n'
                             'но в конце будут добавлены данные'
                             ' об ошибках и возможные варианты')
    args = parser.parse_args(list)
    return args


def work_with_file(args, aimfunc, dict1, res_path, silent=False):
    if pth.exists(args):
        if aimfunc == "filespell":
            file_spellchecker.main(args, dict1, res_path, silent)
        elif aimfunc == 'generate':
            generate_base.main(args)
    else:
        print('Please, enter another path.This one is not right1')


if __name__ == '__main__':
    main()
