import config
import torch

from typing import List, Sequence, Union, Dict
from torch import Tensor

from config import Config

config = Config()

class CustomDataset(torch.utils.data.Dataset):

    def __init__(self, texts : Sequence[Union[str, List[str]]], tags: Sequence[List[str]]):

        # textes representes a sequence phrase [["Paris", "is", "a", "beautiful", "country"], ["I", "love", "American", "country"]]
        self.texts = texts

        self.tags = tags

    def __len__(self)-> int:

        return len(self.texts)
    
    def __getitem__(self, index: int) -> Dict[str, Tensor]:
        """Get item at index"""
        # text represents a sequence of word ["Paris", "is", "a", "beautiful", "country"]
        text = self.texts[index]
        tags = self.tags[index]

        ids = []
        target_tag = []

        for idx, token in enumerate(text):
            # camemBERT tokenizer takes a token like Paris and return {'input_ids': [5, 300, 6], 'attention_mask': [1, 1, 1]}
            inputs = config.TOKENIZER(
                token,
                truncation=True,
                max_length=config.MAX_LEN,
            )
            # remove special tokens <s> and </s>
            ids_ = inputs["input_ids"][1:-1]

            input_len = len(ids_)

            ids.extend(ids_)

            if config.PROPAGATE_LABEL_TO_WORD_PIECES:
                target_tag.extend([tags[idx]] * input_len)
            else:
                target_tag.append(tags[idx])
                target_tag.extend([config.LOSS_IGNORE_INDEX] * (input_len - 1))

        # Ids contains ids of word pieces, which the lenght can be more than MAX_LEN
        # In order to have save lenght for each input we select only MAX_LEN - 2 ids of word pieces
        ids = ids[: config.MAX_LEN - 2]
        target_tag = target_tag[: config.MAX_LEN - 2]

        # Reconstruct specials tokens at start and end
        ids = [config.TOKENIZER.cls_token_id] + ids + [config.TOKENIZER.sep_token_id]
        target_tag = [config.LOSS_IGNORE_INDEX] + target_tag + [config.LOSS_IGNORE_INDEX]
        mask = [1] * len(ids)
        token_type_ids = [0] * len(ids)
        
        # Padding
        padding_len = config.MAX_LEN - len(ids)
        ids = ids + ([config.TOKENIZER.pad_token_id] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_ids = token_type_ids + ([0] * padding_len)
        target_tag = target_tag + ([config.LOSS_IGNORE_INDEX] * padding_len)

        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "target_tags": torch.tensor(target_tag, dtype=torch.long),
        }