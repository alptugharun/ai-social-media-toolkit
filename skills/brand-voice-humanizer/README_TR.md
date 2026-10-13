# Brand Voice Humanizer + Rewrite Fact Guard

[English](README.md) · [Skill talimatı](SKILL.md)

**Metin daha doğal oldu. Peki fiyat veya teslim tarihi değişti mi?**

Mevcut skill'in iki parçası var: yapay zekâya yazıyı nasıl düzenleyeceğini anlatan talimat ve iki metni bilgisayarında karşılaştıran küçük bir Python programı. Program bir **metinsel değişiklik kontrolüdür**; metnin doğru olduğunu veya insan tarafından yazıldığını kanıtlamaz.

## Hangisi ne işe yarar?

Metni kendi üslubuna yaklaştırmak için skill'i kullan. Metin değişmeden yalnızca somut eleştiri almak için Audit modunu seç. Elinde özgün metin ve düzenlenmiş sürümü varsa Rewrite Fact Guard ile sayısal ifadelerde, bağlantılarda ve özellikle korumak istediğin cümlelerde değişiklik arayabilirsin.

Program metin yazmaz, AI modeline bağlanmaz, sosyal hesap açmaz ve paylaşım yapmaz. Python bölümünü kullanmak için API anahtarı veya ücretli model gerekmez. Skill talimatını bir AI uygulamasında çalıştırmak ise o uygulamanın ücret ve veri işleme koşullarına bağlıdır.

## Terminal bilmeden başla

1. [SKILL.md](SKILL.md) içindeki süreci kullandığın yetkili AI ortamında uygula.
2. Düzenlenecek metni ver ve modu seç: Audit, Light, Editorial, Spoken veya Brand-Locked.
3. Değişmemesi gereken isim, fiyat, tarih ve sınırlamaları belirt.
4. Düzenlenmiş metni ve önemli değişiklikleri iste. Audit modunda yalnızca bulgular iste.
5. Paylaşmadan önce iki sürümü de oku. Burada hiçbir içerik otomatik yayımlanmaz.

Örnek istek: “Bu açıklamayı Light modunda düzenle. Türkçe ifadelerimi ve mizahımı koru. Fiyatı, teslim süresini ve ‘garanti değildir’ ifadesini değiştirme. Nelerin değiştiğini söyle.”

Üslup kalitesini kendi onaylı örneklerinle değerlendir. Aşağıdaki program bunun yalnızca küçük, mekanik bir kısmını kontrol eder.

## Python programını sıfırdan dene

Depoyu indir veya klonla. Terminali **ai-social-media-toolkit klasörünün içinde** aç. `python --version` ile Python 3.10 veya üzerini doğrula. `pip install` gerekmez. Windows'ta sisteminde tanımlıysa `python` yerine `py -3` kullanabilirsin.

Önce yapay örnek dosyalarını dene. Dosyalardaki fiyat ve süre gerçek bir hizmet teklifi değildir:

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-good.txt --lock "garanti değildir"
```

Beklenen sonuç: `NO_TRACKED_CHANGE`, sıfır değişiklik ve **0** çıkış kodu. Ayrıca kontrolün sınırlaması yazılır. Yalnızca izlenen ifadelerin korunmuş olduğu anlaşılır; metnin bütün anlamının doğru olduğu değil.

Şimdi fiyatı ve süreyi bilerek değiştirilmiş örneği dene:

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-review.txt --lock "garanti değildir" --format json --show-values
```

Beklenen sonuç: `REVIEW_REQUIRED`, **7 bulgu**, **1** çıkış kodu. Silinen ve eklenen ifadeler ayrı sayılır: fiyat için iki, süre için iki, bağlantı için iki bulgu ve kaybolan korumalı ifade. Değerleri açık gösteriyoruz çünkü örnek dosyalar yapaydır.

PowerShell'de hemen ardından `$LASTEXITCODE` ile kodu görebilirsin. **1**, gözden geçirilecek değişiklik bulundu demektir; uygulama çöktü demek değildir. **2**, girdi veya ayar hatasıdır. Bir AI ajanı 1 görünce aynı işlemi durmadan tekrar etmemeli veya metni otomatik onaylamamalıdır.

## Kendi metnini kullan

Özgün metni ve düzenlenmiş sürümünü ayrı UTF-8 `.txt` dosyalarına kaydet. Komuttaki dosya yollarını değiştir. Korumak istediğin, özgün metinde zaten bulunan isim, alıntı veya uyarıyı `--lock` ile ver. Birden fazla ifade için seçeneği tekrarlayabilirsin.

Özgün metinde bulunmayan bir ifadeyi kilitlersen program hata verir. Yanlış yazılmış bir koruma kuralını sessizce başarılı saymaz. Kilitler büyük/küçük harfe duyarlıdır; karşılaştırmadan önce Unicode NFC normalizasyonu yapılır.

Varsayılan rapor bulguların açık değerlerini göstermez. Özel müşteri metinleri veya CI kayıtlarında `--show-values` kullanma. Şifre ve anahtarları metne ya da `--lock` argümanına koyma; terminal geçmişi argümanları kaydedebilir. Program kaynakları değiştirmez. Kendin eklersen `> rapor.json` yönlendirmesi dosyayı terminalin aracılığıyla yazar.

## Sınırları bil

Program sayısal ifadeleri, sınırlı sayıdaki yaygın birimi, URL'leri ve seçtiğin ifadelerin kaç kez geçtiğini karşılaştırır. `1.500` ile `1,500` değerlerini otomatik aynı kabul etmez. Yazıyla yazılmış sayıları, tüm Türkçe çekimleri ve anlam ilişkilerini çözmez. Bağlantıyı açıp içeriğini doğrulamaz.

Önemli kör nokta: “A: 25, B: 50” ifadesi “A: 50, B: 25” olursa aynı sayılar metinde kaldığı için değişiklik saptanmayabilir. Gerekirse tüm cümleyi korumaya al; yine de anlamı insan olarak kontrol et. Kilitlenmemiş bir “olabilir” ifadesinin “olacaktır” yapılması da gözden kaçabilir.

Sonuç bir güvenlik sertifikası, AI tespit yüzdesi, hukuki değerlendirme veya yayın onayı değildir. Değişmemiş bir yanlış bilgi hâlâ yanlış olabilir.

## Sık sorunlar

**Kilit bulunamadı:** İfadeyi özgün metinden tam olarak kopyala. Kontrol yeşil olsun diye gerekli bir uyarıyı korumadan çıkarma.

**UTF-8 hatası:** Dosyayı UTF-8 olarak kaydet. UTF-8 BOM desteklenir.

**Dosya büyük:** Her girdi en fazla 256 KiB olabilir. Anlam bağını koparmadan bölümler hâlinde karşılaştır.

**Dosya yok:** Terminalin doğru klasörde olduğunu ve dosya yolunu kontrol et. Klasörler ve sembolik bağlantılar girdi olarak kabul edilmez.

**Hiç bulgu yok:** Sayı veya korunan ifade içermeyen metinde mekanik kontrolün takip edeceği pek bir şey olmayabilir. İki metni de oku.

## Test ve yardım

Depo kökünde:

```bash
python -m unittest discover -s tests -p test_rewrite_fact_guard.py -v
```

Testler yapay girdilerle metinsel karşılaştırmayı, hatalı girdileri, komut satırını ve bilinen kör noktaları sınar. Bir AI modelinin güzel yazdığını veya tüm metinlerde hata yapmayacağını kanıtlamaz.

Sorunu özel veri içermeyen küçük bir örnekle [GitHub Issues](https://github.com/alptugharun/ai-social-media-toolkit/issues/new/choose) üzerinden bildir. Özel müşteri metni, şifre veya oturum bilgisi gönderme. Hassas güvenlik açıkları için deponun özel güvenlik bildirim yolunu kullan.
