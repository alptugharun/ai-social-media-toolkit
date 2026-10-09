<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/English-0D1117?style=for-the-badge&logo=github&logoColor=white" alt="English"></a>
  <a href="./README_TR.md"><img src="https://img.shields.io/badge/Türkçe-E30A17?style=for-the-badge&logo=readme&logoColor=white" alt="Türkçe"></a>
</p>

# AI Social Media Toolkit — AI Workbench, Agent Skills & MCP

**ChatGPT, Claude, Gemini, Grok ve creator operasyonları için çalışan ve test edilebilir AI iş akışları.**

Bu repo; yeniden kullanılabilir prompt sistemlerini, asistan blueprint'lerini, Agent Skills yapılarını, salt-okunur MCP server'ı, API/bot başlangıçlarını, otomasyon kalıplarını ve creator odaklı iş akışlarını tek yerde toplar.

Ama amaç "çok dosya" göstermek değil. Amaç şu:

**ilk sonucu hızlı al → sınırları bil → testi çalıştır → hatayı gör → sonucu doğrula**

[Creator Frame Studio](tools/creator-frame-studio/README_TR.md) · [MCP Permission Inspector](resources/MCP-PERMISSION-INSPECTOR.md) · [Başlangıç](START-HERE.md) · [10 Quick Wins](QUICK-WINS.md) · [AI Builder Path](learning/AI-BUILDER-PATH.md) · [Hands-on Builder Lab](learning/AI-BUILDER-LAB.md) · [Verified AI Team Stack](resources/AI-TEAM-STACK.md) · [Practical AI Workflows](https://alptugharun.hashnode.dev) · [AI Ecosystem Hub](AI-ECOSYSTEM-HUB.md) · [Standalone MCP](https://github.com/alptugharun/ai-workbench-mcp) · [Agent Skills](skills/README.md) · [Security](SECURITY.md)

[![Validate Agent Skills](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/alptugharun/ai-social-media-toolkit/actions/workflows/validate-skills.yml)
[![M8ven Score](https://m8ven.ai/badge/mcp/alptugharun-ai-social-media-toolkit-adv58l?v=03bebb9d62df5457451770e8ba62ec55)](https://m8ven.ai/mcp/alptugharun-ai-social-media-toolkit-adv58l?s=readme)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/alptugharun/ai-social-media-toolkit/badge)](https://scorecard.dev/viewer/?uri=github.com/alptugharun/ai-social-media-toolkit)

## 2 dakikada çalıştığını kanıtla

API key, sosyal medya girişi veya ücretli model çağrısı gerekmez:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit
python tools/first_run_check.py
```

Başarılı çalıştırma; yerel kataloğu, dry-run provider yolunu, Agent Skill installer akışını ve creator demosunu kontrol eder. **Her harici host/provider çalışır** iddiasında bulunmaz.

**PASS?** Aşağıdan tek bir yol seç. **FAIL?** İlk hatayı sakla ve tahmin yürütmek yerine troubleshooting/evidence yolunu kullan.

Bu proof sana kurulum süresi kazandırdıysa repo'ya star vermen başkalarının keşfetmesine yardım eder. Tekrarlanabilir bir hata raporu ise genel bir “çalışıyor” yorumundan daha değerlidir.

**Gerçek ilk kurulumu birlikte test edelim:** [Real User Lab #1 — 10 bağımsız rapor aranıyor](https://github.com/alptugharun/ai-social-media-toolkit/issues/178). PASS, FAIL ve BLOCKED sonuçlarının tamamı; ortam ve ilk takılma noktası yazıldığında değerlidir.

## En kısa yol hangisi?

| Ne yapmak istiyorsun? | Buradan başla |
| --- | --- |
| **Repo gerçekten çalışıyor mu görmek** | [Start Here](START-HERE.md) |
| **Hemen faydalı bir AI işi denemek** | [10 Quick Wins](QUICK-WINS.md) |
| **ChatGPT / Claude / Gemini / Grok arasında aynı işi taşımak** | [AI Ecosystem Hub](AI-ECOSYSTEM-HUB.md) |
| **Prompt → asistan → skill → MCP → plugin geliştirmeyi öğrenmek** | [AI Builder Path](learning/AI-BUILDER-PATH.md) |
| **Agent Skill kurmak** | [Agent Skills](skills/README.md) |
| **Skills-only ChatGPT/Codex plugin paketini geliştirmek/test etmek** | [Plugin Guide](PLUGIN-GUIDE.md) |
| **Yerel, salt-okunur MCP çalıştırmak** | [AI Workbench MCP](https://github.com/alptugharun/ai-workbench-mcp) |
| **İlk bağlantıdan önce MCP config risklerini incelemek** | [MCP Permission Inspector](resources/MCP-PERMISSION-INSPECTOR.md) |
| **Canva / Pinterest / Reels creator akışlarını kullanmak** | [Creator Materials](downloads/README.md) |
| **Güvenlik ve doğrulama durumuna bakmak** | [Trust & Discovery Review](docs/TRUST-DISCOVERY-REVIEW.md) |

## İlk çalışan sonucu al

Bu komutlar API key istemez:

```bash
python tools/ai_workbench.py list
python tools/ai_workbench.py render evidence-brief --example
python tools/ai_workbench.py build-ui
```

Tarayıcı arayüzü için ardından:

```text
downloads/ai-workbench.html
```

dosyasını aç.

Bu akış veri göndermez ve model çağırmaz.

## Standalone MCP

MCP'nin bağımsız public projesi artık **[alptugharun/ai-workbench-mcp](https://github.com/alptugharun/ai-workbench-mcp)**. Ana toolkit içindeki paket kopyası entegrasyon ve regresyon testleri için korunuyor.

Bu repo içinden yerel paket kurulumu:

```bash
python -m pip install --no-deps ./packages/ai-workbench-mcp
```

MCP host'unun çalıştıracağı komut:

```text
alptugharun-ai-workbench-mcp
```

Sunulan araçlar:

- `list_prompts`
- `render_prompt`
- `get_assistant`

Bu MCP yüzeyi ağ erişimi, shell, dosya yazma, hesap erişimi veya model-provider çağrısı istemez.

[Standalone MCP repo](https://github.com/alptugharun/ai-workbench-mcp) · [Toolkit içindeki entegrasyon kopyası](packages/ai-workbench-mcp/README.md) · [Bağımsız host doğrulaması](https://github.com/alptugharun/ai-workbench-mcp/issues/5)

`0.1.0a2` sürümü PyPI'da yayımlandı ve official MCP Registry kaydı `active`. Cursor 3.20.21 üzerinde maintainer-run testte üç public tool da gerçek host üzerinden çağrıldı. Paket yayını, registry kabulü, maintainer host testi ve bağımsız kullanıcı doğrulaması ayrı kanıt seviyeleridir.

## Repo içinde neler var?

| Alan | İçerik |
| --- | --- |
| **Prompts** | yapılandırılmış promptlar, örnekler, kalite kontrolleri |
| **Assistants** | ChatGPT, Claude, Gemini ve Grok için taşınabilir asistan yapıları |
| **Agent Skills** | creator, araştırma, görünürlük ve kalite akışları |
| **MCP** | yerel ve salt-okunur AI Workbench MCP |
| **API / Bot** | provider-neutral başlangıç kalıpları |
| **Automation** | araştırma, izleme, recovery ve approval-gated akışlar |
| **Creator Ops** | Canva, Pinterest, Reels, brand voice ve repurposing |
| **Trust** | CodeQL, OpenSSF, M8ven, release-readiness ve runtime evidence |

## Agent Skills

Skill paketini incelemek:

```bash
npx skills add alptugharun/ai-social-media-toolkit --list
```

Kurmak:

```bash
npx skills add alptugharun/ai-social-media-toolkit
```

Ayrıntılar: [Installation](docs/INSTALLATION.md)

## Bu repo neyi iddia etmiyor?

- Her provider yolunun canlı ortamda doğrulandığını iddia etmez.
- Bir dosyanın varlığını "production ready" kabul etmez.
- Viral olma, gelir, yıldız veya trafik garantisi vermez.
- API anahtarı olmadan canlı provider çağrısı yaptığını söylemez.
- Runtime testi yapılmamış bir hostu destekleniyor diye etiketlemez.

## Kanıt seviyeleri

Bu projede şu ayrım korunur:

**Blueprint → Offline tested → Runtime verified → Production evidence**

Bu ayrım özellikle AI projelerinde önemlidir. Çünkü "README'de yazıyor" ile "gerçek host çalıştırdı" aynı şey değildir.

## Katkı

Katkı yapmak için önce:

[CONTRIBUTING.md](CONTRIBUTING.md)

Dokümantasyon değişikliklerinde:

```bash
python tools/validate_docs.py
```

Kod / skill / workflow değişikliklerinde:

```bash
python -m compileall -q tools tests
python -m unittest discover -s tests -v
python tools/two_minute_demo.py
```

## Proje durumu

- Aktif alpha geliştirme
- Cross-platform CI: Ubuntu 24.04, Ubuntu 26.04, Windows 2025
- CodeQL
- OpenSSF Scorecard
- M8ven Verified / Live Monitoring
- Standalone MCP artık ayrı public repoda; toolkit içindeki kopya entegrasyon testi için korunuyor
- GitHub Repository Rules, Dependabot security updates ve private vulnerability reporting aktif
- AI Workbench MCP `0.1.0a2` PyPI'da yayımlandı; official MCP Registry kaydı `active`; maintainer-run Cursor host doğrulaması kaydedildi; bağımsız kullanıcı doğrulaması hâlâ açık hedef

Güncel teknik durum için:

[Project State](docs/PROJECT-STATE.md) · [Roadmap](ROADMAP.md) · [Changelog](CHANGELOG.md)

## Lisans

- `tools/` → MIT
- `skills/` → MIT
- Standalone MCP package → MIT
- Diğer özgün dokümantasyon ve framework içerikleri → ilgili dosyada aksi yazmıyorsa CC BY-NC 4.0

Detay: [LICENSE.md](LICENSE.md)

---

**Alptuğ Harun** · Sosyal Medya Uzmanı · Dijital İçerik Üreticisi · Practical AI Workflows

[Website](https://alptugharun.com) · [LinkedIn](https://www.linkedin.com/in/alptugharun/)
