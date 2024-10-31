from string import punctuation
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from Deep_layer.NLP_package.Interfaces import IGpt
import torch
import logging
DEVICE = torch.device('cpu')

class Gpt(IGpt.IGpt):

    @classmethod
    def generate(cls, text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
            tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
            model = GPT2LMHeadModel.from_pretrained(model_name_or_path).to(DEVICE)
            input_ids = tokenizer.encode(text, return_tensors="pt").to(DEVICE)
            out = model.generate(input_ids, do_sample=False, max_length=100)
            tokens = text
            tokens = [token for token in tokens if token != ' '
                      and token.strip() not in punctuation]
            text = ' '.join(tokens).rstrip('\n')
            generated_text = list(map(tokenizer.decode, out))[0]
            logging.info('The gpt.generate is done')
            return generated_text.replace('\xa0', ' ').replace('\n', '').replace(text, '').replace('—', '')
        except Exception as e:
            logging.exception(str('The exception is in gpt.generate ' + e))
