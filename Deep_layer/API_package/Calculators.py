from Deep_layer import API_package


class ICalculator(API_package.ABC):

    @API_package.abstractmethod
    def deravative(cls, boto, message, inptmes, dx):
        pass

    @API_package.abstractmethod
    def integrate(cls, boto, message, inptmes, dx):
        pass
    
class SympyCalculator(ICalculator):

    __pr = API_package.tp.QuestionPreprocessing()

    @classmethod
    def deravative(cls,  inptmes, dx):

        try:
            inp = cls.__pr.preprocess_text(dx)
            x = API_package.Symbol(inp[0])
            y = API_package.sympify(str(inptmes))
            yprime = y.diff(x)
            output = str(yprime).replace('**','^')
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
            output = str(yprime).replace('**','^')
            return output
        except:
            print('The exception in SympyCalculator.integrate')