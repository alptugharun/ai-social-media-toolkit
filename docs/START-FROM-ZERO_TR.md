# Sıfırdan Başla — Buradaki Her Şey Nedir, Neden Var ve Nasıl Kullanılır?

Bu rehber GitHub profilini açıp şunu düşünen kişi için:

> “Güzel görünüyor ama Agent Skill ne, MCP ne, blueprint ne, hangisine tıklayacağım hiçbir fikrim yok.”

Bütün repoyu anlaman gerekmiyor.

Ana kural:

**tek bir iş seç → o işi çözen en küçük katmanı kullan → çalışan bir sonuç al → ancak gerekiyorsa sistemi büyüt.**

---

## 1. 60 saniyelik sözlük

| Şey | Basit anlatımı | Ne zaman kullanılır? | Ne zaman gerekmez? |
| --- | --- | --- | --- |
| **Prompt** | Tekrar kullanılabilir talimat | bir AI işi için yapı ve kalite kontrol gerekiyorsa | hesap/araç işlemi gerekiyorsa |
| **Assistant Blueprint** | Tekrar kullanılabilir AI rolü/ayar paketi | aynı iş farklı oturum/provider'da tekrarlanıyorsa | tek prompt yeterliyse |
| **Agent Skill** | AI ajanının yükleyebildiği iş prosedürü | bir workflow ajan içinde tekrar kullanılacaksa | skill'i/runtime'ı incelemediysen |
| **MCP Server** | AI hostuna şemalı araçlar sunan program | AI'ın çağırabileceği gerçek araçlar gerekiyorsa | metin talimatı işi çözüyorsa |
| **Automation** | daha sonra/tekrar/şart olunca çalışan görev | manuel süreç kanıtlanmış ve tekrar ediyorsa | süreç daha net değilse |
| **Creator Tool** | tek creator işini çözen normal uygulama | arayüz, konuşmaktan daha hızlıysa | iş uygulamanın kapsamı dışındaysa |
| **Trust Tool** | yetki/risk/kanıtı görünür yapan araç | kurmadan veya bağlanmadan önce | runtime güvenliğinin yerine |

Önemli:

**Prompt ≠ Assistant ≠ Agent Skill ≠ MCP ≠ Automation.**

Birbirine bağlanabilirler ama aynı şey değiller.

---

# 2. Alptuğ Harun profilindeki ana proje: AI Social Media Toolkit

## Bu nedir?

Ana merkez repo.

Şunları tek yerde birbirine bağlar:

- yapılandırılmış promptlar;
- asistan blueprint'leri;
- Agent Skills;
- creator workflow'ları;
- yerel skor araçları;
- MCP örnekleri;
- otomasyonlar;
- canlı Creator Frame Studio;
- güvenlik/trust araçları;
- release ve adoption kanıtları.

## Neden kullanılır?

“Benim işim için prompt mu skill mi MCP mi lazım?” bilmiyorsan buradan başlarsın.

## Hiç teknik değilsen

1. Ana repoyu aç.
2. Bütün dosyaları okuma.
3. Önce Creator Frame Studio canlı demoyu dene.
4. Sonra Quick Wins / Creator Materials tarafına geç.

## Terminal kullanabiliyorsan

Repo'yu indir/clone et ve:

```bash
python tools/first_run_check.py
```

Windows:

```powershell
py -3 -X utf8 tools/first_run_check.py
```

Beklenen son:

```text
FIRST-RUN CHECK: PASS
No API key, network call, account login or third-party Python package was required.
```

FAIL olursa API key ekleyerek düzeltmeye çalışma.

İlk hatayı, işletim sistemini, Python sürümünü ve komutu kaydet.

Gerçek kullanıcı raporunda sonucu açıkça **PASS / FAIL / BLOCKED** olarak yaz. `BLOCKED`, kod hatasından önce kurulum, ortam, izin veya dokümantasyon nedeniyle ilerleyemediğin anlamına gelir.

## PASS neyi kanıtlamaz?

- her MCP hostunun çalıştığını;
- bütün provider'ların canlı bağlandığını;
- gerçek kullanıcı adoption'ını;
- para kazandıracağını;
- içeriğin viral olacağını.

Sadece dokümante edilen yerel ilk kullanım yolunun beklendiği gibi çalıştığını kanıtlar.

---

# 3. Creator Context Builder — kendini her seferinde tekrar anlatma

Bir creator sistemi sürekli şunu soruyorsa:

> Kimsin?  
> Kitlen kim?  
> Tonun nasıl?  
> Ne istemiyorsun?  
> Bu metrik güncel mi?

ortak context eksiktir.

Creator Context Builder bir defa ortak kaynak oluşturur.

## Dört önemli etiket

- **VERIFIED:** doğrulanmış/açıkça verilmiş bilgi
- **PREFERENCE:** senin seçimin/tercihin
- **OBSERVED:** onaylı örneklerden gözlenen stil
- **HYPOTHESIS:** henüz doğrulanmamış yorum

## Sadece bunu kurmak için

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill creator-context-builder
```

İlk talep örneği:

> Güncel bilgilerim ve onayladığım üç yazı örneğinden ortak creator context oluştur. Gerçekleri, tercihleri, gözlemleri ve hipotezleri ayrı etiketle. Gizli bilgi kaydetme. Tarihi geçmiş metrikleri işaretle.

Beklenen sonuç:

`.agents/creator-context.md`

## Yapmaması gerekenler

- yazı stilinden hassas kişisel özellik çıkarmak;
- şifre/API key/cookie saklamak;
- eski metriği güncelmiş gibi yazmak;
- senin açık tercihini kendi tahminiyle değiştirmek.

---

# 4. Creator Ops — “hedefi biliyorum ama hangi skill lazım bilmiyorum”

Creator Ops yönlendiricidir.

Örnek:

> Bu araştırmayı Instagram Reel'e dönüştürmek istiyorum. Şu kanıtlar var. Public paylaşım yapma. En az sayıda skill ile workflow'u kur.

Beklenen:

1. hedef;
2. girdi/kanıt;
3. doğru rota;
4. kullanılabilir çıktı;
5. review;
6. ölçüm.

Direkt caption yazmaya atlıyorsa routing iyi çalışmamıştır.

---

# 5. Creator Frame Studio — en kolay no-code başlangıç

Bir görsel 4:5'te güzel olup 9:16'da bozulabilir.

Creator Frame Studio bunu paylaşmadan önce görmene yardım eder.

Canlı demo:

https://alptugharun.github.io/ai-social-media-toolkit/

Adımlar:

1. hassas olmayan test görseli ekle;
2. 4:5 → 9:16 → 2:3 → 16:9 arasında geç;
3. bir metin katmanı ekle;
4. preflight kartını kontrol et;
5. export al ve gözle incele.

Yerel çalışacak şekilde tasarlandı; CSP network bağlantısını kapatır.

Ama:

- AI görsel üretmez;
- otomatik paylaşmaz;
- Canva'nın yerine geçmeye çalışmaz;
- “kalite puanı” uydurmaz.

---

# 6. AI Workbench MCP — MCP nedir?

MCP'yi şöyle düşün:

**AI hostu ↔ açık tool sözleşmesi ↔ MCP server**

AI hostu sunucunun araçlarını görür ve gerektiğinde çağırabilir.

AI Workbench MCP sadece üç tool sunar:

- `list_prompts`
- `render_prompt`
- `get_assistant`

Özellikle dar tutulmuştur.

Network yok, shell yok, dosya yazma yok, hesap girişi yok, provider API çağrısı yok.

## Sıfırdan kurulum

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a2"
```

Önce:

```bash
alptugharun-ai-workbench-mcp --doctor
```

Sonra host ayarına geç.

Doğrulama sırası:

**kuruldu → doctor geçti → handshake → host tool'ları gördü → tool çağrıldı → beklenen çıktı**

Bir basamağın geçmesi sonraki basamağı otomatik kanıtlamaz.

---

# 7. Agent Skill Safety Auditor — kurmadan önce bak

Agent Skill sadece “bir markdown dosyası” gibi görünse de script çalıştırabilir.

Risk örnekleri:

- shell;
- network;
- environment variable;
- SSH/browser credential path;
- recursive delete;
- install lifecycle hook.

Kurulum:

```bash
git clone https://github.com/alptugharun/agent-skill-safety-auditor.git
cd agent-skill-safety-auditor
python -m pip install -e .
```

Tarama:

```bash
skill-audit path/to/skill
```

JSON:

```bash
skill-audit path/to/skill --format json
```

CI:

```bash
skill-audit path/to/skill --fail-on high
```

**LOW = güvenlik sertifikası değildir.**

Bu statik taramadır. Sunucunun/servisin kurulumdan sonra davranış değiştirmesini göremez.

Runtime monitoring ayrı savunma katmanıdır.

---

# 8. MCP Permission Inspector — bağlantıdan önce config'i incele

Safety Auditor skill dosyalarına bakar.

MCP Permission Inspector ise MCP client config'ine bakar.

Amaç:

- ne çalıştırılacak;
- hangi argümanlar kullanılacak;
- hangi environment sınırı var;
- ilk bağlantıda neye dikkat edilmeli

gibi noktaları görünür yapmak.

Server'ı çalıştırmadan config incelemek için vardır.

Runtime safety sertifikası değildir.

---

# 9. Creator Signal Lab — “AI öyle dedi” yerine açık formül

İki araç var.

## İçerik fırsatı skoru

“Hangisine önce çalışayım?”

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

## Outlier skoru

“Hangi post kendi normalime göre sıra dışıydı?”

```csv
platform,post_id,views,likes,comments,shares,saves
```

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

Bu araç:

- scrape yapmaz;
- canlı platform API'sine bağlanmaz;
- virallik tahmini yapmaz;
- gelir tahmini yapmaz.

Formülü görebilir ve değiştirebilirsin.

---

# 10. Prompt Library — bazen prompt yeterlidir

Tek bir tekrar kullanılabilir AI işi için önce prompt kullan.

İyi prompt kaydı şunları içerir:

- kullanım amacı;
- gereken girdiler;
- çıktı şekli;
- kalite kontrolü;
- örnek;
- sorun giderme;
- sonraki adım.

Başlangıç:

`prompts/README.md`

ve:

`QUICK-WINS.md`

Prompt yeterliyse MCP kurma.

---

# 11. Assistant Blueprints — aynı rol sürekli tekrarlanıyorsa

Bir assistant blueprint:

- rol;
- sınır;
- çıktı formatı;
- kalite kuralı;
- provider uyarlaması

taşır.

Aynı işi ChatGPT / Claude / Gemini / Grok gibi farklı yüzeylere taşımak için kullanılır.

Ama blueprint export etmek hesabında otomatik assistant oluşturmak değildir.

---

# 12. Agent Skills — prosedürü AI ajanının içine taşı

19 skill'in tamamını tek tek görmek için **[Tüm Agent Skill'ler — Sıfırdan Başla](AGENT-SKILLS-FROM-ZERO_TR.md)** rehberini kullan.

Önce listele:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Tek skill:

```bash
npx skills add alptugharun/ai-social-media-toolkit --skill reels-director
```

Hepsi:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

19 skill var diye 19'unu da kurmak zorunda değilsin.

Önce işi seç.

Üçüncü taraf skill kuracaksan önce incele.

---

# 13. Automation Recipes and GitHub Automations — önce manuel süreci kanıtla

Automation demek “AI kendi kafasına göre her şeyi yapsın” değildir.

Güvenli otomasyon şunları açıkça cevaplamalı:

1. ne zaman tetikleniyor?
2. ne okuyabiliyor?
3. ne yazabiliyor?
4. çıktı nedir?
5. yazdığını nasıl doğruluyor?
6. hangi durumda duruyor?
7. public/geri alınamaz eylemi kim onaylıyor?

Schedule ayarlı olması çalıştığını kanıtlamaz.

Run history ve çıktı kontrol edilir.

---

# 14. Release ve ZIP indirmeleri

v0.3 prerelease ayrı indirilebilir asset'ler sunar:

- tüm Agent Skills;
- Creator Context Builder;
- Creator Frame Studio offline;
- skills-only plugin;
- SHA256 checksum.

Bu download sayıları clone event'ten daha kasıtlı bir sinyaldir.

Ama:

**1 download = 1 benzersiz kullanıcı / başarılı kurulum / müşteri** değildir.

---

# 15. Trust puanlarını nasıl okumalıyım?

## M8ven

MCP tarafında:

- publisher doğrulama;
- code/sandbox doğrulama;
- live monitoring;
- tool annotation;
- tool test coverage;
- hassas erişim/exfiltration bulguları;
- reputation/adoption

gibi sinyalleri birleştirir.

Kod iyi olsa bile yeni proje adoption/reputation yüzünden sınırlı not alabilir.

## OpenSSF Scorecard

Önemli alanlar:

- dependency pinning;
- token permission;
- CI;
- CodeQL/SAST;
- Dependabot;
- security policy;
- branch protection;
- signed release;
- vulnerability;
- packaging.

Tek maintainer yeni projede contributor/code-review/maintained gibi puanlar doğal olarak düşük kalabilir.

Sahte hesap/reviewer ile puan kasılmaz.

## Official MCP Registry

Namespace ve package ownership gibi yayın/discovery güvenini doğrular.

Tam güvenlik sertifikası değildir.

## Glama

MCP tool/schema'larını bağımsız okuyabilir ve tool description kalitesini değerlendirebilir.

Başka bir dış bakıştır, mutlak gerçek değildir.

## skills.sh

Skills CLI'nin anonim install telemetry'sini kullanarak popülerliği sıralar.

Kendi kendimize install spam'i yapıp puan kasmayız.

---

## Rewrite Fact Guard — yerel önce/sonra kontrolü

**Nedir:** Brand Voice Humanizer içindeki, özgün metin ile yeniden yazılmış metni karşılaştıran dependency-free Python helper'ı.

**Ne zaman kullan:** iki sürüm de elindeyse ve sayısal ifadeler, yaygın birimler, literal URL'ler veya `--lock` ile koruduğun tam ifadeler değişmiş mi görmek istiyorsan.

**Ne değildir:** anlamsal doğruluk kontrolü, AI tespiti, hukuki inceleme veya yayın garantisi değildir. Aynı token farklı bağlama taşınabilir; kilitlemediğin bir niteleyici değişebilir ve araç bunu kaçırabilir.

**Başlamadan önce:** Python 3.10+ kullan ve önce yapay/hassas olmayan metinle dene. API anahtarı, ücretli model veya ağ bağlantısı gerekmez. Özel metinlerin log'a düşebileceği ortamlarda `--show-values` kullanma.

**İlk güvenli komut:**

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-good.txt --lock "garanti değildir"
```

**Beklenen:** `NO_TRACKED_CHANGE`, sıfır değişiklik ve **0** çıkış kodu.

Ardından bilerek değiştirilmiş yapay örneği çalıştır:

```bash
python skills/brand-voice-humanizer/scripts/fact_guard.py --before skills/brand-voice-humanizer/examples/before.txt --after skills/brand-voice-humanizer/examples/after-review.txt --lock "garanti değildir" --format json --show-values
```

**Beklenen:** `REVIEW_REQUIRED`, **7 bulgu**, **1** çıkış kodu. **2** çıkış kodu ise değişiklik bulgusu değil, girdi/ayar problemidir.

**PASS neyi kanıtlar:** o örnekte izlenen lexical token/URL/korumalı ifadenin tutulduğunu. Metnin tamamının olgusal veya anlamsal olarak doğru olduğunu kanıtlamaz.

**İlk sık hatalar:** yanlış dosya yolu, Python sürümünün düşük olması, `--lock` ifadesinin özgün metinde bulunmaması, UTF-8 problemi veya özel metinde `--show-values` kullanımı. Ayrıntı için [Türkçe rehberi](../skills/brand-voice-humanizer/README_TR.md) kullan.

---

# 16. Hangisini seçmeliyim?

**Kod bilmiyorum, bir şey denemek istiyorum**  
→ Creator Frame Studio / Quick Wins

**Her seferinde kendimi tekrar anlatıyorum**  
→ Creator Context Builder

**Ne kullanacağımı bilmiyorum**  
→ Creator Ops

**AI metni robot gibi**  
→ Brand Voice Humanizer

**Reel üretim planı lazım**  
→ Reels Director

**MCP hostunda yerel prompt/asistan tool'ları istiyorum**  
→ AI Workbench MCP

**Başkasının Agent Skill'ini kuracağım**  
→ Agent Skill Safety Auditor

**MCP config ekleyeceğim**  
→ MCP Permission Inspector

**CSV metriklerini açık formülle sıralamak istiyorum**  
→ Creator Signal Lab

**Tek iş için talimat yeterli**  
→ Prompt Library

**Aynı rol farklı provider'larda tekrar ediyor**  
→ Assistant Blueprint

**Workflow AI agent'ın içinde reusable olsun**  
→ Agent Skill

**Kanıtlanmış iş tekrar tekrar çalışsın**  
→ Automation

---

# 17. Bir sonuca güvenmeden önce

Sor:

- Bu hangi kanıta dayanıyor?
- Veri hangi tarihten?
- Synthetic mi gerçek mi?
- Network kullanıyor mu?
- Dosya/hesap üzerinde değişiklik yapıyor mu?
- Credential istiyor mu?
- Skor heuristic mi ölçülmüş sonuç mu?
- Bu runtime gerçekten test edildi mi?
- Kanıt kod testi mi, gerçek host testi mi, bağımsız kullanıcı kanıtı mı?

Bu repo özellikle bu seviyeleri birbirine karıştırmamaya çalışır.

---

# 18. Yardım

Ana Toolkit:

- `START-HERE.md`
- `SUPPORT.md`
- `SECURITY.md`
- Real User Lab #178
- Community Idea Box #169
- Discussions

Güvenlik açığını normal issue'da exploit detayıyla paylaşma.

Private vulnerability reporting kullan.

---

## Son kural

Bütün AI stack'ini kullanmak zorunda değilsin.

**İşe yarayan ve doğrulayabildiğin en küçük katmanla başla.**
