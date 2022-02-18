import tkinter as tk
from tkinter import ttk


class Figure:
    def __init__(self, root, name: str):
        super().__init__(root)
        self._name = name
        self.__choices = []
        for choice in self.__class__.what_calc():
            data = {
                'name': choice,
                'frame': None,
                'inputs': None
            }
            
            self._choices.append(data)

    def __str__(self) -> str:
        return self._name

    @staticmethod
    def what_calc() -> tuple:
        return ('Площадь', 'Периметр')

    def get_choices(self) -> list:
        return self.__choices

    def area(self, var, index, mode):
        raise NotImplementedError('Нереализованный метод!')

    def perimetr(self, var, index, mode):
        raise NotImplementedError('Нереализованный метод!')

    def draw(self, canvas: tk.Canvas, *args):
        raise NotImplementedError('Нереализованный метод!')


class Rectangle(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)
        self.__a_frame = tk.Frame(self._params_frame)
        self.__a_lbl = tk.Label(self.__a_frame, text='a: ')
        self.__a_lbl.pack(side=tk.LEFT)
        self.__a_val = tk.StringVar()
        self.__a_entry = tk.Entry(self.__a_frame, textvariable=self.__a_val)

        self.__a_entry.pack(side=tk.LEFT)
        self.__a_frame.pack(side=tk.TOP, pady=10)
        self.__b_frame = tk.Frame(self._params_frame)
        self.__b_lbl = tk.Label(self.__b_frame, text='b: ')
        self.__b_lbl.pack(side=tk.LEFT)
        self.__b_val = tk.StringVar()
        self.__b_entry = tk.Entry(self.__b_frame, textvariable=self.__b_val)
        self.__b_entry.pack(side=tk.LEFT)
        self.__b_frame.pack(side=tk.TOP, pady=10)

        calc_variants = self.__class__.what_calc()
        self._combo.configure(values=calc_variants)
        self._combo.current(0)
        self.__a_val.trace_add('write', self.input_changed)
        self.__b_val.trace_add('write', self.input_changed)


    def get_choices(self) -> list:
        common_choices = super().get_choices()
        for choice in common_choices:
            if choice['name'] == 'Периметр':
                choice['inputs'] = (
                    {'a': tk.StringVar('write', self.perimetr, name='a')}, 
                    {'b': tk.StringVar('write', self.perimetr, name='b')}
                    )
            elif choice['name'] == 'Площадь':
                choice['inputs'] = (
                    {'a': tk.StringVar('write', self.area, name='a')}, 
                    {'b': tk.StringVar('write', self.area, name='b')}
                    )

        return common_choices

    def area(self, var, index, mode):
        return super().area(var, index, mode)

    def perimetr(self, var, index, mode):
        return super().perimetr(var, index, mode)

    # На вход параметры рисуемой фигуры. self.draw(a, b) a - длина стороны а; b - длина стороны b
    def draw(self, canvas: tk.Canvas, *args):
        canv_w = self._canvas.winfo_width()
        canv_h = self._canvas.winfo_height()
        self._canvas.create_rectangle(100, 100, 400, 400)


class Square(Figure):
    def __init__(self, root, name: str):
        super().__init__(root, name=name)

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
        self.__features = []
        self.__root = tk.Tk()
        self.__root.geometry('500x700')
        self.__root.resizable(False, False)
        self.__notebook = ttk.Notebook(self.__root)
        self.__notebook.pack()

        self._canvas = tk.Canvas(self, width=500, height=500, bg='white')
        self._canvas.pack(side=tk.TOP)
        self.__calc_frame = tk.Frame(self)
        self._combo = ttk.Combobox(self.__calc_frame, state='readonly')
        self._combo.pack(side=tk.LEFT, padx=10, pady=10)
        # self._combo.current(0)
        self._params_frame = tk.Frame(self.__calc_frame)
        self._params_frame.pack(side=tk.LEFT)
        self.__calc_frame.pack(side=tk.TOP, fill='x')
        self.__sep = ttk.Separator(self, orient='horizontal')
        self.__sep.pack(fill='x')
        self.__result_frame = tk.Frame(self)
        self.__result_lbl = tk.Label(self.__result_frame, text='Результат: ', font='Arial 20')
        self.__result_lbl.pack(side=tk.LEFT)
        self._result_val_lbl = tk.Label(self.__result_frame, font='Arial 20')
        self._result_val_lbl.pack(side=tk.LEFT)
        self.__result_frame.pack(side=tk.TOP)
        self._combo.bind("<<ComboboxSelected>>", self.solve_selected)

    def run(self):
        self.__root.mainloop()

    def get_notebook(self):
        return self.__notebook


    def add_features(self, features: tuple):
        for feature in features:
            feature_dict = {
                'readable_name': None,
                'choices': None,
                'inputs_frame': None,
                'feature_object': None
            }

            readable_name = feature.get_name()



if __name__ == '__main__':
    calc_app = Calculator()
    parent_notebook = calc_app.get_notebook()
    features = (
        Rectangle(parent_notebook, 'Прямоугольник'),
    )
    calc_app.add_features(features)
    calc_app.run()
