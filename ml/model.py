import logging

from PIL import Image
import torch
from torchvision import transforms


class ModelInf:
    def __init__(self, use_cuda=True):
        if use_cuda and torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            device_name = "GPU"
        else:
            self.device = torch.device("cpu")
            device_name = "CPU"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info(f"Используется устройство: {device_name}")

        self.model = torch.load("ml/model_checkpoint.pth", weights_only=False)
        self.model = self.model.to(self.device)

        self.model.eval()
        self.test_transforms = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def predict(self, img):
        image = Image.open(img).convert("RGB")

        input_tensor = self.test_transforms(image)
        input_batch = input_tensor.unsqueeze(0)
        input_batch = input_batch.to(self.device)

        with torch.no_grad():
            output = self.model(input_batch)
        prob, predicted_class = torch.max(torch.softmax(output, dim=1), 1)

        return (
            str(
                "Данное изображение реальное (не является сгенерированным ИИ)"
                if predicted_class
                else "Данное изображение сгенерировано ИИ"
            )
            + f" с уверенностью {prob.item() * 100:.2f}"
        )
