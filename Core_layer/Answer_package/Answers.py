from Core_layer import Answer_package


class IAnswer(Answer_package.ABC):

    @Answer_package.abstractmethod
    def answer(self):
        pass

class RandomAnswer(IAnswer):
    __inpt = Answer_package.DB_Bridge.DB_Communication.get_data('SELECT * FROM answer_sets.hianswer')
    __data = __inpt
    __df = []

    @classmethod
    def answer(self):
        try:
            for i in range(0, len(self.__data['text'])-1):
                if(self.__data['agenda'][i] == 'Приветствие'):
                    self.__df.append(self.__data['text'][i])
            outmapa = {0: [self.__df[Answer_package.random.randint(0, len(self.__df))]]}
                
            return (outmapa[0])
        except:
            return 'The exception in RandomAnswer.answer'