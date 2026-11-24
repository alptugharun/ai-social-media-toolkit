# Agent Plugin ZIP: ilk güvenli sonuç

[English](PLUGIN-QUICKSTART.md) | [Brand Voice Humanizer talimatları](skills/brand-voice-humanizer/SKILL.md)

## Bu paket ne işe yarar?
Çıkardığınız ZIP, içerik üretimi için tekrar kullanılabilir talimatlar barındıran **yalnızca Agent Skills içeren** bir eklentidir. Barındırılan bir yapay zekâ servisi, sosyal medya hesabı bağlantısı veya otomatik yayın aracı değildir. Uyumlu bir ajan ortamında kullanılır. Tek seferlik prompt veya çalışan bir MCP sunucusu arıyorsanız bu paket doğru başlangıç değildir.

## Gerekenler ve maliyet
İlgili eklenti veya Agent Skills biçimini destekleyen bir ajan ortamı gerekir. Kurulum yöntemi ortama göre değişir. Ortamın resmi yükleme talimatlarını izleyin ve `skills/brand-voice-humanizer/SKILL.md` dosyasını gördüğünü kontrol edin. ZIP içeriğini okumak ücretsizdir; API anahtarı gerekmez. Ajan ortamı ayrı hesap veya ücret gerektirebilir. Bu örnek için hesap erişimi, yayınlama, ağ veya geniş dosya yazma izni vermeyin.

## İlk işlem
ZIP'i çıkarın. [Skill talimatlarını](skills/brand-voice-humanizer/SKILL.md) okuyun. Paketi uyumlu ortamınıza ekleyin veya ortamın belgelerine göre bu skill'i yükleyin. Harici hesap bağlantılarını kapalı tutun. Metnin değiştirilmemesi için **Audit** modunu kullanın.

### Güvenli örnek ilk istek

```text
Brand Voice Humanizer'ı Audit modunda kullan. Bu tamamen hayalî bir örnektir:
"Hayalî atölye 10 Mart 2027 tarihinde saat 18:00'de başlıyor. Bilet 120 TL."
Daha doğal ve anlaşılır anlatım için öneriler sun. Metni yeniden yazma,
tarihi veya sayıları değiştirme, yayınlama yapma, etkinliği gerçek gösterme.
Gözlemlerini ve olası olgusal riskleri belirt.
```

## Beklenen çıktı ve kontrol
Üslup ve açıklık hakkında gözlemler, gerekiyorsa olgusal risk uyarıları beklenir. Yanıtı örnek metinle karşılaştırın. **10 Mart 2027**, **18:00** ve **120 TL** bilgilerinin korunmasını, herhangi bir hesap işlemine girişilmemesini denetleyin. Gerçek ajan ortamında yükleme ve çıktı ayrıca test edilmelidir. ZIP testleri model davranışını kanıtlamaz.

## Sınırlar ve sık hatalar
Talimatlar etkinliğin gerçekliğini veya metnin doğruluğunu doğrulamaz. İsteğe bağlı Rewrite Fact Guard, seçili sayısal ifadeleri ve korunan metinleri karşılaştırır; **anlamsal doğrulama yapmaz** ve ayrı Python betiği için uygun Python ortamı ister. [Detaylı Türkçe rehber](skills/brand-voice-humanizer/README_TR.md). Skill görünmüyorsa ZIP içindeki `skills/` dizinini ve ortamın yükleme kurallarını inceleyin. Audit modu yüklenmiyorsa yükleme başarısı iddia etmeyin. Korunan bilgi değişirse sonucu **FAIL** olarak işaretleyip yeniden değerlendirin.

## Gizlilik, yetkiler ve yardım
Örnek otomatik yayın, hesap girişi, uzaktan veri toplama veya ek izin istemez. Önce uydurma verilerle deneyin. Onaylamadığınız ortama parola, anahtar veya gizli müşteri verisi aktarmayın. Gizli bilgi içermeyen yeniden üretim adımlarını [GitHub sorun kaydında](https://github.com/alptugharun/ai-social-media-toolkit/issues) paylaşın; hassas açıklar için deponun güvenlik politikasını kullanın. Ortam/sürüm, beklenen ve gözlenen sonuç ile PASS, FAIL veya BLOCKED durumunu belirtin.
