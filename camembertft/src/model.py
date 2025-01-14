import config
import torch
import transformers
import torch.nn as nn

def loss_fn(output, target, mask, num_labels):
    lfn = nn.CrossEntropyLoss()
    active_loss = mask.view(-1) == 1
    active_logits = output.view(-1, num_labels)
    active_labels = torch.where(
        active_loss,
        target.view(-1),
        torch.tensor(lfn.ignore_index).type_as(target)
    )
    loss = lfn(active_logits, active_labels)
    return loss


class EntityModel(nn.Module):
    def __init__(self, num_tag):
        super(EntityModel, self).__init__()
        self.num_tag = num_tag
        self.bert = transformers.CamembertModel.from_pretrained(config.BACKBONE,return_dict=False)
        self.bert_drop_1 = nn.Dropout(0.3)
        self.bert_drop_2 = nn.Dropout(0.3)
        self.linear_drop = nn.Dropout(0.1)
        self.out_tag_1 = nn.Linear(768, 64)
        self.out_tag_2 = nn.Linear(64, self.num_tag)
    
    def forward(self, ids, mask, token_type_ids, target_tag):
        o1, _ = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)

        bo_tag = self.bert_drop_1(o1)

        tag1 = self.out_tag_1(bo_tag)

        tag1 = self.linear_drop(tag1)

        tag = self.out_tag_2(tag1)

        loss_tag = loss_fn(tag, target_tag, mask, self.num_tag)

        loss = loss_tag

        return tag,  loss