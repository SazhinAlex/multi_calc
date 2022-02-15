from tkinter import *
from tkinter import ttk


class Figure(Frame):
    def __init__(self, root, name: str):
        super().__init__(root)
        self._name = name
        self._canvas = Canvas(self, width=500, height=500, bg='white')
        self._canvas.pack()

    def area(self):
        raise NotImplementedError('Нереализованный метод!')

    def get_name(self):
        return self._name

    def draw(self):
        raise NotImplementedError('Нереализованный метод!')


class Rectangle(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)
        self._combo = ttk.Combobox(self, values=Rectangle.what_calc(),
                                   state='readonly')
        self._combo.pack(side=LEFT, padx=5, pady=10)
        self._combo.current(0)

    @staticmethod
    def what_calc() -> tuple:
        return 'Площадь', 'Периметр'

    def area(self):
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
