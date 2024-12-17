from PIL import Image
import math
from datetime import datetime
import time
import os
import sys

t1 = datetime.now()
print(f"Başlama zamanı: {t1}")
sayac=0
def resimlestir(dosya_yolu,uzantı,sekil=1):
    def renkolustur(metin):
        # Metni hex'e çevir
        hex_metin = metin.encode("utf-8").hex()
        # Hex uzunluğunu 6'nın katına tamamla
        while len(hex_metin) % 6 != 0:
            hex_metin += "20"  # '20' (space) ile doldur

        rgb_values = []
        for i in range(0, len(hex_metin), 6):
            segment = hex_metin[i:i+6]
            r = int(segment[0:2], 16)
            g = int(segment[2:4], 16)
            b = int(segment[4:6], 16)
            rgb_values.append((r, g, b))
        return rgb_values

    try:
        dosya_yolu = dosya_yolu.replace('\\', '/')
        if not os.path.isfile(dosya_yolu):
            print("Dosya bulunamadı.")
            return
        
        print("Dosya okunmaya başladı")
        with open(dosya_yolu, "r", encoding="utf-8") as file:
            mes = file.read()
        
        t2 = datetime.now()
        print(f"Harcanan süre: {t2 - t1}")
        print("Mesaj parçaları oluşturuluyor...")
        
        mes_parts = [mes[i:i + 3] for i in range(0, len(mes), 3)]
        print("Renkler oluşturuluyor")
        
        renkler = []
        for part in mes_parts:
            renkler.extend(renkolustur(part))
        
        t3 = datetime.now()
        print(f"Harcanan süre: {t3 - t2}")
        print("Resim oluşturuluyor")
        if sekil==1:
            width=height=math.ceil(math.sqrt(len(renkler)))
        elif sekil==2:
            katsayi = math.ceil(math.sqrt(len(renkler)/9/16))
            width=16*katsayi
            height=9*katsayi
        image = Image.new("RGB", (width, height))
        pixels = image.load()
        
        for idx, color in enumerate(renkler):
            x, y = idx % width, idx // width
            pixels[x, y] = color

        image.save(f"steganografi.{uzantı}")
        print(f"{uzantı} dosyası başarıyla oluşturuldu.")
        print(f"Harcanan süre toplam: {datetime.now() - t1}")
        print("*"*40)
    
    except Exception as ex:
        print(f"Hata: {ex}")
        time.sleep(5)
        sys.exit()
def metinlestir(resim_yolu):
    global sayac
    sayac+=1
    try:
        resim_yolu = resim_yolu.replace('\\', '/')
        if not os.path.isfile(resim_yolu):
            print("Resim dosyası bulunamadı.")
            return

        t2 = datetime.now()
        print(f"Harcanan süre: {t2 - t1}")
        print("Resim okunuyor...")
        
        image = Image.open(resim_yolu)
        width, height = image.size

        hex_string = ""
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                hex_string += f"{r:02x}{g:02x}{b:02x}"

        try:
            tam_mesaj = bytes.fromhex(hex_string).decode('utf-8').strip()
        except UnicodeDecodeError:
            raise Exception("Geçersiz hex veya decode hatası!")
            breakpoint()        
        t3 = datetime.now()
        print(f"Harcanan süre: {t3 - t2}")
        print("Mesaj yazdırılıyor...")

        with open(f"desifre_steganografi{sayac}.txt", "w", encoding="utf-8") as file:
            file.write(tam_mesaj)

        print("Mesaj başarıyla yazdırıldı.")
        print(f"Harcanan süre toplam: {datetime.now() - t1}")

    except Exception as ex:
        print(f"Hata: {ex}")
        print("Program kapatılıyor......")
        time.sleep(5)
        sys.exit()

