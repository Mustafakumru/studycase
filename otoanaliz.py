import os
import cv2
import numpy as np

# Görsel boyutunu belirlemek için işlev
def calculate_image_size(image):
    return image.shape[0] * image.shape[1]

# Renk dağılımını belirlemek için işlev
def calculate_color_distribution(image):
    # Renk dağılımını hesaplamak için görüntüyü BGR'den HSV'ye dönüştür
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Renk kanallarını ayırma
    h, s, v = cv2.split(hsv_image)
    # Renk dağılımını hesaplamak için histogramı oluşturma
    hist_h = cv2.calcHist([h], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([s], [0], None, [256], [0, 256])
    hist_v = cv2.calcHist([v], [0], None, [256], [0, 256])
    # Histogramları birleştirme
    color_distribution = np.concatenate((hist_h, hist_s, hist_v), axis=None)
    return color_distribution

# Nesne netliğini belirlemek için işlev
def calculate_object_clarity(image):
    # Görüntüyü gri tonlamalıya dönüştürme
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Laplace gradyanını hesaplama
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    return laplacian

# Fotoğrafların kalitesini belirleme işlevi
def determine_quality(image_path):
    # Fotoğrafı yükle
    image = cv2.imread(image_path)
    # Görsel boyutunu belirleme
    image_size = calculate_image_size(image)
    # Renk dağılımını belirleme
    color_distribution = calculate_color_distribution(image)
    # Nesne netliğini belirleme
    object_clarity = calculate_object_clarity(image)
    # Kaliteyi hesaplama
    quality_score = image_size + np.sum(color_distribution) + object_clarity
    return quality_score

# Klasördeki tüm fotoğrafların kalitesini belirleme
def determine_quality_for_folder(folder_path):
    quality_scores = []
    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)
        if os.path.isfile(image_path):
            quality_score = determine_quality(image_path)
            quality_scores.append(quality_score)
    return quality_scores

# Veri setindeki kalite skorlarını kullanarak eşik değerlerini belirleme
def determine_thresholds(quality_scores):
    q25 = np.percentile(quality_scores, 25)
    q75 = np.percentile(quality_scores, 75)
    return q25, q75

# Kalite skorlarını eşik değerlerine göre etiketleme işlevi
def label_quality(quality_score, low_threshold, high_threshold):
    if quality_score >= high_threshold:
        return "yüksek kalite"
    elif quality_score >= low_threshold:
        return "orta kalite"
    else:
        return "düşük kalite"

# Örnek klasör yolu
folder_path = "C:/Users/Mkumru/Desktop/veriAnaliziTumResimler"

# Kaliteyi belirleme ve eşik değerleri belirleme
quality_scores = determine_quality_for_folder(folder_path)
low_quality_threshold, high_quality_threshold = determine_thresholds(quality_scores)

# Kalite etiketlerini hesaplama
quality_labels = []
for file_name in os.listdir(folder_path):
    image_path = os.path.join(folder_path, file_name)
    if os.path.isfile(image_path):
        quality_score = determine_quality(image_path)
        quality_label = label_quality(quality_score, low_quality_threshold, high_quality_threshold)
        quality_labels.append(quality_label)

# Kalite etiketlerinin sayılarını hesaplama
quality_counts = {
    "düşük kalite": quality_labels.count("düşük kalite"),
    "orta kalite": quality_labels.count("orta kalite"),
    "yüksek kalite": quality_labels.count("yüksek kalite")
}

# Dosya yolu ve ismi
output_file_path = "quality_labels.txt"

# Sonuçları dosyaya yazma
with open(output_file_path, 'w') as file:
    file.write("Kalite Etiketleri:\n")
    for file_name, quality_label in zip(os.listdir(folder_path), quality_labels):
        file.write(f"{file_name}: {quality_label}\n")
    file.write("\nKalite Etiket Sayıları:\n")
    for quality_label, count in quality_counts.items():
        file.write(f"{quality_label}: {count}\n")

print("Kalite etiketleri ve sayıları başarıyla dosyaya yazıldı.")
