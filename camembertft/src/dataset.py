import config
import torch

from typing import List, Sequence, Union, Dict
from torch import Tensor


class CustomDataset():

    def __init__(self, texts : Sequence[Union[str, List[str]]], tags: Sequence[List[str]]):

        self.texts = texts

        self.tags = tags

    def __len__(self)-> int:

        return len(self.texts)
    
    def __getitem__(self, idx: int) -> Dict[str, Tensor]:

        chunktag = self.texts[idx]
       
        tags = self.tags[idx]

        ids = []

        target_tag = []

        
        for i, token in enumerate(chunktag):
            
            inputs = config.TOKENIZER(
                token,
                truncation=True,
                is_split_into_words= True,
            )

            ids_ = inputs["input_ids"][1:-1]

            tag_ = [tags[i][k] for k in inputs.word_ids() if k!=None ]

            ids.extend(ids_)

            target_tag.extend(tag_)


        ids = ids[: config.MAX_LEN -2]

        target_tag = target_tag[: config.MAX_LEN -2]

        
        ids = [config.TOKENIZER.cls_token_id] + ids + [config.TOKENIZER.sep_token_id]


        target_tag = [config.LOSS_IGNORE_INDEX] + target_tag + [config.LOSS_IGNORE_INDEX]

        mask = [1]*len(ids)

        token_type_ids = [0]*len(ids)

        padding_len = config.MAX_LEN - len(ids)

        ids = ids + ([0] * padding_len)

        mask = mask + ([0] * padding_len)

        token_type_ids = token_type_ids + ([0] * padding_len)

        target_tag = target_tag + ([config.LOSS_IGNORE_INDEX] * padding_len)
        


        return {"ids": torch.tensor(ids , dtype=torch.long),
                "mask": torch.tensor(mask , dtype=torch.long),
                "token_type_ids": torch.tensor(token_type_ids , dtype=torch.long),
                "target_tag":torch.tensor(target_tag , dtype=torch.long), 
            }

    