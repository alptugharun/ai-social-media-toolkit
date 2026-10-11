# Tüm Agent Skill'ler — Sıfırdan Başla

Bu rehber repodaki **kurulabilir 19 Agent Skill'in tamamını** daha önce hiç kullanmamış biri için açıklar.

Hepsi var diye hepsini kurma.

Sıra:

1. işi tanımla;
2. en küçük uygun skill'i seç;
3. `SKILL.md` dosyasını incele;
4. mümkünse sadece o skill'i kur;
5. önce synthetic/public-safe girdi kullan;
6. beklenen sonucu ve sınırı kontrol et;
7. gerçekten gerekiyorsa ikinci skill'i ekle.

## Kurulum temeli

Listele:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Tek skill:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill SKILL-ADI
```

Hepsi:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Kurulmuş olması her host/runtime'da aynı davrandığını kanıtlamaz. Ajanın hangi path'ten yüklediğini kontrol et ve küçük bir test yap.

---

## creator-context-builder

**Nedir:** kişiselleştirilmiş creator/marka işlerinin ortak context temelidir.

**Neden:** aynı brief'i sürekli tekrar etmek tutarsızlık üretir.

**Ne zaman:** birden fazla skill aynı kimlik, kitle, kanıt, ses, platform ve onay kurallarını kullanacaksa.

**İlk talep:**  
> Güncel bilgilerim ve onaylı yazı örneklerimden ortak creator context oluştur. VERIFIED gerçekleri, PREFERENCE tercihleri, OBSERVED örüntüleri ve HYPOTHESIS yorumları ayrı tut. Eski metrikleri işaretle ve gizli bilgi saklama.

**Beklenen sonuç:** reusable creator-context dosyası + stale/recheck listesi + açık sorular + en fazla üç sonraki skill.

**Sınır:** hassas özellik çıkarımı, credential saklama ve eski metriği güncelmiş gibi sunma yok.

---

## creator-ops

**Nedir:** routing/orchestration skill'i.

**Neden:** tek dev prompt araştırma, strateji, üretim ve ölçümü aynı anda doğru yapıyormuş gibi davranmamalı.

**Ne zaman:** hedefi biliyor ama hangi skill'lerin gerektiğini bilmiyorsan.

**İlk talep:**  
> Hedefim [hedef], platform [platform], kanıt [girdi]. Minimum gerekli skill ile rotayı kur ve public yayın öncesinde dur.

**Beklenen sonuç:** hedef → kanıt → rota → kullanılabilir çıktı → review → ölçüm.

**Sınır:** external API/hesap bağlantısını kanıtlamaz.

---

## viral-content-radar

**Nedir:** trend/outlier örneklerini evidence-first şekilde söken workflow.

**Neden:** tek popüler post trend değildir; yüzey detayını kopyalamak strateji değildir.

**Ne zaman:** güncel referanslar, outlier postlar veya trend sinyalleri varsa.

**İlk talep:**  
> Bu örnekleri analiz et. Doğrulanmış kanıtı zayıf sinyalden ayır, tekrar edilebilir mekanikleri çıkar ve kaynağın özgün ifadesini kopyalamadan yeni testler öner.

**Beklenen sonuç:** evidence tablosu + mekanizma + confidence + özgün testler.

**Sınır:** tek posttan “trend kesin” demez ve virallik garantisi vermez.

---

## reels-director

**Nedir:** production-ready kısa dikey video planlayıcısı.

**Neden:** caption, Reel prodüksiyon planı değildir.

**Ne zaman:** 9:16 Reel/Short/TikTok için süreli seslendirme, sahne ve QA gerekiyorsa.

**İlk talep:**  
> Bu konuyu 30–35 saniyelik dikey videoya çevir. 0–2 saniye hook, timecode'lu voiceover, shot list, ekran metni, edit yönü ve review gate ver.

**Beklenen sonuç:** çekilebilir/kurguya verilebilir paket.

**Sınır:** erişim garantisi vermez, olmayan bilgi/görsel uydurmaz.

---

## pinterest-growth-engine

**Nedir:** search-led Pinterest cluster planlama workflow'u.

**Neden:** Pinterest büyümesi rastgele Pin sayısından değil intent, board fit, creative çeşitlilik ve destination mantığından gelir.

**Ne zaman:** doğrulanmış keyword/trend/account kanıtından Pin cluster üretmek istiyorsan.

**İlk talep:**  
> Bu doğrulanmış search intent etrafında 7 farklı Pin planla. Her birine farklı rol, görsel yön, board eşleşmesi, destination ve KPI ver.

**Beklenen sonuç:** duplicate olmayan Pin cluster.

**Sınır:** search volume uydurmaz, aynı tasarımın yedi kopyasını üretmez.

---

## pinterest-opportunity-radar

**Nedir:** Pinterest üretiminden önce “hangi fırsata girmeli?” araştırması.

**Neden:** seasonality, visual search ve query fırsatları değişir.

**Ne zaman:** cluster yapmadan önce güçlü Pinterest fırsatını seçmek istiyorsan.

**İlk talep:**  
> Bu Pinterest sinyallerini değerlendir. Verified trend/search kanıtını hipotezlerden ayır, fırsatları sırala ve her birini neyin çürüteceğini yaz.

**Beklenen sonuç:** freshness/fit/uncertainty ile evidence-ranked shortlist.

**Sınır:** search volume veya keşfet garantisi uydurmaz.

---

## content-repurposer

**Nedir:** tek güçlü kaynağı platform-native türevlere dönüştürür.

**Neden:** repurpose aynı metni her platforma kopyalamak değildir.

**Ne zaman:** bir makale/video/araştırmayı birkaç platforma uyarlayacaksan.

**İlk talep:**  
> Bu kaynağı Instagram, LinkedIn ve Pinterest'e uyarla. Gerçekleri koru; hook, yapı ve CTA'yı platforma göre değiştir. Kaynaktan gelen bilgiyle yaratıcı adaptasyonu ayır.

**Beklenen sonuç:** aynı bilgi çekirdeğinden farklı platform execution'ları.

**Sınır:** yeni gerçek uydurmaz ve mekanik duplicate üretmez.

---

## influencer-fit-auditor

**Nedir:** creator/marka kampanya uyumunu kanıtla inceleyen workflow.

**Neden:** takipçi sayısı tek başına kampanya fit değildir.

**Ne zaman:** creator/influencer iş birliğini değerlendireceksen.

**İlk talep:**  
> Bu creator'ı bu kampanya için sadece verdiğim kanıtlarla değerlendir. Fit, risk, eksik kanıt ve anlaşmadan önce cevaplanması gereken soruları ayrı yaz.

**Beklenen sonuç:** gerekçeli fit + risk + uncertainty + next questions.

**Sınır:** demografi/sonuç uydurmaz ve follower count'u yeterli kanıt saymaz.

---

## brand-voice-humanizer

**Nedir:** gerçekleri değiştirmeden generic AI hissini azaltan rewrite workflow'u.

**Neden:** AI metni fazla cilalı, tekrar eden veya şablon gibi olabilir.

**Ne zaman:** bilgi doğru ama yazı creator/marka gibi gelmiyorsa.

**İlk talep:**  
> Bunu onaylı context ve örneklerime göre Brand-Locked modda yeniden yaz. Bütün factual claim'leri koru, generic AI dokusunu temizle.

**Beklenen sonuç:** aynı gerçek payload, daha doğal ses/ritim.

**Sınır:** unsupported claim veya uydurma kişilik eklemez.

---

## signal-to-content

**Nedir:** evidence'i sınırları belli içerik deneyine çeviren köprü.

**Neden:** ilginç sinyal hemen kesin sonuca dönüşmemeli.

**Ne zaman:** araştırma/kitle/trend kanıtından test edilebilir içerik açıları istiyorsan.

**İlk talep:**  
> Bu evidence'ten üç özgün içerik deneyi çıkar. Her biri için evidence, hypothesis, execution, KPI ve stop/review condition yaz.

**Beklenen sonuç:** ölçülebilir özgün testler.

**Sınır:** hipotezi ölçülmüş gerçek gibi sunmaz, virallik garanti etmez.

---

## comment-intelligence

**Nedir:** yorumları soru, itiraz, ihtiyaç ve dil sinyallerine ayırır.

**Neden:** manuel yorum okumada tekrar eden pattern'ler kaybolur.

**Ne zaman:** kullanma hakkın olan comment sample/export varsa.

**İlk talep:**  
> Bu yorumları tekrar eden sorular, itirazlar, pain, desired outcome ve audience language olarak grupla. Sample kanıtını market-wide sonuçtan ayrı tut.

**Beklenen sonuç:** evidence-backed theme map + içerik/araştırma fırsatları.

**Sınır:** küçük sample'ı toplam pazar talebi diye sunmaz.

---

## agent-skill-safety-auditor

**Nedir:** üçüncü taraf Agent Skill'i kurmadan önce inceleme prosedürü.

**Neden:** skill shell/network/filesystem/credential davranışı isteyebilir.

**Ne zaman:** bilinmeyen bir skill'i kurmadan/reuse etmeden önce.

**İlk talep:**  
> Bu Agent Skill ve referans scriptleri kurulumdan önce denetle. Execution, network, credential, filesystem ve supply-chain risklerini somut evidence ile göster.

**Beklenen sonuç:** insan kararına yardımcı evidence-led risk bulguları.

**Sınır:** statik inceleme runtime monitoring veya güvenlik sertifikası değildir.

Deterministik offline tarama için standalone Python CLI projesini kullan.

---

## github-opportunity-radar

**Nedir:** GitHub demand/supply proxy ve gap araştırması.

**Neden:** “az repo var” = “kullanıcı istiyor” değildir.

**Ne zaman:** yeni skill/repo/tool yapmaya değer mi diye karar verirken.

**İlk talep:**  
> Bu GitHub fikirlerini güncel repo/search/activity proxy'leriyle karşılaştır. Proxy'leri gerçek talep gibi sunma, en yakın rakipleri incele, 7 günlük proof ve stop condition ver.

**Beklenen sonuç:** overlap + evidence sınırı + validation planıyla sıralama.

**Sınır:** result count search volume değildir; skor star tahmini değildir.

---

## plugin-mcp-architect

**Nedir:** prompt → assistant → Agent Skill → MCP → plugin → automation mimari karar workflow'u.

**Neden:** birçok proje ihtiyacından daha güçlü/karmaşık katmana sıçrar.

**Ne zaman:** hangi AI integration layer'ı gerektiğini seçerken.

**İlk talep:**  
> Bu işi prompt, assistant, Agent Skill, MCP, plugin veya automation arasından en küçük uygun katmana eşleştir. Yetki, test ve paketlemeyi açıkla; bir üst katmanın neden gereksiz olduğunu da yaz.

**Beklenen sonuç:** mimari karar + sınır + implementation/test planı.

**Sınır:** external registry/deployment işlemini kendi başına yapmış sayılmaz.

---

## maps-opportunity-radar

**Nedir:** Maps/Places/local intelligence ürün/workflow fırsatı araştırması.

**Neden:** generic place-search wrapper yapmak kolay ama çoğu zaman farklılaşmaz.

**Ne zaman:** local/geospatial AI fikri araştırırken.

**İlk talep:**  
> Bu Maps/local intelligence fikirlerini değerlendir. Generic wrapper'ları ele, mevcut çözümleri karşılaştır, higher-level workflow gap bul ve 7 günlük proof tasarla.

**Beklenen sonuç:** differentiation + feasibility + evidence-ranked opportunities.

**Sınır:** restricted scraping önermez, result count'u demand diye sunmaz.

---

## maps-policy-guard

**Nedir:** Maps/Places/Street View veri workflow'ları için policy/architecture review.

**Neden:** scraping, storage, cache, attribution ve screenshot kullanımı policy riskine girebilir.

**Ne zaman:** Maps verisi/media toplayacak, saklayacak, export/reuse edecek sistem tasarlarken.

**İlk talep:**  
> Bu Maps workflow'unu uygulamadan önce authorization, scraping, storage, retention, attribution ve screenshot/media riskleri açısından incele; daha güvenli mimari öner.

**Beklenen sonuç:** policy risk map + BLOCK/REVISE noktaları + safer design.

**Sınır:** legal advice değildir ve platform izni uydurmaz.

---

## local-business-intelligence

**Nedir:** owned/authorized local business sinyalini market/content/creator içgörüsüne çevirir.

**Neden:** local review/FAQ/location verisi ancak kaynak ve inference sınırı netse güvenilir kullanılır.

**Ne zaman:** yetkili/owned local veriden fırsat çıkarmak istiyorsan.

**İlk talep:**  
> Bu yetkili local-business sinyallerini kullan. Source observation ile inference'ı ayır, içerik/market fırsatlarını çıkar ve hangi ek kanıta ihtiyacımız olduğunu yaz.

**Beklenen sonuç:** source-backed local insight + eylem planı.

**Sınır:** private analytics uydurmaz, restricted scraping yapmaz, hassas trait çıkarmaz.

---

## commercial-opportunity-radar

**Nedir:** ürün/hizmet/gelir fikirlerini validation-first karşılaştırır.

**Neden:** teknik novelty buyer demand değildir.

**Ne zaman:** birkaç para kazanma fikrinden hangisini test edeceğine karar verirken.

**İlk talep:**  
> Bu üç ticari fikri buyer clarity, pain frequency, proof, recurring need, distribution ve implementation cost açısından karşılaştır. Minimum 7 günlük validation ve stop condition ver.

**Beklenen sonuç:** commercial hypothesis sıralaması + proof planı.

**Sınır:** buyer, willingness-to-pay, conversion veya gelir uydurmaz.

---

## monetization-architect

**Nedir:** kanıtlanmış değerin staged monetization tasarımı.

**Neden:** real demand görmeden direkt SaaS/fiyatlandırmaya sıçramak kaynak yakabilir.

**Ne zaman:** workflow/product için gerçek kullanım sinyali oluştuysa.

**İlk talep:**  
> Bu kanıtlanmış workflow etrafında en küçük paid test'i tasarla. Free artifact faydalı kalsın; implementation service → recurring product → hosted product geçişini evidence gate'lerine bağla.

**Beklenen sonuç:** açık kaynak kanıt → service → recurring/productized → hosted yol haritası.

**Sınır:** fiyat belirlemez, gelir sözü vermez, star/clone'u ödeme talebi saymaz.

---

# Hızlı seçim

| İş | İlk skill |
| --- | --- |
| Aynı brief'i tekrar etmekten kurtul | `creator-context-builder` |
| Hangi workflow lazım bilmiyorsun | `creator-ops` |
| Trend/outlier mekanizması bul | `viral-content-radar` |
| Kısa video prodüksiyon paketi | `reels-director` |
| Pinterest cluster oluştur | `pinterest-growth-engine` |
| Önce Pinterest fırsatını seç | `pinterest-opportunity-radar` |
| Tek kaynağı platformlara uyarla | `content-repurposer` |
| Creator/marka fit incele | `influencer-fit-auditor` |
| Robot gibi AI metnini düzelt | `brand-voice-humanizer` |
| Evidence'i içerik testine çevir | `signal-to-content` |
| Yorumlardan insight çıkar | `comment-intelligence` |
| Üçüncü taraf skill'i denetle | `agent-skill-safety-auditor` |
| GitHub opportunity/gap bul | `github-opportunity-radar` |
| Prompt vs skill vs MCP seç | `plugin-mcp-architect` |
| Maps/local gap araştır | `maps-opportunity-radar` |
| Maps policy riskini incele | `maps-policy-guard` |
| Yetkili local business sinyalini analiz et | `local-business-intelligence` |
| Neyi satmaya değer test et | `commercial-opportunity-radar` |
| Kanıttan sonra paid path tasarla | `monetization-architect` |

## Son kural

**Tek iş → tek ilk skill → tek doğrulanabilir sonuç.**

Gerçek ihtiyaç çıkmadan karmaşıklık ekleme.
