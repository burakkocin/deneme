import requests
import time
import os
import re
from datetime import datetime
from gorsel_uret import gorsel_uret
from sahne_uretici import ai_ile_sahneler_uret

# Sabit kedi karakteri - HER görselde aynı
SABIT_KEDI = "cute orange cartoon tabby cat with white paws, big eyes, same face and fur, consistent character design, same character throughout"

# Görsel stil ayarları
STIL = "anime style, ultra realistic lighting, cinematic composition, 4k illustration, high detail, expressive face, full body, colorful, vibrant"

# Negatif prompt - istenmeyen öğeler
NEGATIVE_PROMPT = "ugly, blurry, bad anatomy, bad hands, extra limbs, distorted face, cropped, low quality, watermark, text, error, worst quality, lowres, different character, inconsistent character, multiple cats, deformed"

def cevir_en(metin):
    """Türkçe metni İngilizce'ye çevirir"""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": "tr", "tl": "en", "dt": "t", "q": metin}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        ceviri = response.json()
        return ceviri[0][0][0]
    except Exception as e:
        print(f"⚠️ Çeviri hatası: {e}")
        return metin

def temizle_prompt(prompt):
    """Prompt'u temizler ve düzenler"""
    if not prompt:
        return ""
    prompt = prompt.strip()
    while prompt.endswith(","):
        prompt = prompt[:-1].strip()
    return prompt

def dosya_adi_temizle(metin):
    """Dosya adı için güvenli string oluşturur"""
    # Türkçe karakterleri değiştir
    turkce_karakter = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'I': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    }
    
    for tr_kar, en_kar in turkce_karakter.items():
        metin = metin.replace(tr_kar, en_kar)
    
    # Sadece harf, rakam, boşluk ve tire bırak
    metin = re.sub(r'[^a-zA-Z0-9\s\-]', '', metin)
    # Boşlukları tire yap
    metin = re.sub(r'\s+', '_', metin.strip())
    # Çoklu tire'leri tek tire yap
    metin = re.sub(r'_+', '_', metin)
    # Baş ve sondaki tireleri kaldır
    metin = metin.strip('_')
    
    return metin.lower()

def klasor_olustur(baslik):
    """Hikaye için klasör oluşturur ve yolunu döndürür"""
    # Zaman damgası ekle
    zaman = datetime.now().strftime("%Y%m%d_%H%M%S")
    temiz_baslik = dosya_adi_temizle(baslik)
    
    klasor_adi = f"{zaman}_{temiz_baslik}"
    klasor_yolu = os.path.join("hikayeler", klasor_adi)
    
    # Klasörü oluştur
    os.makedirs(klasor_yolu, exist_ok=True)
    os.makedirs("hikayeler", exist_ok=True)
    
    return klasor_yolu, klasor_adi

def hikaye_dosyasi_olustur(klasor_yolu, baslik, sahneler):
    """Hikaye detaylarını metin dosyasına yazar"""
    dosya_yolu = os.path.join(klasor_yolu, "hikaye_detaylari.txt")
    
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        f.write(f"🐱 KEDİ HİKAYESİ 🐱\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"📚 Ana Başlık: {baslik}\n")
        f.write(f"📅 Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write(f"🎬 Toplam Sahne: {len(sahneler)}\n\n")
        f.write("🎭 SAHNELER:\n")
        f.write("-" * 30 + "\n")
        
        for i, sahne in enumerate(sahneler, 1):
            f.write(f"\n{i:2d}. {sahne}\n")
        
        f.write(f"\n\n📝 PROMPT BİLGİLERİ:\n")
        f.write("-" * 30 + "\n")
        f.write(f"🐱 Sabit Karakter: {SABIT_KEDI}\n")
        f.write(f"🎨 Stil: {STIL}\n")
        f.write(f"❌ Negatif: {NEGATIVE_PROMPT}\n")

def main():
    print("🐱" + "=" * 48 + "🐱")
    print("    KEDİ HİKAYE GÖRSEL ÜRETİCİSİ v2.0")
    print("🐱" + "=" * 48 + "🐱")
    print()
    
    # Kullanıcıdan ana hikaye başlığını al
    print("📚 Ana hikaye başlığınızı yazın:")
    print("   Örnek: 'kedi yavru kurdu kaçırdı'")
    print("   Örnek: 'kedi uzaya yolculuk yapıyor'")
    print("   Örnek: 'kedi büyük maceraya çıkıyor'")
    print()
    
    baslik = input("➤ Hikaye başlığı: ").strip()
    if not baslik:
        print("❌ Başlık boş olamaz.")
        return

    # Sahne sayısını al
    try:
        sahne_sayisi = input("➤ Kaç sahne istiyorsunuz? (varsayılan: 8): ").strip()
        sahne_sayisi = int(sahne_sayisi) if sahne_sayisi else 8
        if sahne_sayisi < 3 or sahne_sayisi > 20:
            print("⚠️ Sahne sayısı 3-20 arasında olmalı. 8 kullanılacak.")
            sahne_sayisi = 8
    except ValueError:
        sahne_sayisi = 8

    print(f"\n🎬 '{baslik}' için {sahne_sayisi} sahne üretiliyor...")
    
    # Sahneleri üret
    sahneler_tr = ai_ile_sahneler_uret(baslik, sahne_sayisi)
    if not sahneler_tr:
        print("❌ Sahne üretilemedi.")
        return

    # Klasör oluştur
    klasor_yolu, klasor_adi = klasor_olustur(baslik)
    print(f"📁 Klasör oluşturuldu: hikayeler/{klasor_adi}")
    
    # Hikaye dosyası oluştur
    hikaye_dosyasi_olustur(klasor_yolu, baslik, sahneler_tr)
    
    print(f"✅ {len(sahneler_tr)} sahne üretildi!")
    print(f"📝 Hikaye detayları kaydedildi: {klasor_yolu}/hikaye_detaylari.txt")
    
    # Sahneleri göster
    print(f"\n🎭 SAHNELER:")
    print("-" * 50)
    for i, sahne in enumerate(sahneler_tr, 1):
        print(f"{i:2d}. {sahne}")
    
    print(f"\n🎨 GÖRSEL ÜRETİMİ BAŞLIYOR...")
    print("=" * 50)
    
    # Her sahne için görsel üret
    basarili_sahneler = 0
    for i, sahne_tr in enumerate(sahneler_tr, 1):
        print(f"\n🎬 Sahne {i}/{len(sahneler_tr)}")
        print(f"📝 {sahne_tr}")
        
        # Türkçe sahneyi İngilizce'ye çevir
        sahne_en = cevir_en(sahne_tr)
        print(f"🔤 EN: {sahne_en}")
        
        # Tam prompt'u oluştur
        full_prompt = f"{SABIT_KEDI}, {sahne_en}, {STIL}"
        full_prompt = temizle_prompt(full_prompt)
        
        try:
            # Görsel üret (klasör yolu ile)
            gorsel_uret(full_prompt, i, NEGATIVE_PROMPT, klasor_yolu)
            basarili_sahneler += 1
            print(f"✅ Sahne {i} başarıyla oluşturuldu!")
            
        except Exception as e:
            print(f"❌ Sahne {i} hatası: {e}")
            continue
        
        # API'yi zorlamayalım
        if i < len(sahneler_tr):
            print("⏳ Kısa ara...")
            time.sleep(3)
    
    # Sonuç raporu
    print("\n" + "🎉" + "=" * 48 + "🎉")
    print("              İŞLEM TAMAMLANDI!")
    print("🎉" + "=" * 48 + "🎉")
    print(f"📚 Hikaye: {baslik}")
    print(f"📁 Klasör: hikayeler/{klasor_adi}")
    print(f"📊 Toplam sahne: {len(sahneler_tr)}")
    print(f"✅ Başarılı: {basarili_sahneler}")
    print(f"❌ Başarısız: {len(sahneler_tr) - basarili_sahneler}")
    
    if basarili_sahneler > 0:
        print(f"\n🖼️ Görseller şurada: {klasor_yolu}")
        print(f"📝 Hikaye detayları: {klasor_yolu}/hikaye_detaylari.txt")
        print("🎬 Video oluşturmak için video_yap.py'yi düzenleyin.")
    
    print(f"\n💡 İpucu: Farklı hikayeler için programı yeniden çalıştırın!")

if __name__ == "__main__":
    main()