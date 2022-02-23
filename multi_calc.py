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
                        sv = in_dict[in_lbl][0]
                        trace_info = sv.trace_info()
                        for event_type, fn_name in trace_info:
                            if 'write' in event_type:
                                sv.trace_remove('write', fn_name)
    
                frame.pack_forget()


class Rectangle(Figure):
    def __init__(self, name: str):
        super().__init__(name)
        for choice in self._choices:
            if choice == 'Периметр':
                a_sv = tk.DoubleVar(name='a_perimetr')
                b_sv = tk.DoubleVar(name='b_perimetr')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, {'b': [b_sv, ]})
            elif choice == 'Площадь':
                a_sv = tk.DoubleVar(name='a_area')
                b_sv = tk.DoubleVar(name='b_area')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, {'b': [b_sv, ]})


    def area(self, var, index, mode):
        try:
            a_val = self._choices['Площадь']['inputs'][0]['a'][0].get()
            b_val = self._choices['Площадь']['inputs'][1]['b'][0].get()
        except:
            return
        area = a_val * b_val
        self._choices['Площадь']['output']['text'] = area
        canvas = self._choices['Площадь']['canvas']
        self.draw(canvas, a_val, b_val)

    def perimetr(self, var, index, mode):
        try:
            a_val = self._choices['Периметр']['inputs'][0]['a'][0].get()
            b_val = self._choices['Периметр']['inputs'][1]['b'][0].get()
        except:
            return
        perimetr = (a_val + b_val) * 2
        self._choices['Периметр']['output']['text'] = perimetr
        canvas = self._choices['Периметр']['canvas']
        self.draw(canvas, a_val, b_val)

    # На вход параметры рисуемой фигуры. self.draw(a, b) a - длина стороны а; b - длина стороны b
    def draw(self, canvas: tk.Canvas, *args):
        canv_w = canvas.winfo_width()
        canv_h = canvas.winfo_height()
        x1 = int(canv_w * 0.15)
        y1 = int(canv_h * 0.15)
        x2 = int(canv_w * 0.85)
        y2 = int(canv_h * 0.85)

        if len(args) >= 2 and args[0] > 0.0 and args[1] > 0.0:
            max_val = max(args)
            a_coeff = args[0] / max_val
            b_coeff = args[1] / max_val
            x2 = int(x2 * a_coeff)
            y2 = int(y2 * b_coeff)

        a_x = int((x2 + x1) * 0.5)
        a_y = y2 + 10
        b_x = x2 + 10
        b_y = int((y2 + y1) * 0.5)

        canvas.delete('all')
        canvas.create_rectangle(x1, y1, x2, y2)
        canvas.create_text(a_x, a_y, text='a', fill='black', font=('Helvetica 15 bold'))
        canvas.create_text(b_x, b_y, text='b', fill='black', font=('Helvetica 15 bold'))


class Square(Figure):
    def __init__(self, name: str):
        super().__init__(name)
        for choice in self._choices:
            if choice == 'Периметр':
                a_sv = tk.DoubleVar(name='a_perimetr')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, )
            elif choice == 'Площадь':
                a_sv = tk.DoubleVar(name='a_area')
                self._choices[choice]['inputs'] = ({'a': [a_sv, ]}, )

    def area(self, var, index, mode):
        try:
            a_val = self._choices['Площадь']['inputs'][0]['a'][0].get()
        except:
            return
        area = a_val ** 2
        self._choices['Площадь']['output']['text'] = area
        canvas = self._choices['Площадь']['canvas']
        self.draw(canvas, a_val)

    def perimetr(self, var, index, mode):
        try:
            a_val = self._choices['Периметр']['inputs'][0]['a'][0].get()
        except:
            return
        perimetr = a_val * 4
        self._choices['Периметр']['output']['text'] = perimetr
        canvas = self._choices['Периметр']['canvas']
        self.draw(canvas, a_val)

    def draw(self, canvas: tk.Canvas, *args):
        canv_w = canvas.winfo_width()
        canv_h = canvas.winfo_height()
        min_l = min((canv_w, canv_h))
        x1 = int(min_l * 0.15)
        y1 = int(min_l * 0.15)
        x2 = int(min_l * 0.85)
        y2 = int(min_l * 0.85)

        a_x = int((x2 + x1) * 0.5)
        a_y = y2 + 10

        canvas.delete('all')
        canvas.create_rectangle(x1, y1, x2, y2)
        canvas.create_text(a_x, a_y, text='a', fill='black', font=('Helvetica 15 bold'))


class Triangle(Figure):
    def __init__(self, name: str):
        super().__init__(name)

    def area(self, var, index, mode):
        return super().area(var, index, mode)

    def perimetr(self, var, index, mode):
        return super().perimetr(var, index, mode)

    def draw(self, canvas: tk.Canvas, *args):
        return super().draw(canvas, *args)


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
        Square('Квадрат')
    )
    calc_app.add_features(features)
    calc_app.run()
