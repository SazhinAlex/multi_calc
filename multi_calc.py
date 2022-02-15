from tkinter import *
from tkinter import ttk


class Figure(Frame):
    def __init__(self, root, name: str):
        super().__init__(root)
        self._name = name
        self._canvas = Canvas(self, width=500, height=500, bg='white')
        self._canvas.pack(side=TOP)

    def area(self):
        raise NotImplementedError('Нереализованный метод!')

    def get_name(self):
        return self._name

    def draw(self):
        raise NotImplementedError('Нереализованный метод!')


class Rectangle(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)
        self.__calc_frame = Frame(self)
        self._combo = ttk.Combobox(self.__calc_frame, values=Rectangle.what_calc(),
                                   state='readonly')
        self._combo.pack(side=LEFT, padx=10, pady=10)
        self._combo.current(0)
        self.__a_frame = Frame(self.__calc_frame)
        self.__a_lbl = Label(self.__a_frame, text='a: ')
        self.__a_lbl.pack(side=LEFT)
        self.__a_entry = Entry(self.__a_frame)
        self.__a_entry.pack(side=LEFT)
        self.__a_frame.pack(side=TOP, pady=10)
        self.__b_frame = Frame(self.__calc_frame)
        self.__b_lbl = Label(self.__b_frame, text='b: ')
        self.__b_lbl.pack(side=LEFT)
        self.__b_entry = Entry(self.__b_frame)
        self.__b_entry.pack(side=LEFT)
        self.__b_frame.pack(side=TOP, pady=10)
        self.__calc_frame.pack(side=TOP, fill='x')
        self.__sep = ttk.Separator(self, orient='horizontal')
        self.__sep.pack(fill='x')
        self.__result_frame = Frame(self)
        self.__result_lbl = Label(self.__result_frame, text='Результат: ', font='Arial 20')
        self.__result_lbl.pack(side=LEFT)
        self.__result_val_lbl = Label(self.__result_frame, font='Arial 20')
        self.__result_val_lbl.pack(side=LEFT)
        self.__result_frame.pack(side=TOP)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр'

    def area(self):
        pass

    def perimetr(self):
        pass

    def draw(self):
        pass


class Square(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр'

    def area(self):
        pass

    def draw(self):
        pass


class Triangle(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр'

    def area(self):
        pass

    def draw(self):
        pass


class Circle(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр'

    def area(self):
        pass

    def draw(self):
        pass


class Cube(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр', 'Объем'

    def area(self):
        pass

    def draw(self):
        pass


# Калькулятор может быть только один. На данный момент...
# Паттерн синглтон через метаклассы
class MetaCalculator(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaCalculator, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Calculator(metaclass=MetaCalculator):

    def __init__(self):
        self.__root = Tk()
        self.__root.geometry('500x700')
        self.__root.resizable(False, False)
        self.__notebook = ttk.Notebook(self.__root)
        self.__notebook.pack()

    def run(self):
        self.__root.mainloop()

    def get_notebook(self):
        return self.__notebook

    def add_calculable_figures(self, figures: tuple):
        for figure_obj in figures:
            figure_obj.pack(fill='both', expand=True)
            self.__notebook.add(figure_obj, text=figure_obj.get_name())


if __name__ == '__main__':
    calc_app = Calculator()
    parent_notebook = calc_app.get_notebook()
    figs = (
        Rectangle(parent_notebook, 'Прямоугольник'),
    )
    calc_app.add_calculable_figures(figs)
    calc_app.run()
