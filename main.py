import tkinter as tk
from tkinter import ttk
from typing import Callable
import sympy as sp

def linear_algorithm(x: int, y: int, z: int, accuracy: int = 5) -> float:
    """
    Выполняет расчет по линейному алгоритму, который включает в себя 
    несколько математических операций с синусом, косинусом и атангенсом.

    Алгоритм вычисляет значение выражения:
        ((1 + sin(x + y)^2) / |x - (2 * y) / (1 + x^2 * y^2)|) * x^|y| + cos^2(atan(1/z))
    
    Параметры:
    x (int): Переменная x, участвующая в вычислениях.
    y (int): Переменная y, участвующая в вычислениях.
    z (int): Переменная z, участвующая в вычислениях.
    accuracy (int, опционально): Точность вычислений (по умолчанию 5 знаков после запятой).

    Возвращает:
    float: Результат вычислений, округленный до указанной точности.
    """
    # Синус выражения (x + y) в квадрате
    sin_term = sp.sin(x + y)**2
    # Числитель выражения
    numerator = 1 + sin_term
    # Знаменатель выражения
    denominator_expression = (2 * y) / (1 + x**2 * y**2)
    denominator = sp.Abs(x - denominator_expression)
    # Косинус квадрат арктангенса 1/z
    cos_term = sp.cos(sp.atan(1 / z))**2
    # Основное выражение для вычислений
    expression = (numerator / denominator) * x**sp.Abs(y) + cos_term
    # Округление результата до указанной точности
    result = expression.evalf(accuracy)
    return result

def branching_algorithm(x_val: float, y_val: float, f_func: Callable[[sp.Symbol], sp.Expr]) -> float:
    """
    Выполняет вычисление значения разветвляющейся функции на основе заданных условий и математических операций.
    В зависимости от значений x и y функция может принимать одно из нескольких выражений.

    Алгоритм использует кусочную функцию, где выбор выражения зависит от условий:
        - Если x * y > 12, вычисляется f(x)^3 + cot(y)
        - Если x * y < 7, вычисляется sinh(f(x)^3) + y^2
        - В остальных случаях вычисляется cos(x - f(x)^3)
    
    Параметры:
    x_val (float): Значение переменной x.
    y_val (float): Значение переменной y.
    f_func (Callable[[sp.Symbol], sp.Expr]): Функция f(x), которая будет применяться в выражениях.

    Возвращает:
    float: Результат вычислений в зависимости от выбранной функции и условий.
    """
    x, y = sp.symbols('x y')
    # Применяем выбранную функцию к x и возводим результат в куб
    f_cubed = f_func(x)**3
    # Выражения для разных условий
    part1 = f_cubed + sp.cot(y)
    part2 = sp.sinh(f_cubed) + y**2
    part3 = sp.cos(x - f_cubed)
    # Условия для выбора соответствующего выражения
    condition1 = x * y > 12
    condition2 = x * y < 7
    # Кусочная функция, которая зависит от условий
    func = sp.Piecewise((part1, condition1), (part2, condition2), (part3, True))
    # Подставляем значения x и y и вычисляем результат
    result = func.subs({x: x_val, y: y_val})
    return result.evalf()

class CalculatorApp:
    def __init__(self, root):
        """
        Инициализация приложения калькулятора.

        Параметры:
        root (tk.Tk): Корневой элемент интерфейса (главное окно приложения).
        """
        self.root = root
        self.root.title("Калькулятор")

        self.tab_control = ttk.Notebook(self.root)
        
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Линейный алгоритм")
        
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Разветвляющийся алгоритм")
        
        self.tab_control.pack(expand=1, fill="both")

        self.create_linear_algorithm_widgets()
        self.create_piecewise_function_widgets()

    def create_linear_algorithm_widgets(self):
        """
        Создает виджеты для ввода данных и отображения результата линейного алгоритма.
        """
        self.img = tk.PhotoImage(file="images/2.png")   
        self.image_label = tk.Label(self.tab1, image=self.img)
        self.image_label.grid(row=0, column=0, columnspan=2, pady=10)   

        self.label_x = tk.Label(self.tab1, text="x:")
        self.label_x.grid(row=1, column=0)
        self.entry_x = tk.Entry(self.tab1)
        self.entry_x.grid(row=1, column=1)
        
        self.label_y = tk.Label(self.tab1, text="y:")
        self.label_y.grid(row=2, column=0)
        self.entry_y = tk.Entry(self.tab1)
        self.entry_y.grid(row=2, column=1)
        
        self.label_z = tk.Label(self.tab1, text="z:")
        self.label_z.grid(row=3, column=0)
        self.entry_z = tk.Entry(self.tab1)
        self.entry_z.grid(row=3, column=1)

        self.label_accuracy = tk.Label(self.tab1, text="Accuracy:")
        self.label_accuracy.grid(row=4, column=0)
        self.entry_accuracy = tk.Entry(self.tab1)
        self.entry_accuracy.grid(row=4, column=1)
        self.entry_accuracy.insert(0, "5")

        self.result_label = tk.Label(self.tab1, text="Result:")
        self.result_label.grid(row=5, column=0)

        self.result_display = tk.Label(self.tab1, text="")
        self.result_display.grid(row=5, column=1)

        self.calculate_button = tk.Button(self.tab1, text="Calculate", command=self.calculate_linear_algorithm)
        self.calculate_button.grid(row=6, columnspan=2)

    def create_piecewise_function_widgets(self):
        """
        Создает виджеты для ввода данных и отображения результата разветвляющегося алгоритма .
        """
        self.img2 = tk.PhotoImage(file="images/1.png")   
        self.image_label2 = tk.Label(self.tab2, image=self.img2)
        self.image_label2.grid(row=0, column=0, columnspan=2, pady=10) 

        self.label_x2 = tk.Label(self.tab2, text="x:")
        self.label_x2.grid(row=1, column=0)
        self.entry_x2 = tk.Entry(self.tab2)
        self.entry_x2.grid(row=1, column=1)

        self.label_y2 = tk.Label(self.tab2, text="y:")
        self.label_y2.grid(row=2, column=0)
        self.entry_y2 = tk.Entry(self.tab2)
        self.entry_y2.grid(row=2, column=1)

        self.label_func = tk.Label(self.tab2, text="Выберите функцию:")
        self.label_func.grid(row=3, column=0)
        self.func_combobox = ttk.Combobox(self.tab2, values=["cot", "sin", "cos", "tan"], state="readonly")
        self.func_combobox.grid(row=3, column=1)
        self.func_combobox.set("cot")   

        self.result_label2 = tk.Label(self.tab2, text="Result:")
        self.result_label2.grid(row=4, column=0)

        self.result_display2 = tk.Label(self.tab2, text="")
        self.result_display2.grid(row=4, column=1)

        self.calculate_button2 = tk.Button(self.tab2, text="Calculate", command=self.calculate_piecewise_function)
        self.calculate_button2.grid(row=5, columnspan=2)

    def calculate_linear_algorithm(self):
        """
        Выполняет расчет линейного алгоритма, получая данные из полей ввода
        и отображая результат в соответствующем виджете.
        """
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            z = int(self.entry_z.get())
            accuracy = int(self.entry_accuracy.get())
            result = linear_algorithm(x, y, z, accuracy)
            self.result_display.config(text=f"{result:.5f}")
        except ValueError:
            self.result_display.config(text="Invalid input")

    def calculate_piecewise_function(self):
        """
        Выполняет расчет разветвляющейся функции, получая данные из полей ввода
        и отображая результат в соответствующем виджете.
        """
        try:
            x = float(self.entry_x2.get())
            y = float(self.entry_y2.get())
            selected_func = self.func_combobox.get()
            
            func_dict = {
                "cot": sp.cot,
                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,
            }
            
            f_func = func_dict[selected_func]
            result = branching_algorithm(x, y, f_func)
            self.result_display2.config(text=f"{result:.5f}")
        except ValueError:
            self.result_display2.config(text="Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
