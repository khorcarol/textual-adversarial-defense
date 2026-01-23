k=10
# python main.py \
#     --attack_name textfooler \
#     --device cuda \
#     --dataset sst2 \
#     --model textattack/roberta-base-SST-2 \
#     --subset 100

python main.py \
    --attack_name textfooler \
    --device cuda \
    --dataset mnli \
    --model textattack/roberta-base-MNLI \
    --subset 100