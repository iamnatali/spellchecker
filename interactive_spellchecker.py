import sqlite3
from fuzzywuzzy import fuzz
import stemmer
import file_spellchecker
import os


def GetVariants(wrd, initial, dict1='virtualdict'):
    wrd = initiality_stem(wrd, initial)
    wrd = wrd.replace('ё', 'е')
    wrd = wrd.replace('-', '')
    # jaro(0-1),fuzzy(0-100),ratio(0-1)
    fuzzy = fuzz.ratio
    # fuzzy=Levenshtein.distance
    # fuzzy=Levenshtein.ratio
    # fuzzy=Levenshtein.jaro_winkler
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), st))
    conn.create_function('fuz', 2, fuzzy)
    cursor = conn.cursor()
    cursor.execute('pragma table_info("{}")'.format(dict1))
    a = cursor.fetchall()
    if a:
        c = a[0][1]
        b = a[1][1]
        if initial:
            c = b
        cursor .execute(
            'SELECT "{nb}" FROM "{ndict}"'
            ' WHERE fuz((?),"{na}")>60 ORDER BY fuz((?),"{na}")'.format(
                nb=b, na=c, ndict=dict1), (wrd, wrd))
    list = cursor.fetchall()
    list.reverse()
    list = list[0:10]
    conn.commit()
    conn.close()
    return appropriate_list(list)


def appropriate_list(list):
    new_list = []
    for k in list:
        new_list.append(k[0])
    return new_list


def main(ndict='virtualdict'):
    while True:
        wrd = input("Введите слово для проверки/Нажмите Enter для выхода\n")
        if not wrd:
            print("Спасибо за использование нашего продукта!")
            break
        print("Это начальная форма?(ДА/НЕТ)")
        flaginitial = str(input()).lower() == "ДА"
        if is_word_right(wrd, flaginitial, ndict):
            print("Это слово верно")
        else:
            user_asking(wrd, flaginitial, ndict)


def user_asking(wrd, flaginitial, ndict):
    # возвращает список вариантов, если выбрана эта опция или None
    IsUserRight = False
    while not IsUserRight:
        print("Это слово ОШИБОЧНО или НЕ содержится в словаре\n"
              "Введите:\n"
              "В - посмотреть варианты\n"
              "Д - добавить в словарь\n"
              "ДН - добавить в словарь, если слово стоит в начальной форме\n"
              "П - пропустить обработку слова")
        choice = input()
        if choice == "П":
            IsUserRight = True
        if choice == "В":
            vars = GetVariants(wrd, flaginitial, ndict)
            if len(vars) == 0:
                print("Варианты не найдены")
            else:
                print("Варианты:")
                for e in vars:
                    print(e)
                IsUserRight = True
                return vars
        elif choice == "Д":
            AddToBase(wrd, False, ndict)
            IsUserRight = True
        elif choice == "ДН":
            AddToBase(wrd, True, ndict)
            IsUserRight = True


def initiality_stem(wrd, initial):
    if not initial:
        st = stemmer.Stemmer()
        wrd = st.stem(wrd)
    return wrd


def AddToBase(wrd, initial, dict1):
    swrd = initiality_stem(wrd, initial)
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), st))
    cursor = conn.cursor()
    cursor.execute('insert into "{}" values(?,?)'.format(dict1), (swrd, wrd))
    conn.commit()
    conn.close()


def is_word_right(wrd, initial, dict1):
    wrd1 = wrd.replace('-', ' ')
    if wrd1 != wrd:
        mist = file_spellchecker.data_analyze(
            file_spellchecker.text_prerocessing(
                wrd1, [])[0], dict1,
            file_spellchecker.text_prerocessing(wrd1, [])[1],
            r"res.txt", [], False)
        if len(mist) == 0:
            return True
    else:
        wrd = initiality_stem(wrd, initial)
        wrd = wrd.replace('ё', 'е')
        st = r'speller.db'
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), st))
        cursor = conn.cursor()
        a = cursor.fetchall()
        c = ""
        b = ""
        if a:
            c = a[0][1]
            b = a[1][1]
        if initial:
            c = b
        cursor.execute(
            'SELECT "{nc}" FROM "{d}"'
            ' WHERE "{d}" MATCH (?) ORDER BY rank'.format(nc=c, d=dict1),
            (wrd, ))
        list = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(list) > 0:
            return True
        else:
            return False
