import fitz  # PyMuPDF

def metin_oku(dosya_yolu):
    """
    Verilen PDF dosya yolundan metni okur ve metni bir string olarak döner.
    """
    try:
        doc = fitz.open(dosya_yolu)
        metin = ""
        for sayfa in doc:
            metin += sayfa.get_text()
        return metin
    except Exception as e:
        return f"Bir hata oluştu: {e}"

