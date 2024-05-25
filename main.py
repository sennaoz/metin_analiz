import metin_okuyucu
import metin_arama
import metin_analizi
import benzerlik_analizi
import istatistik_analizi

dosya_yolu1 = 'ornek1.pdf'
dosya_yolu2 = 'ornek2.pdf'
aranacak_kelime = input("Aranacak Kelime Giriniz: ")

# İlk PDF dosyasından metni oku
metin1 = metin_okuyucu.metin_oku(dosya_yolu1)

# İkinci PDF dosyasından metni oku
metin2 = metin_okuyucu.metin_oku(dosya_yolu2)

# Eğer dosyalar başarıyla okunmuşsa
if "Bir hata oluştu" not in metin1 and "Bir hata oluştu" not in metin2:
    # Metin içinde kelime ara
    pozisyonlar1 = metin_arama.kelime_ara(metin1, aranacak_kelime)
    pozisyonlar2 = metin_arama.kelime_ara(metin2, aranacak_kelime)

    if pozisyonlar1:
        print(f'"{aranacak_kelime}" kelimesi birinci metin içinde şu pozisyonlarda bulundu: {pozisyonlar1}')
    else:
        print(f'"{aranacak_kelime}" kelimesi birinci metin içinde bulunamadı.')

    if pozisyonlar2:
        print(f'"{aranacak_kelime}" kelimesi ikinci metin içinde şu pozisyonlarda bulundu: {pozisyonlar2}')
    else:
        print(f'"{aranacak_kelime}" kelimesi ikinci metin içinde bulunamadı.')

    # Metin analizi yaparak önemli kelimeleri çıkar
    onemli_kelimeler1 = metin_analizi.onemli_kelimeleri_cikar(metin1, n=10)
    onemli_kelimeler2 = metin_analizi.onemli_kelimeleri_cikar(metin2, n=10)
    print(f'Birinci metindeki önemli kelimeler: {onemli_kelimeler1}')
    print(f'İkinci metindeki önemli kelimeler: {onemli_kelimeler2}')

    # Metinler arasındaki benzerlik derecesini hesapla
    benzerlik_derecesi = benzerlik_analizi.metin_benzerligi(metin1, metin2)
    print(f'İki metin arasındaki benzerlik derecesi: {benzerlik_derecesi}')

    # Metin istatistiklerini çıkar
    istatistikler1 = istatistik_analizi.metin_istatistikleri(metin1)
    istatistikler2 = istatistik_analizi.metin_istatistikleri(metin2)
    print(f'Birinci metin istatistikleri: {istatistikler1}')
    print(f'İkinci metin istatistikleri: {istatistikler2}')
else:
    print(f'Bir hata oluştu: {metin1 if "Bir hata oluştu" in metin1 else metin2}')
