import myutils
import torch
import numpy as np
class Charmix:
    
    def __init__(self, model_wrapper, args):
        self.model_wrapper = model_wrapper
        self.args = args
        
        self.device = args.device
        
        if args.model == "textattack/roberta-base-SST-2":
            self.criterion = myutils.cw_loss_batched(reduction='none')
            
        self.V =  myutils.BIDI_CHARS+myutils.VARIATION_SELECTORS+myutils.TAG_CHARS+myutils.INVIS_CHAR+myutils.DEL_CHAR #Unicode indices
            
        
    def get_top_n_locations(self, orig_S, orig_label):
        SS = myutils.generate_all_sentences(orig_S, [ord(" ")],  range(0, 2*len(orig_S)+1, 2))
        T = self.model_wrapper.tokenizer(SS, padding="longest", return_tensors="pt", add_special_tokens=True, truncation=True)
        pred = self.model_wrapper.model(input_ids = T['input_ids'].to(self.device), attention_mask = T['attention_mask'].to(self.device)).logits
        loss = self.criterion(pred,orig_label.repeat(pred.shape[0]))
        
        idx = list(torch.topk(loss,min(self.args.n_positions,len(loss))).indices)
        positions = [2 * i for i in idx]
 
        return positions

    def attack_brute_force(self, S, label, subset_z, bs=1024):
        with torch.no_grad():
            SS = myutils.generate_all_sentences(S, self.V, subset_z)
            pred = []
            for i in range(len(SS)//bs+1):
                
                T = self.model_wrapper.tokenizer(SS[i*bs:min((i+1)*bs, len(SS))], padding = 'longest',return_tensors = 'pt', add_special_tokens = True, truncation = True)
                pred.append(self.model_wrapper.model(input_ids = T['input_ids'].to(self.device), attention_mask = T['attention_mask'].to(self.device)).logits)
            pred = torch.cat(pred, dim=0)
            loss = self.criterion(pred, label.repeat(pred.shape[0]))
            idx = torch.argmax(loss)
        return SS[idx], pred[idx], loss[idx]
    
    def attack_brute_force_random(self, S, label, bs=1):
        with torch.no_grad():
            SS = myutils.generate_all_sentences(S, self.V)
            B = np.random.choice(SS, min(bs, len(SS)), replace = False).tolist()

            T = self.model_wrapper.tokenizer(B, padding = 'longest',return_tensors = 'pt', add_special_tokens = True, truncation = True)
            pred = (self.model_wrapper.model(input_ids = T['input_ids'].to(self.device), attention_mask = T['attention_mask'].to(self.device)).logits)
            
            loss = self.criterion(pred, label.repeat(pred.shape[0]))
            idx = torch.argmax(loss)
        return SS[idx], pred[idx], loss[idx]
    
    def attack(self, orig_S, orig_label):
        with torch.no_grad(): 
            for n in range(self.args.n_positions):
                if self.args.attack_name == "charmer":
                    subset_z = self.get_top_n_locations(orig_S, orig_label)
                    s, pred, _ = self.attack_brute_force(orig_S, orig_label, subset_z)
                    
                elif self.args.attack_name == "positionrand":
                    s, pred, _ = self.attack_brute_force_random(orig_S, orig_label)
                
                adv_label = torch.argmax(pred).item()
                
                orig_S = s
                if adv_label != orig_label.item():
                    break
        return orig_S, adv_label, n+1


    