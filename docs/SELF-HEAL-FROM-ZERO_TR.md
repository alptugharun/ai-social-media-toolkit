# Self-Heal Guardian: güvenli ilk sonuç

[English](SELF-HEAL-FROM-ZERO.md) · [Kaynak](../tools/self_heal.py) · [İş akışı](../.github/workflows/self-heal.yml)

## Nedir, kimler için?

Bu yerel yardımcı, başarısız GitHub Actions günlüklerini sınıflandırarak JSON tanı ve Markdown olay özeti üretir. Bakım sorumlusunun **sınırlı** yeniden denemenin güvenli olup olmadığını değerlendirmesine yardımcı olur. Otomatik kod onarımı, GitHub API kotası sıfırlama aracı, güvenlik açığı tarayıcısı veya hatanın giderileceğinin kanıtı değildir. İzinlerini incelemeden başka hesaba iş akışı yüklemek isteyenler için değildir.

**Gereksinim / maliyet:** Python 3.11+ ve yardımcıyı/örneği içeren depo kopyası. Bu örnekte API anahtarı, ağ isteği, ücretli API veya GitHub yazma izni gerekmez. Yalnızca belirttiğiniz iki yerel dosya oluşturulur.

## İlk işlem: sentetik HTTP 429

Depo ana dizininden:

```bash
python tools/self_heal.py --log examples/self-heal-429.log --workflow "GitHub Opportunity Radar" --run-id demo-429 --json-output self-heal-demo.json --markdown-output self-heal-demo.md
```

`self-heal-demo.json` dosyasını açın. Beklenen değerler: `classification: "http-rate-limit"`, `retryable: false`, `probe_retry_safe: false` ve 12 karakterli parmak izi. `self-heal-demo.md` olay özetini ve sınırları göstermeli. Bağımsız regresyon kontrolü:

```bash
python -m unittest tests.test_self_heal -v
```

Testler GitHub'a özgü ve genel HTTP 429, 403 ve 503 hataları dahil sentetik veriler kullanır. Başarılı test gerçek GitHub hız sınırının aşıldığını veya gerçek çalıştırıcı davranışını kanıtlamaz. Geçmiş sürüm ZIP dosyalarının bu yeni politikayı içerdiği varsayılamaz.

## Sorun giderme ve veri güvenliği

Python yoksa desteklenen yerel sürümü yükleyin; dosya bulunamıyorsa komutu depo ana dizininden çalıştırın; çıktı yazılamıyorsa yazılabilir bir yerel yol seçin. `HTTP 429` durup inceleme gerektirir; sınıflandırıcı reset sayısından otomatik yeniden deneme planlamaz. Bağımsız 503 hataları mevcut sınırlı yeniden deneme politikası kapsamında uygun kalabilir. Genel 403, yetki sorunu ile hız sınırı güvenli şekilde ayırt edilemediği için yeniden denenmez.

Herkese açık issue'larda yalnızca sentetik veya bilinçli şekilde temizlenmiş günlükler kullanın. Gerçek günlüklerde erişim anahtarları, özel adresler ve kişisel bilgiler bulunabilir; bunları herkese açık paylaşmayın. Sınıflandırıcı **kapsamlı gizli veri temizleyici değildir**. GitHub kurallarını zorunlu kılamaz veya gerçek çalıştırıcı ortamını bağımsız olarak doğrulayamaz. Hassas bulgular için [özel bildirim](../SECURITY.md), hassas olmayan tekrar üretilebilir hatalar için [GitHub issues](https://github.com/alptugharun/ai-social-media-toolkit/issues) kullanın. İşlem sonunda `self-heal-demo.json` ve `self-heal-demo.md` dosyalarını silin.
