from PIL import Image
import os

def classify_image_quality(image_path, quality_threshold=0.8):
    """
    Verilen bir resmin kalitesini belirli bir eşik değere göre yüksek, orta ve düşük olarak sınıflandırır.
    :param image_path: Resmin dosya yolu
    :param quality_threshold: Görüntü kalitesi için eşik değeri
    :return: Sınıflandırılmış görüntü kalitesi (yüksek, orta, düşük)
    """
    try:
        with Image.open(image_path) as img:
            # Resmin boyutunu al
            width, height = img.size
            # Genellikle, daha büyük boyutlu resimler daha yüksek kalitede olabilir
            # Bu basit bir kriter kullanarak sınıflandırabiliriz
            if width >= 2000 or height >= 2000:
                return 'yüksek'
            elif width >= 1000 or height >= 1000:
                return 'orta'
            else:
                return 'düşük'
    except Exception as e:
        print(f"Hata: {e}")
        return 'bilinmiyor'

def classify_images_in_directory(directory_path, quality_threshold=0.8):
    """
    Verilen bir dizindeki tüm resim dosyalarını sınıflandırır.
    :param directory_path: Resimlerin bulunduğu dizinin yolu
    :param quality_threshold: Görüntü kalitesi için eşik değeri
    :return: Sınıflandırılmış resimlerin sözlüğü {dosya_adı: kalite}
    """
    image_qualities = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory_path, filename)
            quality = classify_image_quality(image_path, quality_threshold)
            image_qualities[filename] = quality
    return image_qualities

# Örnek kullanım:
directory_path = "/Users/Mkumru/Desktop/Apparel"
image_qualities = classify_images_in_directory(directory_path)

for filename, quality in image_qualities.items():
    print(f"{filename}: {quality}")
