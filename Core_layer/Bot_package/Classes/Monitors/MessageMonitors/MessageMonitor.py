import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IMonitor
from Core_layer.Answer_package.Classes import GptAnswer
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing


class MessageMonitor(IMonitor.IMonitor):
    """
    It is class for messaging
    """
    _pr = CommonPreprocessing.CommonPreprocessing()
    _dbc = DB_Communication.DB_Communication()
    _gpta = GptAnswer.GptAnswer()

    @classmethod
    def __decision(cls, text_message, emotion, commands):
        # call gpt to get an answer and check commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            outlist = []
            # check if the message contains a command
            if (cls._dbc.checkcommands(text_message)):
                # analyze the command and add the result to the output list
                outlist.append(commands.analyse(text_message))
                return outlist
            # get a response from gpt
            res = cls._gpta.answer(text_message)
            outlist.append(res)
            # append the emotion to the output list
            outlist.append('' + emotion)
            # log successful completion of the process
            logging.info('The messagemonitor.__decision process has completed successfully')
            return outlist
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in messagemonitor.__decision: ' + str(e))

    @classmethod
    def _neurodesc(cls, text, text_message, command):
        # calling the decision with emotion
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # initialize an empty emotion variable
            emotion = ''
            # log successful execution of the method
            logging.info('The messagemonitor._neurodesc process has completed successfully')
            # call the __decision method with the provided parameters
            return cls.__decision(text_message,
                                emotion,
                                command)
        except Exception as e:
            # log the exception if an error occurs
            logging.exception('The exception occurred in messagemonitor._neurodesc: ' + str(e))

    @classmethod
    def check(cls, text_message):
        # check of commands
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # check if the given text_message matches any command in the database
            if (cls._dbc.checkcommands(text_message)):
                logging.info('The messagemonitor.check process has completed successfully')
                return True
            else:
                logging.info('The messagemonitor.check process has completed successfully')
                return False
        except Exception as e:
            # log the exception if an error occurs during execution
            logging.exception('The exception occurred in messagemonitor.check: ' + str(e))

    @classmethod
    def monitor(cls, message, command, pltype):
        # main monitor for calculating messages
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            text = []
            # determine the message content based on the platform type
            if(pltype == 'discord'):
                lowertext = message.content.lower()
            elif (pltype=='telegram'):
                lowertext = message.text.lower()
            else:
                lowertext = message.lower()
            # insert the processed text into the database
            cls._dbc.insert_to(lowertext)
            outstr = ''
            # check if the message contains specific keywords
            if (lowertext.count('миса') > 0
                or lowertext.lower().count('misa')
                or lowertext.count('миша') > 0
                or lowertext.count('misha') > 0
                or lowertext.count('миса,')>0
                or lowertext.count('иса')>0):
                # perform text replacements (currently empty replacements)
                lowertext = (lowertext.replace('миса ', '')
                            .replace('misa ', '')
                            .replace('миса,', '')
                            .replace('misa,', '')
                            .replace('миша', '')
                            .replace('misha', '')
                            .replace('иса', ''))
                # add processed text to the list
                text.append(lowertext)
                # process the text using a neural network function
                outlist = cls._neurodesc(text, lowertext, command)
                # if the function returns a result, format it into a string
                if (outlist != None):
                    for outmes in outlist:
                        outstr += str(outmes)
                # log successful completion of the process
                logging.info('The messagemonitor.monitor process has completed successfully')
                return outstr.capitalize()
            else:
                # log successful completion even if no keywords were found
                logging.info('The messagemonitor.monitor process has completed successfully')
                return outstr.capitalize()
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in messagemonitor.monitor: ' + str(e))
