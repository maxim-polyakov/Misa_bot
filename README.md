![plot](https://github.com/maxim-polyakov/Misa_bot/blob/train_dev_branch/House.jpg)

# Misa_bot

Misa_bot is a three-layer architecture python application.

  ## Front layer

  Front layer contains discord and telegram bots to collect data from an environment platforms:
  
  The functional paradigm is realeased in a Front layert. Front layer doesnt comprise entityes, it comprises only functions for implementation commands.
  
    1) telegram
          
    2) discord
    
    
  ## Core layer

  Core layer comprises a few packages:
  
    1) Answer_package - this package is created for generate answer for input questions. 
    
       Answer_package contains the next entityes:
       
          a) IAnswer
        
    2) Bot_package - this package is created to implement the main bot's logic.
    
       Bot_package contains the next entityes:
       
          a) ITrain
          b) ICleaner
          c) IMonitor
          d) IAnalyzer
        
        
    3) Command_package - this package is created to implement the command's action logic.
    
       Command package contains the next entityes:
       
         a) IAction
         b) ICommandAnalyzer
    
    4) Test_package - this package is created as for testing all application's entities. 
       
       Test package contains the next entityes:
         a) ITestCase
         b) ITestMonitor

  ## Deep layer

  Deep layer contains a few packages:
  
    1) API_package - this package is created to use API's like googletrans or wikipedia.
    
       API_package comprises the next entityes:
       
          a) ICalculator
          b) IFinder
          c) ITranslator
      
    2) DB_package - this package is created for using several databases.
    
       DB_package contains the next entityes:
       
          a) IDB_Communication
            
    3) NLP_package - this package is created to train NLP models and to use models as predictors.
    
       NLP_package contains the next entityes:
       
          a) IDataShower
          b) IGpt
          c) IModel
          d) IPredictor
          e) ISaver
          f) IPreprocessing
          g) ITokenizer

  and 2 folders
  
    1) models
       models contains the text types of models
          a) LSTM - the recurent model with a memory https://medium.com/mlearning-ai/the-classification-of-text-messages-using-lstm-bi-lstm-and-gru-f79b207f90ad
          
    2) tokenizers
          a) The tokenizer for this LSTM model
          
Also architecture contains SistersMemory - general database which contains samples for models' trainings for all chat_bots which hosted in       https://console.neon.tech/.
 
