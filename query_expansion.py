import torch
from transformers import BertTokenizer, BertForMaskedLM


class QueryExpander:
    def __init__(self):
        ##
        ## You can download the folder "nextWordModel" from https://drive.google.com/drive/folders/1ny3-cA_MQz6wPLmhFi3GVxusoipkNQjX?usp=sharing
        ##
        self.model = BertForMaskedLM.from_pretrained("./nextWordModel/model")
        self.tokenizer = BertTokenizer.from_pretrained("./nextWordModel/tokenizer")

    def get_query_suggestions(self, query):
        m_query = query.strip() + " [MASK]."
        print(m_query)
        inputs = self.tokenizer(m_query, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits

        mask_token_index = (inputs.input_ids == self.tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]
        topk_ind = torch.topk(logits[0, mask_token_index], k=3).indices
        words = self.tokenizer.decode(topk_ind[0]).split()
        return [query + " " + word for word in words]
