# Реализуйте программу, которая будет эмулировать работу с пространствами имен.
# Необходимо реализовать поддержку создания пространств имен и добавление в них переменных.
# В данной задаче у каждого пространства имен есть уникальный текстовый идентификатор – его имя.
#
# Вашей программе на вход подаются следующие запросы:
#
#   * create <namespace> <parent> –  создать новое пространство имен с именем <namespace> внутри пространства <parent>
#   * add <namespace> <var> – добавить в пространство <namespace> переменную <var>
#   * get <namespace> <var> – получить имя пространства, из которого будет взята переменная <var> при запросе из пространства <namespace>, или None, если такого пространства не существует
#
# Рассмотрим набор запросов
#
#   * add global a
#   * create foo global
#   * add foo b
#   * create bar foo
#   * add bar a
#
# Структура пространств имен описанная данными запросами будет эквивалентна структуре пространств имен, созданной при выполнении данного кода:
# a = 0
# def foo():
#  b = 1
#  def bar():
#     a = 2
#
# Формат входных данных:
#
# В первой строке дано число n (1 ≤ n ≤ 100) – число запросов.
# В каждой из следующих n строк дано по одному запросу.
# Запросы выполняются в порядке, в котором они даны во входных данных.
# Имена пространства имен и имена переменных представляют из себя строки длины не более 10, состоящие из строчных латинских букв.
#
# Формат выходных данных:
#
# Для каждого запроса get выведите в отдельной строке его результат.
#
# Sample Input:
# 9
# add global a
# create foo global
# add foo b
# get foo a
# get foo c
# create bar foo
# add bar a
# get bar a
# get bar b
#
# Sample Output:
# global
# None
# bar
# foo


class Namespace:
    def __init__(self, name):
        self.name = name
        self.vars = []
        self.namespaces = []
        self.parent = None

    def add_var(self, var):
        self.vars.append(var)

    def add_namespace(self, namespace):
        self.namespaces.append(namespace)

    def set_parent(self, parent):
        self.parent = parent
        parent.add_namespace(self)

    def find_namespace(self, namespace_id):
        if self.name == namespace_id:
            return self
        else:
            if len(self.namespaces) > 0:
                for child in self.namespaces:
                    result = child.find_namespace(namespace_id)
                    if result is not None:
                        return result
                return None
            else:
                return None

    def find_var(self, var):
        if var in self.vars:
            return self.name
        elif self.parent is not None:
            return self.parent.find_var(var)
        else:
            return None


root = Namespace('global')

req_num = input()

for _ in range(0, int(req_num)):
    request = input()
    (command, name, value) = request.split(' ')

    if command == 'create':
        nm = root.find_namespace(value)
        tmp = Namespace(name)
        tmp.set_parent(nm)

    if command == 'add':
        nm = root.find_namespace(name)
        nm.add_var(value)

    if command == 'get':
        nm = root.find_namespace(name)
        print(nm.find_var(value))
