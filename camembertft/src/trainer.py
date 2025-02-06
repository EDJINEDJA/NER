import torch
from tqdm import tqdm


def train_fn(data_loader, model, optimizer, device, scheduler):
    """
    Training function for one epoch.

    Args:
        data_loader (torch.utils.data.DataLoader): DataLoader for the training dataset.
        model (torch.nn.Module): The model to be trained.
        optimizer (torch.optim.Optimizer): Optimizer for updating model parameters.
        device (torch.device): Device to run the training on (e.g., "cuda" or "cpu").
        scheduler (torch.optim.lr_scheduler._LRScheduler): Learning rate scheduler.

    Returns:
        float: Average training loss for the epoch.
    """
    model.train()  # Set the model to training mode
    total_loss = 0  # Accumulate the total loss for the epoch

    # Iterate over the data loader with a progress bar
    for batch in tqdm(data_loader, total=len(data_loader)):
        # Move all batch data to the specified device
        for key, value in batch.items():
            batch[key] = value.to(device)

        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass: compute model predictions and loss
        _, loss = model(**batch)

        # Backward pass: compute gradients
        loss.backward()

        # Update model parameters
        optimizer.step()

        # Update learning rate
        scheduler.step()

        # Accumulate the loss
        total_loss += loss.item()

    # Return the average loss for the epoch
    return total_loss / len(data_loader)


def eval_fn(data_loader, model, device):
    """
    Evaluation function for one epoch.

    Args:
        data_loader (torch.utils.data.DataLoader): DataLoader for the evaluation dataset.
        model (torch.nn.Module): The model to be evaluated.
        device (torch.device): Device to run the evaluation on (e.g., "cuda" or "cpu").

    Returns:
        float: Average evaluation loss for the epoch.
    """
    model.eval()  # Set the model to evaluation mode
    total_loss = 0  # Accumulate the total loss for the epoch

    # Disable gradient computation for evaluation
    with torch.no_grad():
        # Iterate over the data loader with a progress bar
        for batch in tqdm(data_loader, total=len(data_loader)):
            # Move all batch data to the specified device
            for key, value in batch.items():
                batch[key] = value.to(device)

            # Forward pass: compute model predictions and loss
            _, loss = model(**batch)

            # Accumulate the loss
            total_loss += loss.item()

    # Return the average loss for the epoch
    return total_loss / len(data_loader)