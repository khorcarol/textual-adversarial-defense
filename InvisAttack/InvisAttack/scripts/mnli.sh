k=10

python main.py \
    --attack_name charmix \
    --device cuda \
    --dataset mnli \
    --model textattack/roberta-base-MNLI  \
    --k $k \
    --n_positions 10 \
    --subset 10

# python main.py \
#     --attack_name positionrand \
#     --device cuda \
#     --dataset mnli \
#     --model textattack/roberta-base-MNLI  \
#     --k $k \
#     --n_positions 5 \
#     --subset 10

