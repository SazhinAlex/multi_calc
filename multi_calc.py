from audioop import add
import tkinter as tk
from tkinter import ttk


class Figure:
    def __init__(self, name: str):
        self._name = name
        self._choices = {}
        for choice in self.__class__.what_calc():
            fn = self.area if choice == 'Площадь' else self.perimetr
            self._choices[choice] = {
                'frames': {'inputs_frame': None, 'parent_frame': None}, 
                'inputs': None, 
                'canvas': None, 
                'output': None, 
                'solve_fn': fn
                }

    def __str__(self) -> str:
        return self._name

    @staticmethod
    def what_calc() -> tuple:
        return ('Площадь', 'Периметр')

    def get_choices(self) -> list:
        return self._choices

    def area(self, var, index, mode):
        raise NotImplementedError('Нереализованный метод!')

    def perimetr(self, var, index, mode):
        raise NotImplementedError('Нереализованный метод!')

    def draw(self, canvas: tk.Canvas, *args):
        raise NotImplementedError('Нереализованный метод!')

    def solve_selected(self):
        raise NotImplementedError('Нереализованный метод!')


class Rectangle(Figure):
    def __init__(self, name: str):
        super().__init__(name)
        for choice in self._choices:
            if choice == 'Периметр':
                a_sv = tk.DoubleVar(name='a')
                b_sv = tk.DoubleVar(name='b')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, {'b': [b_sv, ]})
            elif choice == 'Площадь':
                a_sv = tk.DoubleVar(name='a')
                b_sv = tk.DoubleVar(name='b')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, {'b': [b_sv, ]})


    def area(self, var, index, mode):
        print('Площаль')

    def perimetr(self, var, index, mode):
        print('Периметр')

    # На вход параметры рисуемой фигуры. self.draw(a, b) a - длина стороны а; b - длина стороны b
    def draw(self, canvas: tk.Canvas, *args):
        canv_w = canvas.winfo_width()
        canv_h = canvas.winfo_height()
        canvas.create_rectangle(100, 100, 400, 400)

    def solve_selected(self, event):
        selected = event.widget.get()
        for choice in self._choices:
            frame = self._choices[choice]['frames']['inputs_frame']
            inputs = self._choices[choice]['inputs']
            solve_fn = self._choices[choice]['solve_fn']
            if choice == selected:
                for in_dict in inputs:
                    for in_lbl in in_dict:
                        in_dict[in_lbl][0].trace_add('write', solve_fn)
                frame.pack()
            else:
                for in_dict in inputs:
                    for in_lbl in in_dict:
                        in_dict[in_lbl][0].trace_info().clear()
                frame.pack_forget()


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
# Паттерн - синглтон через метаклассы
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
        # self.__root.geometry('500x700')
        self.__root.resizable(False, False)
        self.__notebook = ttk.Notebook(self.__root)
        self.__notebook.pack()

    def run(self):
        self.__root.mainloop()

    def get_notebook(self):
        return self.__notebook


    def add_features(self, features: tuple):
        for feature in features:
            choices = feature.get_choices()
            feature_frame = tk.Frame(self.__notebook)
            canvas = tk.Canvas(feature_frame, width=500, height=500, bg='white')
            canvas.pack(side=tk.TOP)
            calc_frame = tk.Frame(feature_frame)
            combo = ttk.Combobox(calc_frame, state='readonly', values=feature.__class__.what_calc())
            combo.pack(side=tk.LEFT, padx=10, pady=10)
            combo.current(0)
            blank_frame = tk.Frame(calc_frame)
            blank_frame.pack(side=tk.TOP)
            
            calc_frame.pack(side=tk.TOP, fill='x')
            sep = ttk.Separator(feature_frame, orient='horizontal')
            sep.pack(fill='x')
            result_frame = tk.Frame(feature_frame)
            result_lbl = tk.Label(result_frame, text='Результат: ', font='Arial 20')
            result_lbl.pack(side=tk.LEFT)
            result_val_lbl = tk.Label(result_frame, font='Arial 20')
            result_val_lbl.pack(side=tk.LEFT)
            result_frame.pack(side=tk.TOP)
            combo.bind("<<ComboboxSelected>>", feature.solve_selected)
            
            for choice in choices:
                params_frame = tk.Frame(blank_frame)
                # params_frame.pack(side=tk.LEFT)
                choices[choice]['frames']['inputs_frame'] = params_frame
                choices[choice]['frames']['parent_frame'] = blank_frame
                choices[choice]['canvas'] = canvas
                choices[choice]['output'] = result_val_lbl

                inputs = choices[choice]['inputs']
                for input in inputs:
                    for input_lbl in input:
                        sv = input[input_lbl][0]
                        in_frame = tk.Frame(params_frame)
                        in_lbl = tk.Label(in_frame, text=f'{input_lbl}: ')
                        in_lbl.pack(side=tk.LEFT)
                        in_entry = tk.Entry(in_frame, textvariable=sv)
                        input[input_lbl].append(in_entry)
                        in_entry.pack(side=tk.LEFT)
                        in_frame.pack(side=tk.TOP, pady=10)

            self.__notebook.add(feature_frame, text=str(feature))
            self.__features.append(feature)
            combo.event_generate("<<ComboboxSelected>>")

if __name__ == '__main__':
    calc_app = Calculator()
    features = (
        Rectangle('Прямоугольник'),
    )
    calc_app.add_features(features)
    calc_app.run()
