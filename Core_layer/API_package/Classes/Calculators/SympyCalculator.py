from sympy import *
from Deep_layer.NLP_package.Classes.TextPreprocessers import QuestionPreprocessing as tp
from Core_layer.API_package.Interfaces import ICalculator

class SympyCalculator(ICalculator.ICalculator):

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
            x = Symbol(inp[0])
            y = sympify(str(inptmes))
            yprime = y.integrate(x)
            output = str(yprime).replace('**', '^')
            return output
        except:
            print('The exception in SympyCalculator.integrate')