from transformers import ElectraTokenizer
from transformers import GPT2Tokenizer
## model choices
# 'EleutherAI/gpt-neo-125M'
## BertTokenizer
## ElectraTokenizer
def tokenizeElectra(text):
    tokenizer = ElectraTokenizer.from_pretrained('google/electra-small-discriminator')
    tokens = tokenizer.tokenize("Find me cheap sushi in SF")
    return tokens
def detokenizeElectra(tokens):
    tokenizer = ElectraTokenizer.from_pretrained('google/electra-small-discriminator')
    text = tokenizer.convert_tokens_to_string(tokens)
    return text

def tokenize_text(text):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    return tokenizer.encode(text, return_tensors="pt")

def detokenize_tokens(tokens):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    return tokenizer.decode(tokens)
