from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


f_template = open('test_template.html', 'r', encoding='utf-8-sig')
html = f_template.read()
f_template.close()

template = Template(html)

result_html = template.render(name="Алина")

# создадим файл для HTML-страницы
f = open('test.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()

# ------------------------------------------------------------------------
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('ind_test_template.html')

student = [
    ["Алина", "Бизнес-информатика", ["Базы данных",
                                     "Программирование", "Эконометрика", "Статистика"], "ж"],
    ["Вадим", "Экономика", ["Информатика", "Теория игр",
                            "Экономика", "Эконометрика", "Статистика"], "м"],
    ["Ксения", "Экономика", ["Информатика", "Теория игр",
                             "Статистика"], "ж"]
]


def add_spaces(text):
    return " ".join(text)


def word_form(n):
    if 10 <= n <= 20:
        n = 0
    else:
        n = n % 10
    match n:
        case 0 | 5 | 6 | 7 | 8 | 9:
            return str(n) + ' дисциплин'
        case 1:
            return str(n) + ' дисциплину'
        case 2 | 3 | 4:
            return str(n) + ' дисциплины'


template.globals["add_spaces"] = add_spaces
template.globals["word_form"] = word_form

user = student[0]
result_html = template.render(user=user,
                              add_spaces=add_spaces,
                              word_form=word_form,
                              n=len(user[2]))
# создадим файл для HTML-страницы
f = open('test_student.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
