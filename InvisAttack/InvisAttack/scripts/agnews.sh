k=10
python main.py \
    --attack_name charmix \
    --device cuda \
    --dataset agnews \
    --model textattack/roberta-base-ag-news  \
    --k $k \
    --n_positions 5 \
    --subset 10

# python main.py \
#     --attack_name positionrand \
#     --device cuda \
#     --dataset agnews \
#     --model textattack/roberta-base-ag-news  \
#     --n_positions 5 \
#     --subset 10

