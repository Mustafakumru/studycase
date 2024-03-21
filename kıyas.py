import os
import cv2
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input


def load_and_preprocess_image(image_path):
    # Resmi yükle
    image = cv2.imread(image_path)
    # Boyutunu değiştir ve VGG16 modeli için ön işlem yap
    resized_image = cv2.resize(image, (224, 224))
    preprocessed_image = preprocess_input(resized_image)
    return preprocessed_image


def evaluate_image_quality(image_path, model):
    # Resmi yükle ve ön işleme yap
    image = load_and_preprocess_image(image_path)
    # Tahmin yap
    prediction = model.predict(np.expand_dims(image, axis=0))
    return prediction[0][0]  # Örnek olarak, sadece ilk sınıfın olasılığını kullanıyoruz


def categorize_quality_score(score):
    if score >= 0.5:
        return "yüksek kalite"
    elif score >= 0.3:
        return "orta kalite"
    else:
        return "düşük kalite"


if __name__ == "__main__":
    folder_path = "C:/Users/Mkumru/Desktop/Apparel"  # Klasör yolunu güncelleyin
    image_files = os.listdir(folder_path)

    # VGG16 modelini yükle
    model = VGG16(weights="imagenet", include_top=True)

    # Her bir resmin kalite kategorisini tahmin et
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        if os.path.isfile(image_path):
            quality_score = evaluate_image_quality(image_path, model)
            quality_category = categorize_quality_score(quality_score)
            print(f"{image_file}: {quality_category}")
