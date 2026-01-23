k=10

python main.py \
    --attack_name charmix \
    --device cuda \
    --dataset rte \
    --model textattack/roberta-base-RTE  \
    --k $k \
    --n_positions 5 \
    --subset 100

# python main.py \
#     --attack_name positionrand \
#     --device cuda \
#     --dataset rte \
#     --model textattack/roberta-base-RTE \
#     --n_positions 10 \
#     --subset 10

