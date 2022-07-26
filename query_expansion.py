import transformers
from transformers import BertTokenizer, BertForMaskedLM
import numpy as np
import torch


class QueryExpander:
    def __init__(self):
        self.model = BertForMaskedLM.from_pretrained("/Users/kian/Desktop/MIR/MIR-Project/nextWordModel/model")
        self.tokenizer = BertTokenizer.from_pretrained("/Users/kian/Desktop/MIR/MIR-Project/nextWordModel/tokenizer")
    
    def get_next_word(self, query):
        
        m_query = query.strip() + " [MASK]."
        print(m_query)
        inputs = tokenizer(m_query, return_tensors="pt")

        with torch.no_grad():
            logits = model(**inputs).logits
        
        mask_token_index = (inputs.input_ids == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]
        topk_ind = torch.topk(logits[0, mask_token_index], k=3).indices
        words = tokenizer.decode(topk_ind[0]).split()
        return [query + " " + word for word in words]
