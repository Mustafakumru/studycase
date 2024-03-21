import os
from PIL import Image

def classify_image_quality(image_path, size_threshold_high=1900000, size_threshold_low=7000, color_threshold=100):
    """
    Verilen bir resmin piksel yoğunluğuna ve renk yoğunluğuna göre kalitesini belirler.
    :param image_path: Resmin dosya yolu
    :param size_threshold_high: Yüksek kalite için boyut eşik değeri
    :param size_threshold_low: Düşük kalite için boyut eşik değeri
    :param color_threshold: Renk yoğunluğu eşik değeri
    :return: Sınıflandırılmış görüntü kalitesi (yüksek, orta, düşük)
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            pixel_count = width * height
            # Renk yoğunluğunu hesapla
            colors = img.getcolors()
            color_density = sum([count for count, color in colors])

            if pixel_count >= size_threshold_high and color_density >= color_threshold:
                return 'yüksek'
            elif pixel_count >= size_threshold_low:
                return 'orta'
            else:
                return 'düşük'
    except Exception as e:
        print(f"Hata: {e}")
        return 'bilinmiyor'

def classify_images_in_directory(directory_path, size_threshold_high=1900000, size_threshold_low=7000,
                                 color_threshold=100):
    """
    Verilen bir dizindeki tüm resim dosyalarını piksel yoğunluğuna göre sınıflandırır.
    :param directory_path: Resimlerin bulunduğu dizinin yolu
    :param size_threshold_high: Yüksek kalite için boyut eşik değeri
    :param size_threshold_low: Düşük kalite için boyut eşik değeri
    :param color_threshold: Renk yoğunluğu eşik değeri
    :return: Sınıflandırılmış resimlerin sözlüğü {dosya_adı: kalite}
    """
    image_qualities = {}
    for filename in os.listdir(directory_path):
        if filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            image_path = os.path.join(directory_path, filename)
            quality = classify_image_quality(image_path, size_threshold_high, size_threshold_low, color_threshold)
            image_qualities[filename] = quality
    return image_qualities

# Örnek kullanım:
directory_path = "C:/Users/Mkumru/Desktop/veriAnaliziTumResimler"
image_qualities = classify_images_in_directory(directory_path)

for filename, quality in image_qualities.items():
    print(f"{filename}: {quality}")
