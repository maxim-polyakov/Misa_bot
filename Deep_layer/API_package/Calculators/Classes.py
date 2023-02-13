from Deep_layer import API_package
from sympy import *
from Deep_layer.NLP_package import TextPreprocessers as tp
from Deep_layer.API_package.Calculators import Interfaces

class SympyCalculator(Interfaces.ICalculator):
    __pr = tp.QuestionPreprocessing()

    @classmethod
    def deravative(cls, inptmes, dx):
        try:
            inp = cls.__pr.preprocess_text(dx)
            x = Symbol(inp[0])
            y = sympify(str(inptmes))
            yprime = y.diff(x)
            output = str(yprime).replace('**', '^')
            return output
        except:
            print('The exception in SympyCalculator.deravative')

    @classmethod
    def integrate(cls, inptmes, dx):
        try:
            inp = cls.__pr.preprocess_text(dx)
            x = API_package.Symbol(inp[0])
            y = API_package.sympify(str(inptmes))
            yprime = y.integrate(x)
            output = str(yprime).replace('**', '^')
            return output
        except:
            print('The exception in SympyCalculator.integrate')