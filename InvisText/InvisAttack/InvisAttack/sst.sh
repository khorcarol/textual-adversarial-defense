# python main.py \
#     --device cuda \
#     --dataset sst2 \
#     --model textattack/roberta-base-SST-2 \
#     --n_positions 5 \
#     --subset 100

python main.py \
    --attack_name positionrand \
    --device cuda \
    --dataset sst2 \
    --model textattack/roberta-base-SST-2 \
    --n_positions 5 \
    --subset 100

