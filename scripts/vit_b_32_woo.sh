train_data_file="/home/work/cc_ocr/data_s/train/tar_addr.txt"
val_data_file="/home/work/cc_ocr/data_s/val/tar_addr.txt"

train_data=$(cat $train_data_file)
val_data=$(cat $val_data_file)



python3 /home/work/VisionAI_Intern_Project/open_clip_vision_enc/src/open_clip_train/main.py \
    --model ViT-B-32 \
    --name vit-B-32_data-s_11 \
    --image-mean 0.556 0.531 0.504 \
    --image-std 0.326 0.321 0.334 \
    --seed 0 \
    --save-frequency 1 \
    --dataset-type webdataset \
    --train-data="${train_data}"  \
    --val-data="${val_data}"  \
    --batch-size=64 \
    --lr=1e-4 \
    --epochs=30 \
    --workers=1 \
    --train-num-samples 1014744 \
    --val-num-samples 253687  \
    --device cuda  \
    --report-to wandb  \
    --wandb-project-name KT_VisionAI_Intern_Project \
    --log-every-n-steps 100 \
    --logs=/home/work/VisionAI_Intern_Project/open_clip_vision_enc/scripts/logs

