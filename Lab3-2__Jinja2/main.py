# Импортировать объект-шаблон из модуля jinja2
from jinja2 import Template
import numpy as np
# В начале программы импортировать модуль для построения графиков
import matplotlib.pyplot as plt


# Описать функцию, в качестве параметра передать значение аргумента x
# функция должна возвращать значение заданной функции, вычисленной от x
def f(x, n_var):
    y = 0
    if n_var == 0:
        y = x ** 3 - 6 * x ** 2 + x + 5
    elif n_var == 1:
        y = x ** 2 - 5 * x + 1
    elif n_var == 2:
        y = 1 / (x ** 2 + 1)
    return y


# Определить функции для построения графика по спискам координат x и y
def create_pict(x, y):
    # Построить линию графика, установить для нее цвет и толщину:
    line = plt.plot(x, y)
    plt.setp(line, color="darkblue", linewidth=2)
    # Вывести 2 оси, установить их в позицию zero:
    plt.gca().spines["left"].set_position("zero")
    plt.gca().spines["bottom"].set_position("zero")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    # Сохранть результат построения в файл:
    plt.savefig("pict.jpg")

    # Вернуть имя созданного файла
    return "pict.jpg"


# Задать начало a и конец b интервала построения функции,
# количество точек построения.
a = -2
b = 6
n = 100
# Вычислить шаг
h = (abs(a) + abs(b)) / (n - 1)
# Сформировать список со значениями аргумента
x_list = [i for i in np.arange(a, b + h, h) if (i - h < b)]
# print(x_list)
# Сформировать список со значениями функции для
# каждого элемента списка x_list
# Номер функции
n_var = 2
f_list = [f(x, n_var) for x in np.array(x_list)]
# print(f_list)
# Прочитать шаблон из файла function_template.html
f_template = open('function_template.html', 'r', encoding='utf-8-sig')
html = f_template.read()
f_template.close()
# Создать объект-шаблон
template = Template(html)
# Указать, что в шаблоне будет использована функция len
template.globals["len"] = len
# Cоздадать файл для HTML-страницы
file = open('function.html', 'w', encoding='utf-8-sig')

name_pict = create_pict(x_list, f_list)
list_of_functions = ['f(x)', 'y(x)', 'z(x)']

# Сгенерировать страницу на основе шаблона
result_html = template.render(n_var=n_var,
                              x=[round(i, 4) for i in x_list],
                              y=[round(i, 4) for i in f_list],
                              pict=name_pict,
                              list_f=list_of_functions,
                              a=a,
                              b=b,
                              n=n)
# Вывести сгенерированную страницу в файл
file.write(result_html)
file.close()
