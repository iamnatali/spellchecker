import re
import interactive_spellchecker
import os
from colorama import init
import colorama


up = colorama.Cursor.UP
forward = colorama.Cursor.FORWARD


def clear(): return '\x1b[2J'


def main(path, dict, res_path, silent):
    handle = open(path, errors='ignore')
    data1 = handle.read()
    handle.close()
    hyphen_thing = []
    d = text_prerocessing(data1, hyphen_thing)
    data = d[0]
    data2 = d[1]
    return data_analyze(data, dict, data2, res_path, hyphen_thing, silent)


def change_wrong_right(wrong_right, text_data):
    if len(wrong_right) != 0:
        for e in wrong_right:
            text_data = text_data.replace(e[0], e[1])
    return text_data


def form_start_end(data, start_end, dict):
    for el in data:
        nword = el.group()
        if not interactive_spellchecker.is_word_right(nword, False, dict):
            start_end.append([el.start(), el.end(), nword])
    return start_end


def form_red_list(text_data, start_end):
    red_date = text_data
    index = 0
    mylist = []
    if len(start_end) != 0:
        for el in start_end:
            part1 = str(red_date[0:el[0] - index]) + "\x1b[31;40m" + \
                str(red_date[el[0] - index:el[1] - index]) + "\x1b[0m"
            mylist.append(part1)
            red_date = red_date[el[1] - index:]
            index = el[1]
    mylist.append(red_date)
    mylist = "".join(mylist)
    return mylist


def form_green_list(text_data, start_end, main_st):
    red_date = text_data
    index = 0
    mylist = []
    if len(start_end) != 0:
        for el in main_st:
            if el[0] != start_end[0][0]:
                part1 = str(red_date[0:el[0] - index]) + "\x1b[31;40m" + \
                    str(red_date[el[0] - index:el[1] - index]) + "\x1b[0m"
                mylist.append(part1)
                red_date = red_date[el[1] - index:]
                index = el[1]
            else:
                part1 = str(red_date[0:el[0] - index])\
                        + '*' + "\x1b[92;40m"\
                        + str(red_date[el[0] - index:el[1] - index]) \
                        + "\x1b[0m"
                mylist.append(part1)
                red_date = red_date[el[1] - index:]
                index = el[1]
    mylist.append(red_date)
    mylist = "".join(mylist)
    return mylist


def talk_while_analyze(data, wrong_right, dict, text_data, start_end):
    for e in data:
        word = e.group()
        if not interactive_spellchecker.is_word_right(word, False, dict):
            print(clear())
            green_list = form_green_list(
                text_data, [[e.start(), e.end()]], start_end)
            print(green_list)
            print(word + " " + str(e.start()))
            var = interactive_spellchecker.user_asking(word, False, dict)
            if var:
                print(up(len(var)+1))
                for ek in range(0, len(var)):
                    print(forward(10)+str(ek))
                choice = input("напечатайте номер выбранного слова"
                               "(от 0 до количества вариантов),"
                               "чтобы заменить неверное\n"
                               "НЕТ, чтобы не заменять его или МОЕ"
                               " чтобы использовать собственное взамен\n")
                numericFlag = choice.isnumeric() and\
                    (float(choice)).is_integer() and 0 <= int(choice)\
                    < len(var)
                stringdFlag = choice == "НЕТ" or choice == "МОЕ"
                while not numericFlag and not stringdFlag:
                    choice = input("напечатайте номер выбранного слова"
                                   "(от 0 до количества вариантов)\n"
                                   "чтобы заменить неверное\n"
                                   "НЕТ, чтобы не заменять его или МОЕ"
                                   " чтобы использовать собственное взамен\n")
                    numericFlag = choice.isnumeric() and 0 <= int(choice) <\
                        len(var)
                    stringdFlag = choice == "НЕТ" or choice == "МОЕ"
                if choice != "НЕТ" and choice != "МОЕ":
                    num = int(choice)
                    wrong_right.append((word, var[num]))
                elif choice == "МОЕ":
                    v = input(
                        "напечатайте слово, которое хотите использовать\n")
                    interactive_spellchecker.AddToBase(v, False, dict)
                    wrong_right.append((word, v))


def data_analyze(data, dict, text_data, res_path, hyphen, keep_silent):
    init()
    wrong_right = []
    start_end = []
    data = list(data)
    form_start_end(data, start_end, dict)
    for place in hyphen:
        if text_data[place[2]] == " ":
            text_data = text_data[:place[2]]+"-"+text_data[place[2]+1:]
    if not keep_silent:
        talk_while_analyze(data, wrong_right, dict, text_data, start_end)
    text_data = change_wrong_right(wrong_right, text_data)
    handle = open(res_path, "w")
    handle.write(text_data)
    handle.close()
    if keep_silent:
        handle = open(res_path, "a")
        handle.write("\nОшибка/слова, которого нет в словаре и номер символа,"
                     " где оно встретилось:")
        for g in start_end:
            handle.write('\n')
            handle.write(str(g[0])+" "+g[2])
            my_var = interactive_spellchecker.GetVariants(g[2], False)
            if len(my_var) == 0:
                handle.write("Варианты не найдены\n")
            else:
                handle.write('\n Варианты:')
                for v in my_var:
                    handle.write("\n")
                    handle.write(v)
                handle.write("\n==========")
        handle.close()
    path = os.path.abspath(res_path)
    print("\nИщите исправленный файл здесь\n" + path + "\nПереименуйте его,"
          "чтобы быть уверенными,\nчто он не будет переписан")


def text_prerocessing(data, hyphen):
    data1 = data.replace('-', ' ')
    itera = re.finditer(r'(\w+)-(\w+)', data)
    for e in itera:
        w1 = e.group(1)
        w2 = e.group(2)
        st = e.start()+len(w1)
        hyphen.append((w1, w2, st))
    data = re.finditer(r'[А-Яа-яЁё]+', data1)
    return data, data1
