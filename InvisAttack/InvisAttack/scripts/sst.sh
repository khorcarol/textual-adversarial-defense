k=10
python main.py \
    --attack_name charmix \
    --device cuda \
    --dataset sst2 \
    --model textattack/roberta-base-SST-2 \
    --k $k \
    --n_positions 5 \
    --subset 100

# python main.py \
#     --attack_name positionrand \
#     --device cuda \
#     --dataset sst2 \
#     --model textattack/roberta-base-SST-2 \
#     --k $k \
#     --n_positions 5 \
#     --subset 20

