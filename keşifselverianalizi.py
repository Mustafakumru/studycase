import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Kök dizin yolu
root_path ="C:/Users/Mkumru/Desktop/veriAnaliziTumResimler"

# Bilgileri saklamak için boş listelerin oluşturulması
sizes = []  # resim boyutlarını (byte cinsinden) saklamak için
widths = []  # resim genişliklerini (piksel cinsinden) saklamak için
heights = []  # resim yüksekliklerini (piksel cinsinden) saklamak için
contrast_values = []  # resimlerin kontrast değerlerini saklamak için

# Her alt dizindeki her resim dosyası üzerinde döngü
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # OpenCV kullanarak resim dosyasını yükleme
            img_path = os.path.join(dirpath, filename)
            img = cv2.imread(img_path)

            # Resmin boyutunu elde etme
            size = os.path.getsize(img_path)
            sizes.append(size)

            # Resmin çözünürlüğünü elde etme
            width, height = img.shape[1], img.shape[0]
            widths.append(width)
            heights.append(height)

            # Kontrast değerini hesaplama
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Resmi gri tonlamalıya dönüştürme
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])  # Histogramı hesaplama
            contrast_values.append(hist.std())  # Histogramın standart sapması kontrast değeri olarak kullanılır

# Listeleri numpy dizilerine dönüştürme
sizes = np.array(sizes)
widths = np.array(widths)
heights = np.array(heights)
contrast_values = np.array(contrast_values)

# Resim boyutlarının histogramını çizme
plt.hist(sizes, bins=50, color='skyblue', edgecolor='black')
plt.title("Resim Boyutlarının Dağılımı")
plt.xlabel("Dosya Boyutu (byte)")
plt.ylabel("Resim Sayısı")
plt.show()

# Resim genişlikleri ve yüksekliklerinin histogramlarını çizme
plt.figure()
plt.hist(widths, bins=50, color='orange', edgecolor='black', alpha=0.7, label='Genişlik')
plt.hist(heights, bins=50, color='green', edgecolor='black', alpha=0.7, label='Yükseklik')
plt.title("Resim Çözünürlüklerinin Dağılımı")
plt.xlabel("Çözünürlük")
plt.ylabel("Resim Sayısı")
plt.legend()
plt.show()

# Çözünürlükleri içeren bir veri çerçevesi oluşturma
df = pd.DataFrame({'Genişlik': widths, 'Yükseklik': heights})

# Plotly ile 3B dağılım grafiği oluşturma
fig = px.scatter_3d(df, x='Genişlik', y='Yükseklik', z=df.index,
                    title='Resim Çözünürlüklerinin Dağılımı',
                    labels={'Genişlik': 'Genişlik (piksel)',
                            'Yükseklik': 'Yükseklik (piksel)',
                            'index': 'Resim İndeksi'},
                    color=df.index)

# Grafiği özelleştirme
fig.update_traces(marker=dict(size=2, line=dict(width=0.5)))

# Grafiği gösterme
fig.show()
