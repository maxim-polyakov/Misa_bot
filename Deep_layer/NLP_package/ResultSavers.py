from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class ISaver(ABC):

    @abstractmethod
    def saveRes(cls, history, path):
        pass

class ResultSaver(ISaver):
    @classmethod
    def saveRes(cls, history, path, accuracy):
        s, (at, al) = plt.subplots(2, 1)
        at.plot(history.history[accuracy], c='b')
        at.plot(history.history['val_' + accuracy], c='r')
        at.set_title('model accuracy')
        at.set_ylabel('accuracy')
        at.set_xlabel('epoch')
        at.legend(['LSTM_train', 'LSTM_val'], loc='upper left')

        al.plot(history.history['loss'], c='m')
        al.plot(history.history['val_loss'], c='c')
        al.set_title('model loss')
        al.set_ylabel('loss')
        al.set_xlabel('epoch')
        al.legend(['train', 'val'], loc='upper left')

        fig = al.get_figure()
        fig.savefig('resultstraining_multy.png')
        fig.savefig(path)