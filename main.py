import metin_okuyucu
import metin_arama

dosya_yolu = 'ornek.txt'
aranacak_kelime = input("Aranacak kelimeyi giriniz: ")

# Dosyadan metni oku
metin = metin_okuyucu.metin_oku(dosya_yolu)

# Eğer dosya başarıyla okunmuşsa
if "Bir hata oluştu" not in metin and "Dosya bulunamadı" not in metin:
    # Metin içinde kelime ara
    pozisyonlar = metin_arama.kelime_ara(metin, aranacak_kelime)

    if pozisyonlar:
        print(f'"{aranacak_kelime}" kelimesi metin içinde şu pozisyonlarda bulundu: {pozisyonlar}')
    else:
        print(f'"{aranacak_kelime}" kelimesi metin içinde bulunamadı.')
else:
    print(metin)
