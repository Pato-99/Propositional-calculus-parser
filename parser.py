#!/usr/bin/python3

# ------- Parser vyrokove logiky ----------
# formule zadavejte v reverse polish notaci
# zapis:   negace -> '!'
#          konjunkce -> '*'
#          disjunkce -> '+'
#          implikace -> 'i'
#          ekvivalence -> 'e'
#          literal -> jakekoliv velke pismeno z ASCII

class LinkedList:
    def __init__(self):
        self.head = None

    # when print is called
    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.name)
            node = node.next
        nodes.append("None")
        return "->".join(nodes)

    # makes list iterable
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def add_first(self, node):
        node.next = self.head
        self.head = node

    def add_last(self, node):
        curr_node = Node
        if not self.head:
            self.head = node
            return

        for curr_node in self:
            pass
        curr_node.next = node

    def remove_first(self):
        if not self.head:
            raise Exception("List is empty")
        self.head = self.head.next

    def draw_table(self, node, literals):
        if not node.ohodnoceni or not literals:
            return
        o_base = self.generate_literals_eval(len(literals))
        o_len = 2**len(literals)

        for i in range(o_len):
            if node.ohodnoceni[i]:
                node.ohodnoceni[i] = 1
            else:
                node.ohodnoceni[i] = 0

        for i in range(len(o_base)):
            for j in range(o_len):
                if o_base[i][j]:
                    o_base[i][j] = 1
                else:
                    o_base[i][j] = 0

        for i in range(len(o_base)):
            print("{}   ".format(literals[i]), end='')
        print(node.name)

        for i in range(o_len):
            for j in range(len(o_base)):
                print("{} |".format(o_base[j][i]), end=' ')
            print(" {} ".format(node.ohodnoceni[i]))

    # vygeneruje pocatecni hodnoty pro zadany pocet literalu
    def generate_literals_eval(self, count):
        eval = []
        size = 2**count
        repeat = size
        for i in range(count):
            o = []
            in_true = True
            repeat //= 2
            for j in range(size):
                o.append(in_true)
                if (j + 1) % repeat == 0:
                    if in_true:
                        in_true = False
                    else:
                        in_true = True
            eval.append(o)
        return eval

class Node:
    def __init__(self, name=None, ohodnoceni=None):
        self.name = name
        self.ohodnoceni = ohodnoceni
        self.next = None

    def __repr__(self):
        return self.name

    def copy(self):
        return self.name, self.ohodnoceni

    def negate(self):
        self.name = '!' + self.name
        neg = []
        lenA = len(self.ohodnoceni)
        for i in range(lenA):
            if self.ohodnoceni[i]:
                neg.append(False)
            else:
                neg.append(True)
        self.ohodnoceni = neg


def get_ohodnoceni(a, b, spojka):
    result = []
    if spojka == "*":
        for a, b in zip(a, b):
            result.append(a and b)

    if spojka == "+":
        for a, b in zip(a, b):
            result.append(a or b)

    if spojka == "i":
        for a, b in zip(a, b):
            if not a:
                result.append(True)
                continue
            if a and b:
                result.append(True)
                continue
            result.append(False)

    if spojka == "e":
        for a, b in zip(a, b):
            if a and b or (not a) and (not b):
                result.append(True)
            else:
                result.append(False)

    return result


def count_literals(str):
    count = 0
    literals = []
    for char in str:
        if char.isupper() and char.isalpha() and char not in literals:
            count += 1
            literals.append(char)
    return count


def read_input():
    literals = ""
    llist = LinkedList()
    inputstr = input()
    c = count_literals(inputstr)
    ohodnoceni = llist.generate_literals_eval(c)
    for char in inputstr:
        if char == '*' or char == '+' or char == '!' or char == 'i' or char == 'e':
            node = Node(char)
            llist.add_last(node)
        else:
            if char.isupper() and char.isalpha():
                if char not in literals:
                    literals += char
                node = Node(char, ohodnoceni[literals.find(char)])
                llist.add_last(node)

    return llist, literals


#  main program
llist, literals = read_input()
o = []
#print(llist)

while llist.head:
    if not llist.head.next:
        break

    while llist.head.ohodnoceni:
        o.append(llist.head.copy())
        llist.remove_first()

    if llist.head.name == '!':
        llist.remove_first()
        data = o.pop()
        node = Node(data[0], data[1])
        node.negate()
        llist.add_first(node)

        while o:
            data = o.pop()
            node = Node(data[0], data[1])
            llist.add_first(node)

    else:
        if len(o) < 2:
            llist.head = None
            break
        data1 = o.pop()
        data2 = o.pop()
        node = Node("({}{}{})".format(data2[0], llist.head.name, data1[0]),
                    get_ohodnoceni(data2[1], data1[1], llist.head.name))

        llist.remove_first()
        llist.add_first(node)

        while o:
            data = o.pop()
            node = Node(data[0], data[1])
            llist.add_first(node)

   # print(llist)


if llist.head:
    print("Tabulka:")
    llist.draw_table(llist.head, literals)

    count = 0
    total = len(llist.head.ohodnoceni)
    for item in llist.head.ohodnoceni:
        if item:
            count += 1

    if not count:
        print("Formule je kontradikce")
    elif count == total:
        print("Formule je tautologie")
    else:
        print("Formule je splnitelna pro {} ohodnoceni z {}".format(count, total))

else:
    print("Spatne zadana formule")
