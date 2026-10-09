# Creator Frame Studio

**İçerik üreticileri için tarayıcıda çalışan kadraj, iç alan kontrolü ve çoklu format dışa aktarma çalışma alanı.**

[⚡ Canlı demoyu aç](https://alptugharun.github.io/ai-social-media-toolkit/) · [English README](README.md) · [Yol haritası](ROADMAP.md) · [Test notları](TESTING.md) · [İçerik paketi](CONTENT-PACK.md)

> **Durum:** v0.3.0 beta. Araç kullanılabilir durumdadır; fakat resmî Instagram doğrulayıcısı veya “AI tasarım hakemi” olarak sunulmaz.

## Hangi sorunu çözüyor?

Bir tasarım editörde güzel görünüp başka bir yüzeye uyarlandığında başlık, yüz veya CTA etkisini kaybedebilir. Creator Frame Studio tek bir yerel çalışma alanında şunları yapar:

- kaynak görseli yeniden üretmeden yerleştirme ve kadrajlama,
- farklı sosyal medya tuvalleri arasında önizleme,
- düzenlenebilir metin katmanları,
- ihtiyatlı iç alan kılavuzları,
- yaygın kırpma görünümlerinin simülasyonu,
- tek dosya veya çoklu format ZIP çıktısı,
- projeyi dosya olarak kaydetme ve yeniden açma.

## Hazır tuvalller

| Platform | Biçim | Tuval |
| --- | --- | ---: |
| Instagram | Portre / carousel | 1080 × 1350 · 4:5 |
| Instagram | Uzun portre | 1080 × 1440 · 3:4 |
| Instagram | Kare | 1080 × 1080 · 1:1 |
| Instagram | Yatay | 1080 × 566 · ≈1.91:1 |
| Instagram | Hikâye | 1080 × 1920 · 9:16 |
| Instagram | Reels kapak tuvali | 1080 × 1920 · 9:16 |
| Instagram | Profil / Öne Çıkan çalışma tuvali | 1080 × 1080 + daire önizlemesi |
| Pinterest | Standart Pin | 1000 × 1500 · 2:3 |
| YouTube | Video thumbnail | 3840 × 2160 · 16:9 |
| YouTube | Shorts thumbnail tuvali | 2160 × 3840 · 9:16 |
| YouTube | Hafif thumbnail tuvali | 1280 × 720 · 16:9 |
| Her yer | Özel ölçü | Araç sınırları içinde 64–4096 px / kenar |

Bunlar **çalışma tuvalleri**dir. Her paylaşım yolunun her oranı kabul ettiği iddia edilmez; platform arayüzleri ve kırpmaları değişebilir.

## Yerelde çalıştır

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit/tools/creator-frame-studio
```

Sonra `index.html` dosyasını modern bir tarayıcıda aç. API anahtarı veya hesap girişi gerekmez.

## Gizlilik yaklaşımı

- model/API çağrısı yok,
- sosyal hesap girişi yok,
- analytics isteği yok,
- dosya yükleme sunucusu yok,
- kaynak görseli yeniden üretme yok.

Sayfanın Content Security Policy ayarı ağ bağlantılarını engeller. Proje ve çıktı dosyaları tarayıcı içinde oluşturulur.

## Mevcut sınırlar

- Kılavuzlar editöryal/ihtiyatlı öneridir; **evrensel resmî güvenli alan değildir**.
- Yüklenmiş görselin içine gömülü yazılar otomatik algılanmaz veya taşınmaz.
- OCR, yüz algılama, estetik puanı, viral puanı veya otomatik paylaşım yoktur.
- Story/Reels arayüz katmanları temsili simülasyondur; son kontrol gerçek yayın ekranında yapılmalıdır.
- Çoklu format paketi kompozisyonu yeniden kadrajlar; her çıktı gözle kontrol edilmelidir.

**Alptuğ Harun** tarafından geliştiriliyor.

## v0.3 creator iş akışı geliştirmesi

v0.3 sürümünde Hook / Alt başlık / CTA hızlı metin stilleri, Dengeli / Hook odaklı / CTA odaklı editöryal kılavuz profilleri ve deterministik yayın öncesi durum kartı eklendi. Bunlar estetik kalite, yüz, görsele gömülü metin veya algoritmik performans puanı üretmez.
