import logging
from typing import Dict, Text
import numpy as np
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm

from scripts.models.nn_model import NetworkModel
from scripts.networks.network_class import MyNetwork

logger = logging.getLogger()


class Pretrained_Bert_Model(NetworkModel):

    def __init__(self,
                 network: MyNetwork,
                 dataloader: Dict[Text, DataLoader],
                 loss,
                 optimizer: Optimizer,
                 save_dir: Text):
        super().__init__(network, dataloader, loss, optimizer, save_dir)
        self.name = 'Pretrained_bert_model'
        self.model_path = self._save_path(save_dir)

    def train(self,
              epochs: int,
              patience: int = None,
              min_delta: float = 0):
        super().train(epochs, patience, min_delta)

    def _train_one_epoch(self):
        super()._train_one_epoch()
        losses = []

        for data in tqdm(self.dataloader['train'], desc='Training   '):
            input_ids = data["input_ids"]
            attention_mask = data["attention_mask"]
            targets = data["targets"]

            out = self.network.forward(input_ids, attention_mask)
            out = out.squeeze()

            loss = self.loss(out, targets.float())
            loss.backward()
            self.optimizer.step()

            losses.append(loss.item())

        return np.mean(losses)

    def _validate_one_epoch(self):
        super()._validate_one_epoch()
        losses = []

        for x, y in tqdm(self.dataloader['valid'], desc='Validation '):

            out = self.network.forward(x)

            loss = self.loss(out, y.long())

            losses.append(loss.item())

        return np.mean(losses)

    def save(self):
        super().save()
        logger.info(f'Saving {self.name} at {self.model_path}')
