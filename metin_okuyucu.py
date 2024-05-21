def metin_oku(dosya_yolu):
    """
    Verilen dosya yolundan metni okur ve metni bir string olarak döner.
    """
    try:
        # Encoding kısmı tr karakter girdisi almasını sağlar
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            metin = dosya.read()
        return metin
    except FileNotFoundError:
        return "Dosya bulunamadı."
    except Exception as e:
        return f"Bir hata oluştu: {e}"
