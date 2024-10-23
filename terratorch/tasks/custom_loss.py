import torch
from torch import nn 

class MaskedRMSELoss:

    def __init__(self, norm_pix_loss:bool=True):
        self.norm_pix_loss = norm_pix_loss

    @staticmethod
    def _avoid_null_mask(mask):
        if not torch.all(mask):
            return torch.ones_like(mask)
        else:
            return mask

    def __call__(self, model_output, target):

        prediction = model_output.output 
        mask = self._avoid_null_mask(model_output.mask)
    
        if self.norm_pix_loss:
            mean = target.mean(dim=-1, keepdim=True)
            var = target.var(dim=-1, keepdim=True)
            target = (target - mean) / (var + 1.0e-6) ** 0.5

        loss = (prediction - target) ** 2
        loss = loss.mean(dim=-1)  # [N, L], mean loss per patch

        loss = (loss * mask).sum() / mask.sum()  # mean loss on removed patches

        return loss    
