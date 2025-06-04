import json
import requests
import os
import shutil
import time

def temizle_prompt(prompt):
    """Prompt'u temizler ve boşlukları düzenler"""
    if not prompt:
        return ""
    prompt = prompt.strip()
    while prompt.endswith(","):
        prompt = prompt[:-1].strip()
    return prompt

def gorsel_uret(prompt, index, negative_prompt="", hedef_klasor=None, hikaye_adi=None):
    """
    Görsel üretir ve belirtilen klasöre kopyalar
    
    Args:
        prompt: Pozitif prompt
        index: Sahne numarası
        negative_prompt: Negatif prompt
        hedef_klasor: Ana klasör
        hikaye_adi: Hikaye adı (alt klasör için)
    """
    prompt = temizle_prompt(prompt)
    negative_prompt = temizle_prompt(negative_prompt)

    if not prompt:
        raise ValueError("Prompt boş olamaz!")

    with open("workflow_api.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Promptları workflow'a yerleştir
    data["4"]["inputs"]["text"] = prompt
    data["5"]["inputs"]["text"] = negative_prompt

    # CLIP text encode clip parametreleri kesin olmalı
    data["4"]["inputs"]["clip"] = ["1", 1]
    data["5"]["inputs"]["clip"] = ["1", 1]

    # Unique seed kullan
    data["6"]["inputs"]["seed"] = int(time.time() * 1000) % 2147483647

    # Debug için JSON'u yazdır
    print(f"[DEBUG] Gönderilen JSON:")
    print(f"  Positive prompt: {data['4']['inputs']['text'][:100]}...")
    print(f"  Negative prompt: {data['5']['inputs']['text'][:50]}...")
    print(f"  Seed: {data['6']['inputs']['seed']}")

    # API isteği gönder
    payload = {"prompt": data}
    response = requests.post("http://127.0.0.1:8188/prompt", json=payload)

    if response.status_code != 200:
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response text: {response.text}")
        raise Exception(f"ComfyUI hatası: {response.text}")

    # Response'dan prompt ID'yi al
    result = response.json()
    prompt_id = result.get("prompt_id")
    
    if not prompt_id:
        print("⚠️ Prompt ID alınamadı, dosya kopyalama yapılamayacak")
        print(f"✅ [{index}] Görsel üretildi (ComfyUI output klasöründe)")
        return result

    print(f"🔄 Görsel üretiliyor... (Prompt ID: {prompt_id})")
    
    # Görselin oluşmasını bekle
    max_bekleme = 60  # 60 saniye max
    bekleme_suresi = 0
    
    while bekleme_suresi < max_bekleme:
        time.sleep(2)
        bekleme_suresi += 2
        
        # ComfyUI output klasörünü kontrol et
        comfyui_output = "ComfyUI/output"
        if os.path.exists(comfyui_output):
            # Tüm PNG dosyalarını kontrol et (gorsel_ öneki olmadan)
            dosyalar = []
            for dosya in os.listdir(comfyui_output):
                if dosya.lower().endswith(".png"):
                    dosya_yolu = os.path.join(comfyui_output, dosya)
                    # Son 10 saniye içinde oluşturulan dosyaları al
                    if os.path.getmtime(dosya_yolu) >= (time.time() - 10):
                        dosyalar.append((dosya_yolu, os.path.getmtime(dosya_yolu)))
            
            if dosyalar:
                # En son değiştirilen dosyayı al
                en_son_dosya = max(dosyalar, key=lambda x: x[1])[0]
                
                # Hikaye klasörü oluştur
                if hedef_klasor and hikaye_adi:
                    hikaye_klasoru = os.path.join(hedef_klasor, hikaye_adi)
                    klasor_olustur(hikaye_klasoru)
                    hedef_dosya = os.path.join(hikaye_klasoru, f"sahne_{index:02d}.png")
                elif hedef_klasor:
                    hedef_dosya = os.path.join(hedef_klasor, f"sahne_{index:02d}.png")
                else:
                    print(f"✅ [{index}] Görsel üretildi: {en_son_dosya}")
                    return result
                
                # Dosyayı kopyala
                try:
                    shutil.copy2(en_son_dosya, hedef_dosya)
                    print(f"📁 Görsel kopyalandı: {hedef_dosya}")
                except Exception as e:
                    print(f"⚠️ Dosya kopyalama hatası: {e}")
                
                print(f"✅ [{index}] Görsel üretildi!")
                return result
        
        print(f"⏳ Bekleniyor... ({bekleme_suresi}s)")
    
    print(f"⚠️ [{index}] Zaman aşımı - 30 saniye sonra dosya bulunamadı")
    return result

def comfyui_durumu_kontrol():
    """ComfyUI'nin çalışıp çalışmadığını kontrol eder"""
    try:
        response = requests.get("http://127.0.0.1:8188/system_stats", timeout=5)
        if response.status_code == 200:
            print("✅ ComfyUI çalışıyor")
            return True
        else:
            print(f"⚠️ ComfyUI yanıt verdi ama durum kodu: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ ComfyUI'ye bağlanılamıyor - Servis çalışmıyor olabilir")
        return False
    except requests.exceptions.Timeout:
        print("❌ ComfyUI zaman aşımı")
        return False
    except Exception as e:
        print(f"❌ ComfyUI durumu kontrol edilemedi: {e}")
        return False

def klasor_olustur(klasor_yolu):
    """Belirtilen klasörü oluşturur"""
    try:
        if not os.path.exists(klasor_yolu):
            os.makedirs(klasor_yolu)
            print(f"📁 Klasör oluşturuldu: {klasor_yolu}")
        return True
    except Exception as e:
        print(f"❌ Klasör oluşturma hatası: {e}")
        return False

# Örnek kullanım
if __name__ == "__main__":
    # Önce ComfyUI'nin çalışıp çalışmadığını kontrol et
    if not comfyui_durumu_kontrol():
        print("❌ ComfyUI çalışmıyor, lütfen önce başlatın!")
        exit(1)
    
    # Hedef klasörü oluştur
    hedef_klasor = "uretilen_gorseller"
    if klasor_olustur(hedef_klasor):
        # Örnek görsel üret
        try:
            prompt = "güzel manzara, dağlar, gün batımı, yüksek kalite"
            negative_prompt = "bulanık, düşük kalite, çirkin"
            
            gorsel_uret(
                prompt=prompt,
                index=1,
                negative_prompt=negative_prompt,
                hedef_klasor=hedef_klasor,
                hikaye_adi="Ornek_Hikaye"
            )
            
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")