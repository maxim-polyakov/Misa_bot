import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Core_layer.Bot_package.Classes.Weather import Weather
from Core_layer.Bot_package.Classes.Finder import GoogleFinder
from Core_layer.Bot_package.Classes.Finder import WikiFinder
from Core_layer.Command_package.Interfaces import IAction
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing, Preprocessing


class CommandAction(IAction.IAction):
    """
    It is class for comand's actions
    """
    boto = None
    message = None
    message_text = None

    __pred = Preprocessing.Preprocessing()
    __pr = CommonPreprocessing.CommonPreprocessing()

    def __init__(self, message, message_text):
        CommandAction.message = message
        CommandAction.message_text = message_text

    @classmethod
    def first(cls):
        # attack
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            if cls.message_text.count('фас') > 0:
                # preprocess the message text
                Inputstr = cls.__pred.preprocess_text(cls.message_text)
                # remove specific attack-related words from the text
                Inputstr = Inputstr.replace('атакуй ', '').replace('пиздани ', '').replace('фас ', '')
                # split the processed text into an array of words
                Inputarr = Inputstr.split(' ')
                # set a command flag indicating an action
                cls.command_flag = 1
                # remove the first word from the input string
                Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
                # log successful completion of the process
                logging.info('The commandaction.first process is completed successfully')
                # return the modified string with an appended phrase
                return Inputstr + ' - пидор.'
        except Exception as e:
            logging.exception('The exception occurred in aaction.first: ' + str(e))

    @classmethod
    def second(cls):
        # translate
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception('The exception occurred in commandaction.second: ' + str(e))

    @classmethod
    def third(cls):
        # find
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains "найди" but not "найдись"
            if cls.message_text.count('найди') > 0 and cls.message_text.count('найдись') == 0:
                # remove unnecessary spaces and "найди" from the message
                message_text = (cls.message_text.strip(' ')
                                .replace('найди ', ''))
                # check if the message is related to mathematical operations
                if (message_text.count('производную') > 0) or (message_text.count('интеграл') > 0):
                    logging.info('The commandaction.find process has completed successfully')
                    return ''
                else:
                    # check if the message is related to wikipedia search
                    if (message_text.count('в википедии') > 0):
                        message_text = (message_text.strip(' ')
                                        .replace('в википедии ', ''))
                        try:
                            # perform a wikipedia search
                            apif = WikiFinder.WikiFinder(cls.__pr.preprocess_text(message_text))
                            finded_list = apif.find()
                            logging.info('The commandaction.find process has completed successfully')
                            return str(finded_list)
                        except Exception as e:
                            # log any exceptions that occur during the wikipedia
                            logging.exception('The exception occurred in commandaction.third: ' + str(e))
                            return 'Не нашла'
                    else:
                        try:
                            # perform a google search
                            gpif = GoogleFinder.GoogleFinder(message_text)
                            outstr = gpif.find()
                            logging.info('The commandaction.third process has completed successfully')
                            return outstr
                        except Exception as e:
                            # log any exceptions that occur during the google search
                            logging.exception('The exception occurred in commandaction.third: ' + str(e))
                            return 'Не нашла'
        except Exception as e:
            # log any general exceptions that occur in the method
            logging.exception('The exception occurred in commandaction.third: ' + str(e))

    @classmethod
    def fourth(cls):
        # say
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains the word "скажи" (which means "say" in russian)
            if cls.message_text.lower().count('#скажи') > 0:
                # remove "скажи " from the message text
                message_text = cls.message_text.replace('#скажи ', '').replace(' #скажи', '')
                # log successful execution of the method
                logging.info('The commandaction.fourth process has completed successfully')
                # return the modified message text
                return message_text
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception in commandaction.fourth ' + str(e))

    @classmethod
    def fifth(cls):
        # weather
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains the word "погода" (weather)
            if cls.message_text.count('#погода') > 0:
                # remove the word "погода" from the message to extract the location
                message = cls.message_text.replace('#погода ','')
                # get weather information for the specified location
                w = Weather.Weather(message)
                out = w.predict()
                # log successful execution
                logging.info('The commandaction.fifth process has completed successfully')
                return out
        except Exception as e:
            # log any exceptions that occur
            logging.exception('The exception occurred in commandaction.fifth: ' + str(e))
            return 'Проблемы с сервисом'

    @classmethod
    def sixth(cls):
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            pass
        except Exception as e:
            logging.exception(str('The exception occurred in commandaction.sixth: ' + str(e)))

    @classmethod
    def seventh(cls):
        # clean
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains the word "почисти" but not "почистись"
            if cls.message_text.count('почисти') > 0 and cls.message_text.count('почистись') == 0:
                # remove "почисти " from the message text
                message_text = (cls.message_text.replace('почисти ', ''))
                # create an instance of the common preprocessing class
                pr = CommonPreprocessing.CommonPreprocessing()
                # log successful execution
                logging.info('The commandaction.seventh process has completed successfully')
                # preprocess the cleaned message text and return the result
                return pr.preprocess_text(message_text)
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception in commandaction.seventh ' + str(e)))


    @classmethod
    def eighth(cls):
        pass

    @classmethod
    def nineth(cls):
        # calculate
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
           pass
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandaction.nineth: ' + str(e))

    @classmethod
    def tenth(cls):
        # clean
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the message contains the word "очисти" but not "очисться"
            if cls.message_text.count('#очисти') > 0 and cls.message_text.count('#очисться') == 0:
                # remove "очисти " from the message text
                message_text = (cls.message_text.replace('#почисти ', '')
                                .replace('#очисти', ''))
                # create an instance of the common preprocessing class
                pr = CommonPreprocessing.CommonPreprocessing()
                # log successful execution of the method
                logging.info('The commandaction.seventh process has completed successfully')
                # preprocess the cleaned message text and return the result
                return pr.preprocess_text(message_text)
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception(str('The exception occurred in commandaction.seventh: ' + str(e)))
