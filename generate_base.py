import sqlite3
import stemmer
import file_spellchecker
import interactive_spellchecker
import os


def virt_table_creation(vd, vw):
    vw1 = vw + "full"
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.abspath(__file__)), st))
    cursor = conn.cursor()
    try:
        if vd != 'virtualdict':
            cursor.execute("insert into tablenames values(?,?)",
                           (vd, vw))
        cursor.execute("CREATE VIRTUAL TABLE '{}' USING fts5('{}','{}')".
                       format(vd, vw, vw1))
    except BaseException:
        print('Base with this name already exists.'
              'Please, try generate base with another name again.')
    conn.commit()
    conn.close()


def virtualdictinit(list, vd):
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.abspath(__file__)), st))
    cursor = conn.cursor()
    st = stemmer.Stemmer()
    for l in list:
        cursor.execute("insert into {} values(?,?)".
                       format(vd), (st.stem(l), l))
    conn.commit()
    conn.close()


def getavailabledicts():
    st = r'speller.db'
    conn = sqlite3.connect(os.path.join
                           (os.path.dirname
                            (os.path.abspath(__file__)), st))
    cursor = conn.cursor()
    cursor.execute('SELECT names FROM tablenames')
    nlist = cursor.fetchall()
    conn.commit()
    conn.close()
    return nlist


def gen_file_into_words(path):
    handle = open(path, errors='ignore', encoding='utf-8')
    data = handle.read()
    data = file_spellchecker.text_prerocessing(data, [])[0]
    new_data = []
    for l in data:
        new_data.append(l.group())
    handle.close()
    return new_data


def question(str):
    print(str)
    return input()


def main(path):
    data = gen_file_into_words(path)
    vd = question('enter name of your base'
                  '(you will not need to remember it)')
    vw = "col"
    nlist = getavailabledicts()
    nnlist = interactive_spellchecker.appropriate_list(nlist)
    IsUserRight = False
    while not IsUserRight:
        if vd in nnlist:
            vd = question('Base with this name already exists.'
                          'Please, try generate base with another name again.')
        else:
            virt_table_creation(vd, vw)
            virtualdictinit(data, vd)
            IsUserRight = True
