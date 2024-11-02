from sympy import *
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import QuestionPreprocessing as tp
from Deep_layer.API_package.Interfaces import ICalculator


class SympyCalculator(ICalculator.ICalculator):

    __pr = tp.QuestionPreprocessing()

    @classmethod
    def deravative(cls, inptmes, dx):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            inp = cls.__pr.preprocess_text(dx)
            x = Symbol(inp[0])
            y = sympify(str(inptmes))
            yprime = y.diff(x)
            output = str(yprime).replace('**', '^')
            logging.info('The sympyCalculator.deravative is done')
            return output
        except Exception as e:
            logging.exception(str('The exception in sympycalculator.deravative ' + str(e)))

    @classmethod
    def integrate(cls, inptmes, dx):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            inp = cls.__pr.preprocess_text(dx)
            x = Symbol(inp[0])
            y = sympify(str(inptmes))
            yprime = y.integrate(x)
            output = str(yprime).replace('**', '^')
            logging.info('The sympycalculator.integrate is done')
            return output
        except Exception as e:
            logging.exception(str('The exception in sympycalculator.integrate ' + str(e)))
