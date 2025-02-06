import logging
from sympy import *
from Deep_layer.API_package.Interfaces import ICalculator
from Deep_layer.NLP_package.Classes.TextPreprocessers import QuestionPreprocessing as tp


class SympyCalculator(ICalculator.ICalculator):
    """
    It is calculator class
    """
    __pr = tp.QuestionPreprocessing()

    @classmethod
    def deravative(cls, inptmes, dx):
        # finding derevatives of  mathematical functions
        # setting up logging to record events
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # preprocessing the input variable name
            inp = cls.__pr.preprocess_text(dx)
            # defining the symbolic variable for integration
            x = Symbol(inp[0])
            # converting the input mathematical expression to a symbolic form
            y = sympify(str(inptmes))
            # computing the deravative of the function with respect to x
            yprime = y.diff(x)
            # formatting the output to use '^' instead of '**' for exponentiation
            output = str(yprime).replace('**', '^')
            # logging successful completion of the integration process
            logging.info('The sympyCalculator.deravative is done')
            return output
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception in sympycalculator.deravative ' + str(e)))

    @classmethod
    def integrate(cls, inptmes, dx):
        # finding integrals of  mathematical functions
        # setting up logging to record events
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # preprocessing the input variable name
            inp = cls.__pr.preprocess_text(dx)
            # defining the symbolic variable for integration
            x = Symbol(inp[0])
            # converting the input mathematical expression to a symbolic form
            y = sympify(str(inptmes))
            # computing the integral of the function with respect to x
            yprime = y.integrate(x)
            # formatting the output to use '^' instead of '**' for exponentiation
            output = str(yprime).replace('**', '^')
            # logging successful completion of the integration process
            logging.info('The sympycalculator.integrate is done')
            return output
        except Exception as e:
            # logging any exceptions that occur during execution
            logging.exception(str('The exception in sympycalculator.integrate ' + str(e)))

