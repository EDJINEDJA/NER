import torch
import torch.nn as nn
from transformers import CamembertModel
from config import Config

config = Config()

def loss_fn(output, target, attention_mask, num_labels):
    """
    Compute the CrossEntropyLoss for active tokens only (ignoring padding tokens).

    Args:
        output (torch.Tensor): Model predictions of shape (batch_size, sequence_length, num_labels).
        target (torch.Tensor): Ground truth labels of shape (batch_size, sequence_length).
        attention_mask (torch.Tensor): Attention mask indicating active tokens (1 for active, 0 for padding).
        num_labels (int): Number of unique labels (e.g., number of NER tags).

    Returns:
        torch.Tensor: Computed loss value.
    """
    loss_function = nn.CrossEntropyLoss()

    # Flatten the tensors to compute loss over all tokens
    active_loss = attention_mask.view(-1) == 1  # Identify active tokens (not padding)
    active_logits = output.view(-1, num_labels)  # Flatten predictions
    active_labels = torch.where(
        active_loss,
        target.view(-1),  # Use ground truth labels for active tokens
        torch.tensor(loss_function.ignore_index).type_as(target)  # Ignore padding tokens
    )

    # Compute the loss
    loss = loss_function(active_logits, active_labels)
    return loss


class NERModel(nn.Module):
    """
    A Named Entity Recognition (NER) model using CamemBERT as the backbone.

    Args:
        num_tag (int): Number of unique NER tags.
    """
    def __init__(self, num_tag):
        super(NERModel, self).__init__()
        self.num_tag = num_tag

        # Load pre-trained CamemBERT model
        self.bert = CamembertModel.from_pretrained(config.BACKBONE, return_dict=False)

        # Dropout layers to prevent overfitting
        self.bert_drop_1 = nn.Dropout(0.2)
        self.bert_drop_2 = nn.Dropout(0.3)
        self.linear_drop = nn.Dropout(0.2)

        # Linear layers for tag prediction
        self.out_tag_1 = nn.Linear(768, 64)  # Reduce dimensionality from 768 to 64
        self.out_tag_2 = nn.Linear(64, self.num_tag)  # Final output layer for NER tags

    def forward(self, input_ids, attention_mask, token_type_ids, target_tags):
        """
        Forward pass of the model.

        Args:
            input_ids (torch.Tensor): Tokenized input IDs of shape (batch_size, sequence_length).
            attention_mask (torch.Tensor): Attention mask of shape (batch_size, sequence_length).
            token_type_ids (torch.Tensor): Token type IDs of shape (batch_size, sequence_length).
            target_tags (torch.Tensor): Ground truth NER tags of shape (batch_size, sequence_length).

        Returns:
            tuple: A tuple containing:
                - tag (torch.Tensor): Predicted NER tags of shape (batch_size, sequence_length, num_tag).
                - loss (torch.Tensor): Computed loss value.
        """
        # Pass inputs through CamemBERT
        sequence_output, _ = self.bert(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)

        # Apply dropout to the BERT output
        sequence_output = self.bert_drop_1(sequence_output)

        # First linear layer for tag prediction
        tag_hidden = self.out_tag_1(sequence_output)
        tag_hidden = self.linear_drop(tag_hidden)

        # Final linear layer for tag prediction
        tag_logits = self.out_tag_2(tag_hidden)

        # Compute the loss
        loss = loss_fn(tag_logits, target_tags, attention_mask, self.num_tag)

        return tag_logits, loss