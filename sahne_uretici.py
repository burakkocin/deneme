import requests
import json
import time
import re

def ai_ile_sahneler_uret(baslik, sahne_sayisi=8):
    """
    Ana metinden dinamik sahneler üretir
    """
    print(f"🤖 '{baslik}' için {sahne_sayisi} sahne üretiliyor...")
    
    # Metni analiz et ve uygun hikaye tipini belirle
    sahneler = gelismis_sahne_uret(baslik, sahne_sayisi)
    return sahneler

def gelismis_sahne_uret(baslik, sahne_sayisi):
    """
    Ana metni detaylı analiz ederek sahne üretir
    """
    baslik_lower = baslik.lower()
    sahneler = []
    
    # Ana karakteri belirle
    ana_karakter = "kedi"
    if "köpek" in baslik_lower:
        ana_karakter = "köpek"
    elif "tavşan" in baslik_lower:
        ana_karakter = "tavşan"
    elif "kuş" in baslik_lower:
        ana_karakter = "kuş"
    
    # Hikaye konusunu ve türünü analiz et
    if "kaçır" in baslik_lower or "çal" in baslik_lower:
        # Neyi kaçırdığını bul
        if "yavru" in baslik_lower and "kurt" in baslik_lower:
            sahneler = yavru_kurt_kaçirma_hikayesi(ana_karakter)
        elif "yavru" in baslik_lower:
            sahneler = genel_yavru_kaçirma_hikayesi(ana_karakter)
        else:
            sahneler = genel_kaçirma_hikayesi(ana_karakter, baslik)
            
    elif "macera" in baslik_lower or "yolculuk" in baslik_lower:
        sahneler = macera_hikayesi_detayli(ana_karakter, baslik)
        
    elif "kayıp" in baslik_lower or "kaybol" in baslik_lower:
        sahneler = kaybolma_hikayesi_detayli(ana_karakter)
        
    elif "arkadaş" in baslik_lower:
        sahneler = arkadas_hikayesi_detayli(ana_karakter)
        
    elif "savaş" in baslik_lower or "kavga" in baslik_lower:
        sahneler = savas_hikayesi_detayli(ana_karakter, baslik)
        
    elif "aşk" in baslik_lower or "sevgi" in baslik_lower:
        sahneler = ask_hikayesi_detayli(ana_karakter)
        
    else:
        # Genel hikaye analizi
        sahneler = akilli_genel_hikaye(ana_karakter, baslik)
    
    # Sahne sayısını ayarla
    return sahne_sayisini_ayarla(sahneler, sahne_sayisi)

def yavru_kurt_kaçirma_hikayesi(karakter):
    """Yavru kurt kaçırma hikayesi - özel detaylı sahneler"""
    return [
        f"{karakter} ormanda sessizce yürüyor, etrafı dikkatli şekilde inceliyor",
        f"{karakter} uzaktan kurt ailesinin seslerini duyuyor, merakla yaklaşıyor",
        f"{karakter} çalıların arkasına saklanıyor, kurt ailesini gizlice izliyor",
        f"{karakter} tek başına oynayan sevimli yavru kurdu fark ediyor",
        f"anne kurt avlanmaya gidiyor, yavru kurt yalnız kalıyor, {karakter} fırsatı görüyor",
        f"{karakter} yavaşça yavru kurdun yanına yaklaşıyor, arkadaş olmak istiyor gibi davranıyor",
        f"yavru kurt {karakter}le oynamaya başlıyor, ikisi birlikte eğleniyor",
        f"{karakter} yavru kurdu oyun bahanesiyle uzaklara doğru çekiyor",
        f"{karakter} ve yavru kurt beraber koşuyor, ormanda saklambaç oynuyor",
        f"anne kurt geri dönüyor, yavrusunu bulamıyor, endişeyle aramaya başlıyor",
        f"diğer kurtlar da aramaya katılıyor, orman çığlıklarla doluyor",
        f"{karakter} yavru kurdla gizli mağarada saklanıyor, dışarıdaki sesleri duyuyor",
        f"yavru kurt ağlamaya başlıyor, annesini özlüyor, {karakter} endişeleniyor",
        f"{karakter} yaptığının yanlış olduğunu anlıyor, pişmanlık hissediyor",
        f"{karakter} yavru kurdu annesine geri götürmeye karar veriyor",
        f"anne kurt yavrusunu görünce sevinçle koşuyor, kurtlar barışçıl şekilde yaklaşıyor",
        f"{karakter} özür diliyor, kurtlar onu affediyor, dostluk kuruluyor",
        f"tüm hayvanlar birlikte oyun oynuyor, orman tekrar huzurlu oluyor"
    ]

def macera_hikayesi_detayli(karakter, baslik):
    """Detaylı macera hikayesi"""
    # Maceranın türünü belirle
    if "uzay" in baslik.lower():
        return uzay_macerasi(karakter)
    elif "deniz" in baslik.lower():
        return deniz_macerasi(karakter)
    elif "dağ" in baslik.lower():
        return dag_macerasi(karakter)
    else:
        return genel_macera(karakter)

def uzay_macerasi(karakter):
    """Uzay macerası hikayesi"""
    return [
        f"{karakter} geceleyin yıldızları izliyor, uzayı merak ediyor",
        f"{karakter} garip bir ışık görüyor, yaklaşıp inceliyor",
        f"ışık bir uzay gemisi çıkıyor, {karakter} şaşırıyor ama merakla yaklaşıyor",
        f"uzaylı dostlar {karakter}yi içeri davet ediyor, heyecanla kabul ediyor",
        f"uzay gemisi kalktıyor, {karakter} ilk kez Dünya'yı yukarıdan görüyor",
        f"{karakter} uzay istasyonunu geziyor, ilginç teknolojiler görüyor",
        f"uzaylı arkadaşlar {karakter}ye galaksiyi gezdiriyor, renkli gezegenler görüyor",
        f"{karakter} uzay yürüyüşü yapıyor, sıfır yerçekiminde eğleniyor",
        f"uzay korsanları saldırıyor, {karakter} arkadaşlarına yardım ediyor",
        f"{karakter} cesurca savaşıyor, uzay gemisini kurtarıyor",
        f"uzaylılar {karakter}yi kahraman olarak kutluyor",
        f"{karakter} Dünya'ya geri dönüyor, unutulmaz anılarla dolu"
    ]

def savas_hikayesi_detayli(karakter, baslik):
    """Savaş/kavga hikayesi"""
    return [
        f"{karakter} huzurlu bir şekilde yaşamını sürdürüyor",
        f"kötü karakterler bölgeye gelip huzuru bozuyor",
        f"{karakter} durumu fark ediyor, ne yapacağını düşünüyor",
        f"{karakter} cesaret topluyor, kötülere karşı durmaya karar veriyor",
        f"ilk karşılaşma oluyor, {karakter} gücünü test ediyor",
        f"{karakter} müttefikler buluyor, ekip oluşturuyor",
        f"büyük savaş hazırlıkları yapılıyor, herkes rolünü alıyor",
        f"nihai savaş başlıyor, {karakter} liderlik yapıyor",
        f"{karakter} zor anlar yaşıyor ama pes etmiyor",
        f"arkadaşlarının yardımıyla güçleniyor",
        f"kötüler yeniliyor, barış geri geliyor",
        f"{karakter} kahraman olarak kutlanıyor, huzur geri geliyor"
    ]

def ask_hikayesi_detayli(karakter):
    """Aşk hikayesi"""
    return [
        f"{karakter} yalnız yaşıyor, arkadaş arıyor",
        f"parkta güzel bir partner görüyor, kalbi hızlanıyor",
        f"{karakter} utangaç şekilde yaklaşmaya çalışıyor",
        f"ilk tanışma oluyor, ikisi de mutlu oluyor",
        f"birlikte vakit geçirmeye başlıyorlar, eğleniyor",
        f"romantik anlar yaşıyorlar, güneş batımında yürüyüş",
        f"küçük bir anlaşmazlık oluyor, üzülüyorlar",
        f"{karakter} hatasını anlıyor, özür dilemeye gidiyor",
        f"barışıyorlar, aşkları daha da güçleniyor",
        f"birlikte yeni maceralar yaşamaya karar veriyorlar",
        f"mutlu son, ikisi birlikte huzurlu yaşıyor"
    ]

def akilli_genel_hikaye(karakter, baslik):
    """Ana metni analiz ederek akıllı hikaye üretimi"""
    baslik_kelimeler = baslik.lower().split()
    
    # Anahtar kelimeleri bul
    duygular = ["mutlu", "üzgün", "kızgın", "korkulu", "heyecanlı"]
    mekanlar = ["orman", "şehir", "ev", "okul", "park", "deniz", "dağ"]
    eylemler = ["koş", "uç", "yüz", "oyna", "keşfet", "araştır"]
    
    # Hikayeyi dinamik olarak oluştur
    sahneler = [
        f"{karakter} hikayenin başında normal yaşamını sürdürüyor",
        f"{karakter} önemli bir olayla karşılaşıyor",
        f"{karakter} durumu analiz ediyor, ne yapacağını düşünüyor"
    ]
    
    # Baslik'tan çıkarılan eylemlere göre orta sahneler
    orta_sahneler = [
        f"{karakter} harekete geçiyor ve maceraya atılıyor",
        f"{karakter} zorluklarla karşılaşıyor ama mücadele ediyor",
        f"{karakter} yeni şeyler öğreniyor ve gelişiyor",
        f"{karakter} kritik bir noktaya geliyor",
        f"{karakter} büyük bir karar veriyor"
    ]
    
    son_sahneler = [
        f"{karakter} amacına ulaşmak için son hamlesini yapıyor",
        f"{karakter} başarıya ulaşıyor ve mutlu oluyor",
        f"{karakter} öğrendiği derslerle hikaye sona eriyor"
    ]
    
    return sahneler + orta_sahneler + son_sahneler

def sahne_sayisini_ayarla(sahneler, hedef_sayi):
    """Sahne sayısını istenen sayıya ayarlar"""
    if len(sahneler) == hedef_sayi:
        return sahneler
    elif len(sahneler) > hedef_sayi:
        # Fazla sahneler varsa, en önemli olanları seç
        baslangic = sahneler[:2]  # İlk 2 sahne
        orta = sahneler[2:-2]     # Orta sahneler
        son = sahneler[-2:]       # Son 2 sahne
        
        # Orta sahnelerden seç
        orta_hedef = hedef_sayi - 4
        if orta_hedef > 0 and len(orta) > orta_hedef:
            # Eşit aralıklarla seç
            adim = len(orta) / orta_hedef
            secilen_orta = [orta[int(i * adim)] for i in range(orta_hedef)]
        else:
            secilen_orta = orta[:orta_hedef] if orta_hedef > 0 else []
        
        return baslangic + secilen_orta + son
    else:
        # Eksik sahneler varsa, genel sahneler ekle
        while len(sahneler) < hedef_sayi:
            sahneler.append("karakterimiz macerasına devam ediyor ve yeni deneyimler yaşıyor")
        return sahneler

def prompt_detaylandir(sahne, karakter_bilgisi, stil_bilgisi):
    """
    Sahne açıklamasını detaylı görsel prompt'a çevirir
    """
    # Sahne analizi
    sahne_lower = sahne.lower()
    
    # Ortam belirleme
    if "orman" in sahne_lower:
        ortam = "deep forest, tall trees, sunlight filtering through leaves, natural environment"
    elif "mağara" in sahne_lower or "saklan" in sahne_lower:
        ortam = "mysterious cave, rocky walls, dim lighting, hidden place"
    elif "koş" in sahne_lower:
        ortam = "dynamic motion blur, running scene, action pose, speed lines"
    elif "uç" in sahne_lower or "uzay" in sahne_lower:
        ortam = "outer space, stars, planets, cosmic background, sci-fi scene"
    else:
        ortam = "beautiful outdoor scene, natural lighting, detailed background"
    
    # Emotion belirleme
    if "mutlu" in sahne_lower or "sevinç" in sahne_lower:
        duygu = "happy expression, joyful, smiling, positive mood"
    elif "üzgün" in sahne_lower or "ağla" in sahne_lower:
        duygu = "sad expression, tears, melancholic mood"
    elif "korku" in sahne_lower or "endişe" in sahne_lower:
        duygu = "worried expression, nervous, cautious pose"
    elif "heyecan" in sahne_lower:
        duygu = "excited expression, energetic, enthusiastic"
    else:
        duygu = "natural expression, calm, focused"
    
    # Detaylı prompt oluştur
    detayli_prompt = f"{karakter_bilgisi}, {sahne}, {ortam}, {duygu}, {stil_bilgisi}"
    
    return detayli_prompt

# Test fonksiyonu
if __name__ == "__main__":
    test_basliklar = [
        "Küçük Kedi Yavru Kurdu Kaçırıyor",
        "Cesur Köpek Uzay Macerasına Çıkıyor", 
        "Tavşan Kaybolmuş Arkadaşını Arıyor",
        "Kedi Büyük Aşkını Buluyor",
        "Köpek Kötülere Karşı Savaşıyor"
    ]
    
    for baslik in test_basliklar:
        print(f"\n{'='*80}")
        print(f"📚 HİKAYE: {baslik.upper()}")
        print('='*80)
        sahneler = ai_ile_sahneler_uret(baslik, 10)
        for i, sahne in enumerate(sahneler, 1):
            print(f"{i:2d}. {sahne}")
        print(f"\n✅ Toplam {len(sahneler)} sahne üretildi!")
        
        # Örnek prompt detaylandırma
        print(f"\n🎨 ÖRNEK PROMPT (1. sahne):")
        karakter = "cute orange cartoon tabby cat with white paws, big eyes, consistent character"
        stil = "anime style, ultra realistic lighting, cinematic composition, 4k illustration"
        detayli = prompt_detaylandir(sahneler[0], karakter, stil)
        print(f"   {detayli}")