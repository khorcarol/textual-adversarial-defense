from transformers import AutoTokenizer, AutoModelForSequenceClassification,AutoModelForCausalLM
import torch
# import typing

TAG_CHARS = list(range(0xE0000, 0xE007F + 1))  # Unicode tag characters
VARIATION_SELECTORS = [*range(0xFE00, 0xFE0F + 1), *range(0xE0100, 0xE01EF + 1)]  # Variation selectors
BIDI_CHARS = [*range(0x200E, 0x200F+1),*range(0x202A, 0x202E + 1), *range(0x2066, 0x2069 + 1)]  # Bidi control characters
DEL_CHAR = [0x0008]  # Deletion character
INVIS_CHAR = [0x200b, 0x200c, 0x200d, 0xFEFF, 0x2060] #zero-widths

def load_model(args):
    if "llama" in args.model:
        pass
    else:
        import textattack
        model_name = args.model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name,ignore_mismatched_sizes=True)
        model = model.eval()
        model = model.to(args.device)
        model_wrapper = textattack.models.wrappers.HuggingFaceModelWrapper(model, tokenizer)
    return model_wrapper

def get_attacker(model_wrapper, args):
    if args.attack_name in ['charmix', 'positionrand']:
        from charmix import Charmix
        attack = Charmix(model_wrapper, args)
    elif args.attack_name in ['boucher']:
        from boucher import Boucher
        attack = Boucher(model_wrapper, args)
    else:
        import textattack
        if args.attack_name == 'textfooler':
            attack = textattack.attack_recipes.TextFoolerJin2019.build(model_wrapper)
        elif args.attack_name == 'textbugger':
            attack = textattack.attack_recipes.TextBuggerLi2018.build(model_wrapper)
        elif args.attack_name == 'bertattack':
            attack = textattack.attack_recipes.BERTAttackLi2020.build(model_wrapper)
        elif args.attack_name == 'deepwordbug':
            attack = textattack.attack_recipes.DeepWordBugGao2018.build(model_wrapper)
        
    return attack

def cw_loss(logits, true_class):
    max_other_logit, _ = (torch.cat((logits[:,:true_class], logits[:,true_class+1:]), dim= -1)).max(dim=-1)
    return max_other_logit - logits[:, true_class]


class cw_loss_batched():
    '''
    Computes the Carlini-Wagner loss for 
    '''
    def __init__(self,reduction = 'None'):
        self.reduction = reduction
    
    def __call__(self,logits, true_classes):
        L = torch.cat([cw_loss(l.unsqueeze(0), t) for l,t in zip(logits,true_classes)], dim=0)
        if self.reduction == 'mean':
            return torch.mean(L)
        elif self.reduction == 'sum':
            return torch.sum(L)
        else:
            return L
    
    
# def cw_loss(logits, true_class):
#     max_other_logit, _ = (torch.cat((logits[:true_class], logits[true_class+1:]))).max(dim=-1)
#     return max_other_logit - logits[true_class]

# class cw_loss_batched():
#     def __init__(self,reduction = 'None'):
#         self.reduction = reduction
    
#     def __call__(self,logits, true_classes):
#         L = torch.cat([cw_loss(l, t) for l,t in zip(logits,true_classes)], dim=0)
#         if self.reduction == 'mean':
#             return torch.mean(L)
#         elif self.reduction == 'sum':
#             return torch.sum(L)
#         else:
#             return L

def generate_all_sentences_at_z_with_u(S, z, u):
    
    SS =  "_" + "_".join(S) + "_"
    SS = SS[:z] + chr(u) + SS[z+1:]
    
    mask = [1]*len(SS)
    for pos in range(0,len(mask), 2):
        mask[pos] = 0
    mask[z] = 1
    
    new_SS = [ch if m else "" for ch,m in zip(SS,mask)]
    return "".join(new_SS)
    

def generate_all_sentences_at_z(S, z, V):
    return [generate_all_sentences_at_z_with_u(S, z, u) for u in V]
        
        
def generate_all_sentences(S, V, subset_z=None): 
    out = []
    if subset_z is None:
        subset_z = range(0, 2*len(S)+1, 2)
    for z in subset_z:
        out += generate_all_sentences_at_z(S, z,V)
    
    return out

        
    
# cw_loss(torch.tensor([[1.0, 2.0, 0.5]]), 0)
res = generate_all_sentences("abc", [ord("1")])
print(res)