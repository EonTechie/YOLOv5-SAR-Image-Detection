
# YOLOv5 SAR Training

This project demonstrates training a YOLOv5 object detector for Synthetic Aperture Radar (SAR) imagery. The model is trained for 1000 epochs using custom datasets.

## Features
- Integration with Google Colab for streamlined execution
- Roboflow dataset management for easy data handling
- Training visualization and evaluation with TensorBoard
- Exported YOLOv5 weights for future inference

## Requirements
- Python
- PyTorch
- Dependencies listed in `requirements.txt`

## Steps to Use
1. Clone the YOLOv5 repository:
   ```bash
   git clone https://github.com/ultralytics/yolov5
   ```
2. Download and prepare your dataset. Ensure it's compatible with YOLOv5.
3. Update the `data.yaml` file with your dataset's information.
4. Train the model:
   ```bash
   python train.py --img 416 --batch 16 --epochs 1000 --data your_dataset_path/data.yaml --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache
   ```
5. Evaluate the model's performance using TensorBoard or manual plots.

## Outputs
- Trained weights are saved in the `runs/train/yolov5s_results/weights/` directory.
- Training performance metrics and loss graphs are available in the `runs/train/yolov5s_results/` directory.

## Usage
Use the following command for inference on test images:
```bash
python detect.py --weights runs/train/yolov5s_results/weights/best.pt --img 416 --conf 0.4 --source ../test/images
```

## Download Links
- [Trained Model Weights](https://colab.research.google.com/drive/1dMr7vD4si_G6CRvXXyfl9m0zroAlUjDh)
- [Project Repository](https://github.com/ultralytics/yolov5)
