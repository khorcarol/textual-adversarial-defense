import torch
from scipy.optimize import differential_evolution
import numpy as np
def natural(x: float) -> int:
    """Rounds float to the nearest natural number (positive int)"""
    return max(0, round(float(x)))

def integer(x: float) -> int:
    """Rounds float to the nearest int"""
    return round(float(x))

ZWSP = chr(0x200B)
# Zero width joiner
ZWJ = chr(0x200D)
# Zero width non-joiner
ZWNJ = chr(0x200C)

class InvisibleCharacterObjective():
    def __init__(self, orig_S, max_perturbs, invisible_chrs, **kwargs):
        super().__init__(**kwargs)  
        self.orig_S = orig_S
        self.max_perturbs = max_perturbs
        self.invisible_chrs = invisible_chrs
        
    def bounds(self):
        return [(0,len(self.invisible_chrs)-1), (-1, len(self.orig_S)-1)] * self.max_perturbs

    def candidate(self, perturbations) -> str:
        candidate = [char for char in self.orig_S]
        for i in range(0, len(perturbations), 2):
            inp_index = integer(perturbations[i+1])
            if inp_index >= 0:
                inv_char = self.invisible_chrs[natural(perturbations[i])]
                candidate = candidate[:inp_index] + [inv_char] + candidate[inp_index:]
        return ''.join(candidate)

        
class MnliObjective():
    
    def __init__(self, model_wrapper, args, premise, orig_label, **kwargs):
            super().__init__(**kwargs) 
            self.model = model_wrapper
            self.args = args
            self.premise = premise
            self.orig_label = orig_label
        
    def objective(self):
        def _objective(perturbations) -> float:
            candidate: str = self.candidate(perturbations)
            if self.premise is not None:
                tokens = self.model.tokenizer([self.premise], [candidate], padding='longest', return_tensors='pt', add_special_tokens=True, truncation=True)
            else:
                tokens = self.model.tokenizer([candidate], padding='longest', return_tensors='pt', add_special_tokens=True, truncation=True)
            predict = self.model.model(input_ids = tokens['input_ids'].to(self.args.device), attention_mask = tokens['attention_mask'].to(self.args.device)).logits
            
            if predict.argmax() != self.orig_label:
                return -np.inf
            else:
                return predict[0][self.orig_label].item()
        return _objective

    def differential_evolution(self, verbose=False, maxiter=3, popsize=32, polish=False):
        result = differential_evolution(self.objective(), self.bounds(),
                                    disp=verbose, maxiter=maxiter,
                                    popsize=popsize, polish=polish)
        candidate = self.candidate(result.x)
        if self.premise is not None:
            tokens = self.model.tokenizer([self.premise], [candidate], padding='longest', return_tensors='pt', add_special_tokens=True, truncation=True)
        else:
            tokens = self.model.tokenizer([candidate], padding='longest', return_tensors='pt', add_special_tokens=True, truncation=True)
        predict = self.model.model(input_ids = tokens['input_ids'].to(self.args.device), attention_mask = tokens['attention_mask'].to(self.args.device)).logits
        adv_label = torch.argmax(predict).item()
        return candidate, adv_label
        
        

class InvisibleCharacterMnliObjective(MnliObjective, InvisibleCharacterObjective):
    def __init__(self, model_wrapper, args, orig_S, premise, orig_label, max_perturbs, invisible_chrs =  [ZWJ,ZWSP,ZWNJ]):
        super().__init__(
            model_wrapper=model_wrapper,
            args = args,
            orig_S=orig_S,
            premise=premise,
            orig_label=orig_label,
            max_perturbs=max_perturbs,
            invisible_chrs=invisible_chrs
        )
    
    
class Boucher():

    def __init__(self, model_wrapper, args):
        self.model_wrapper = model_wrapper
        self.args = args
        if self.args.dataset in ["mnli", "qnli", "rte", "sst2", "agnews"]:
            self.objective_class = InvisibleCharacterMnliObjective
    

    def attack(self, orig_S, orig_label, premise=None, budget=10):
        with torch.no_grad():
            obj = self.objective_class(self.model_wrapper, self.args, orig_S, premise, orig_label.item(), budget)
            adv_S, adv_label = obj.differential_evolution()
        return adv_S, adv_label, budget
        
        # return adv_S, adv_label, number of perturbations