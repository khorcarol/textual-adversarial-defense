import argparse
import myutils
import dataloader
import torch
import time
from tqdm import tqdm
import pandas as pd
import os

# model, dataset, n_positions, subset

parser = argparse.ArgumentParser()
MODELS = ["textattack/roberta-base-SST-2"]
DATASETS = ["sst2"]
ATTACK_NAME = ["charmix", "fullrand", "positionrand"]

parser.add_argument('--model', type=str, default= "textattack/roberta-base-SST-2", help=f'Pre-trained model name. One of {" | ".join(MODELS)}')
parser.add_argument('--dataset', type=str, default='sst2', help=f'Dataset name. One of {" | ".join(DATASETS)}')
parser.add_argument('--n_positions', type=int, default=512, help='Maximum number of perturbations')
parser.add_argument('--subset', type=int, default=None, help='Subset of dataset to use')
parser.add_argument('--attack_name', type=str, default='charmix', help=f'Name of the attack method. One of {" | ".join(ATTACK_NAME)}')
parser.add_argument('--device', type = str, default = 'cuda',help='cpu or cuda')


args = parser.parse_args()
args.device = torch.device(args.device) 


attack_dataset = dataloader.load_attack_dataset(args.dataset)
num_classes = dataloader.get_class_num(args.dataset)
model_wrapper = myutils.load_model(args)
attacker = myutils.get_attacker(model_wrapper, args)

test_size = len(attack_dataset['label']) if args.subset is None else min(args.subset, len(attack_dataset['label']))
df = {'original':[], 'perturbed':[], 'True':[], 'Pred_original':[],'Pred_perturbed':[],'success':[],'time':[], 'n_positions':[]}


start_time_all = time.time()
count,skip,succ,fail = 0,0,0,0
for idx in tqdm(range(test_size)):
    
    orig_S = attack_dataset['sentence'][idx]
    orig_label = torch.tensor([attack_dataset['label'][idx]]).to(args.device)
    pred_label = torch.argmax(model_wrapper([orig_S])[0]).item()

    df['original'].append(orig_S)
    df['True'].append(orig_label.item())
    df['Pred_original'].append(pred_label)
    
    if orig_label.item()!= pred_label:
        skip += 1
        count += 1
        print("Skipping wrong sample")
        df['perturbed'].append(None)
        df['Pred_perturbed'].append(-1)
        df['success'].append(False)
        df['time'].append(-1)
        df['n_positions'].append(-1)
        continue
    
    
    start_time_single = time.time()
    adv_example,adv_label, n_positions= attacker.attack(orig_S,orig_label)
    end_time_single = time.time()
    
    df['perturbed'].append(adv_example)
    df['Pred_perturbed'].append(adv_label)
    df['success'].append(adv_label!= orig_label.item())
    df['time'].append(end_time_single - start_time_single)
    df['n_positions'].append(n_positions)
    
    if adv_label!= orig_label.item():
        succ += 1
    else:
        fail += 1
    
    count += 1
    
end_time_all = time.time()
print(f"[Succeeded /Failed / Skipped / Total] {succ} /{fail} / {skip} / {len(attack_dataset['label'])}")
print(f"Total time: {end_time_all - start_time_all} seconds for {count} samples")


output_df = pd.DataFrame(df)

safe_model_name = args.model.replace("/", "-")
output_name = f"{args.attack_name}_{safe_model_name}_{args.dataset}_{args.n_positions}npos_{args.subset}subset.csv"
folder_name = os.path.join("results")
os.makedirs(folder_name, exist_ok=True)

full_path = os.path.join(folder_name, output_name)
output_df.to_csv(full_path, index=False)
print("File saved to ", full_path)