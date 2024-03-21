import requests
import os

def download_product_photos(api_url, params, download_folder):
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        for product in data['products']:
            photos = product['photos']

            for index, photo_url in enumerate(photos):
                response_photo = requests.get(photo_url)

                if response_photo.status_code == 200:
                    with open(os.path.join(download_folder, f'photo_{product["id"]}_{index}.jpg'), 'wb') as f:
                        f.write(response_photo.content)
                    print(f"Fotoğraf {product['id']} için başarıyla indirildi.")
                else:
                    print(f"Fotoğraf {product['id']} indirilemedi.")
    else:
        print("API isteği başarısız: ", response.status_code)

# Örnek API URL ve filtre parametreleri
api_url = 'https://example.com/api/products'
params = {
    'category': 'elektronik',  # Örnek bir kategori adı
    # Diğer filtre parametrelerini ekleyin (örneğin, fiyat aralığı, marka, vb.)
}
download_folder = 'downloaded_photos'

os.makedirs(download_folder, exist_ok=True)

download_product_photos(api_url, params, download_folder)
