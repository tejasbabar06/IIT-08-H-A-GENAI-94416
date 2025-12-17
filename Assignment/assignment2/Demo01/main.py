import Day01.Demo01.calculator as calculator
from Day01.Demo01.calculator import multiply
import Day01.Demo01.gemotery as geo
import Day01.Demo01.greeting as greeting

greeting.greet("Om")

num1 = int(input("enter num1: "))
num2 = int(input("enter num2: "))

calculator.add(num1, num2)
multiply(num1, num2)

geo.calc_rect_area(num1, num2)
geo.calc_rect_peri(num1, num2)