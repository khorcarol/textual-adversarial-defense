k=20
python main.py \
    --attack_name charmix \
    --device cuda \
    --dataset qnli \
    --model textattack/roberta-base-QNLI  \
    --k $k \
    --n_positions 10 \
    --subset 100

# python main.py \
#     --attack_name positionrand \
#     --device cuda \
#     --dataset qnli \
#     --model textattack/roberta-base-QNLI  \
#     --k $k \
#     --n_positions 5 \
#     --subset 20

