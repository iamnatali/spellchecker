import interactive_spellchecker


def get_allparts(s):
    allparts = []
    for e in range(1, len(s) + 1):
        part = s[:e]
        vars = interactive_spellchecker.GetVariants(
            s[:e], False, 'virtualdict')
        for v in vars:
            if part == v:
                allparts.append(part)
    return allparts


def print_children(children, mainstring):
    resstrins = []
    for e in children:
        r = e
        s = []
        while r:
            s.insert(0, r.name)
            r = r.father
        s.append(mainstring[len("".join(s)):])
        resstrins.append(" ".join(s))
    return resstrins


class Node():
    def __init__(self, str, lstr):
        self.name = str
        self.left = lstr
        self.children = []
        self.father = None


def process_word(s):
    print("идет обработка запроса, пожалуйста подождите")
    node = Node("", s)
    root = node
    children = []
    children1 = []
    stack = []
    stack.append(root)
    while len(stack) != 0:
        root = stack.pop()
        st = root.left
        a = get_allparts(st)
        if len(a) == 0:
            children1.append(root)
        for e in a:
            n = Node(e, st[len(e):])
            n.father = root
            n.father = root
            if st[len(e):] != "":
                stack.append(n)
            else:
                children.append(n)
    resstrings = print_children(children, s)
    resstrings1 = print_children(children1, s)
    print("Наиболее вероятные варианты:")
    for e in resstrings:
        print(e)
    print("Варианты, состоящие из неполностью совпавших слов:")
    for e in resstrings1:
        print(e)
    return resstrings


def main():
    while True:
        wrd = input("Введите слово для проверки/Нажмите Enter для выхода\n")
        if not wrd:
            print("Спасибо за использование нашего продукта!")
            break
        w = wrd.replace(" ", "")
        process_word(w)
