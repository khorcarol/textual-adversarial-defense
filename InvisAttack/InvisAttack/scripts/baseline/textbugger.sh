k=10
python main.py \
    --attack_name textbugger \
    --device cuda \
    --dataset sst2 \
    --model textattack/roberta-base-SST-2 \
    --subset 100