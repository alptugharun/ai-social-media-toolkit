# İndirdin. Şimdi ilk sonucunu al.

Bu paket ChatGPT, Claude, Grok ve Gemini için kullanılabilen talimatlar, örnekler ve bir API başlangıç aracı içerir. Dosya indirmek hesabında GPT, bot veya eklenti oluşturmaz. Kurulum ve deneme yolları aşağıda ayrıdır.

## 1. Kodsuz başlangıç

ZIP paketini klasöre çıkart. `ai-workbench/index.html` dosyasını tarayıcıda aç; `browser-template.html` dosyasını değil. Sayfanın dilini Türkçe yap ve Araştırma kategorisini seç. İlk kartta **Talimat ve örnek** bölümünü aç.

GitHub kaynak ZIP'inde oluşturulmuş index.html yoksa ana klasörde `python tools/build_workbench_browser.py` komutunu çalıştır; ardından oluşan sayfayı aç. Sohbette verilen standalone paket ise oluşturulmuş sayfayı içerir. GitHub'ın HTML dosyası görüntüleyicisi uygulamayı çalıştırmaz.

Kartta dört parça görürsün: davranış talimatı, örnek girdi, temsilî çıktı ve kabul kontrolü. **Talimatı kopyala** düğmesine bas. Kullandığın AI ürününde yeni bir sohbet aç, talimatı gönder, ardından ayrı mesaj olarak şunu ver:

```text
Kaynak A: Geçen ay medyan yanıt süresi 12 saatti.
Kaynak B: Bu ay medyan yanıt süresi 8 saatti.
Memnuniyet araştırması yok.
Soru: Yanıt hızı ve müşteri memnuniyeti iyileşti mi?
```

İyi yanıt hızın arttığını A ve B'ye bağlar; memnuniyet verisi olmadığı için memnuniyet artışı ilan etmez. Sayılar değişirse veya memnuniyet uydurulursa test geçmez. Akıcı bir cümle doğruluğun kanıtı değildir.

Kopyalama engellenirse talimat bloğunu elle seçip kopyala. Kurumsal tarayıcı kısıtlarını aşma; Markdown içeriğini veya izin verilen arayüzü kullan.

## 2. GPT, Claude, Grok, Gem veya skill dosyası al

Üstteki dışa aktarma alanından hedefi seç ve kartta **Kurulum dosyasını indir** düğmesine bas. GPT, Claude, Grok ve Gemini seçimleri Markdown kurulum taslaklarıdır. Agent Skill seçimi `SKILL.md` üretir.

Birden fazla skill indiriyorsan her birini kendi klasöründe tut: `evidence-desk/SKILL.md` gibi. Dosyayı oku; kullandığın agent'ın desteklediği kurulum yolunu izle. Bütün ortamlarda çalıştığı iddia edilmiyor. [Ürüne göre adımlar](ASSISTANTS.md).

## 3. Terminalle kullanım

Terminali `tools`, `tests` ve `ai-workbench` klasörlerinin bulunduğu ana klasörde aç. Windows'ta çalışan Python kurulumuna göre `py -3` veya `python`; macOS/Linux'ta genellikle `python3` kullanılır. Python 3.10 veya üstü gerekir.

```powershell
py -3 --version
py -3 tools/ai_workbench.py list
py -3 tools/ai_workbench.py export evidence-desk --target gpt --lang tr
```

PowerShell'de dosyayı UTF-8 kaydetmek için:

```powershell
py -3 tools/ai_workbench.py export voice-editor --target claude --lang tr | Set-Content -Encoding utf8 voice-editor-claude.md
```

macOS/Linux karşılığı:

```bash
python3 tools/ai_workbench.py export voice-editor --target claude --lang tr > voice-editor-claude.md
```

## 4. Kartları doğru görevle eşleştir

**Evidence Desk:** Kaynaklarını A/B/C diye ayır, tek araştırma sorusu sor. Kanıt yoksa sonuç uydurmamalı.

**Voice Editor:** Onayladığın üslup örneklerini ve taslağı birlikte ver. Düzeltilmiş metin yeni deneyim, başarı veya müşteri sonucu eklememeli.

**Study Companion:** Seviyeni ve öğrenmek istediğin tek kavramı yaz. Alıştırmayı cevap anahtarına bakmadan çöz.

**Debug Brief:** Hata metnini, küçük bir örnek girdiyi ve beklenen davranışı ver. Kod çalıştırılmadıysa önerilen neden bir hipotezdir.

**Workflow Designer:** Tek tetikleyici, tek kaynak ve tek çıktı seç. Onay, tekrar önleme ve hata davranışı tamam olmadan dış hesaba bağlama.

**Prompt Repair:** Kötü sonuç aldığın talimatı ve iyi çıktının nasıl görünmesi gerektiğini ver. Normal girdi, eksik bilgi ve kaynak içine gizlenmiş yanıltıcı talimatla üç deneme yap.

**Decision Notebook:** Zorunlu koşulları önce yaz. Daha yüksek puan uğruna zorunlu koşulu yok sayan sonuç geçmez.

**Knowledge Map:** Notları kaynak kimliğiyle ayır. Çelişkileri sildirme; işaretlet. Harita oluşturmak çalışan RAG servisi kurmak değildir.

## 5. API çağrısından önce önizleme

```powershell
py -3 tools/ai_workbench.py request evidence-desk --provider xai --model MODEL_ID --input ai-workbench/sample-input.txt --lang tr
```

Çıktıda `OFFLINE_PREVIEW` ve `network_called: false` görmelisin. Bu bir AI cevabı değil, gönderilmek üzere hazırlanmış istektir. İçinde girdinin metni bulunur; özel bilgi içeriyorsa paylaşma. Canlı çağrı adımları, ücret ve anahtar yönetimi [bot rehberinde](BOT-AND-AUTOMATION.md).

## 6. Bir şey çalışmıyorsa

| Belirti | Ne kontrol edilir? |
| --- | --- |
| `can't open file` | Terminal tools klasörünün bulunduğu ana klasörde mi? |
| `Unknown card ID` | list çıktısındaki küçük harfli kimlik kullanılıyor mu? |
| HTML boş | Oluşturulmuş index.html yerine şablon mu açıldı? |
| Genel veya yanlış çıktı | Hedef, kaynak, örnek ve kabul koşulu birlikte verildi mi? |
| API 401/403/429 | Anahtar, model erişimi, kota ve ücret durumu uygun mu? Körlemesine tekrar çağırma. |
| Yanıt kesilmiş | Çıktı sınırı ve tamamlanma durumu kontrol edildi mi? Kısmi yanıtı tamamlanmış sayma. |

İlk hedef bütün kartları çalıştırmak değil; tek bir işi, girdisini ve sonucu nasıl kontrol edeceğini öğrenmektir.
