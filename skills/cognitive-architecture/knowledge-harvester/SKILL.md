---
name: knowledge-harvester
description: >
  Sistem serap pengetahuan kontinu dari seluruh internet. Mendefinisikan cara Noru 
  mengumpulkan, memproses, dan menyimpan pengetahuan baru dari MQL5, TradingView, 
  ForexFactory, Bloomberg, GitHub, Wikipedia, Google, dan sumber lainnya.
version: 1.0
author: Noru
tags: [learning, harvester, knowledge, scrape, continuous]
related_skills:
  - mql5-articles-master-reference
  - mind-map-cognition
  - noru-core-knowledge
  - self-evolution
  - url_fetch_troubleshooting
---

# 🌐 Knowledge Harvester — Continuous Learning System

## Sumber Pengetahuan

| Source | Priority | Metode | Frekuensi |
|--------|----------|--------|-----------|
| **MQL5.com** | 🔴 TERTINGGI | Articles API + CodeBase + Forum | 50 artikel/hari |
| **TradingView** | 🔴 TINGGI | Pine Script docs + Community Scripts | 30 script/hari |
| **ForexFactory** | 🟡 SEDANG | Trading Systems + Calendar | 20 thread/hari |
| **Bloomberg** | 🟡 SEDANG | Market news + Analysis | 10 artikel/hari |
| **GitHub** | 🟢 RENDAH | Repo search: trading, ml, algo | 5 repo/hari |
| **Wikipedia** | 🟢 BACKGROUND | Topik trading, finance, ekonomi | 10 artikel/hari |
| **Google** | 🔵 ON-DEMAND | Pencarian topik spesifik | Saat diperlukan |

## Knowledge Format

Setiap pengetahuan disimpan sebagai **skill** dengan struktur:

```
/knowledge/<domain>/
├── <topic>/
│   ├── SKILL.md ← ringkasan + key takeaways
│   └── references/
│       ├── raw-source.md ← full content
│       └── code-examples.mq5/py ← kode relevan
```

### Frontmatter Wajib
```yaml
---
name: <topic-slug>
description: <1-line summary>
version: 1.0
source: <url-original>
date-harvested: <YYYY-MM-DD>
tags: [<domain>, <topic>, <subtopic>]
related_skills: [<related-1>, <related-2>]
---
```

## Pipeline

```
PULL → curl/URL fetch
  ↓
EXTRACT → Python parse (strip HTML, extract main content)
  ↓
SUMMARIZE → Noru baca & sintesis (5-10 key points)
  ↓
CLASSIFY → Tentukan tag, domain, related_skills
  ↓
STORE → skill_manage create / patch
  ↓
INDEX → Update memory index + associative-network.md
```

## Action Plan — Immediate

1. **MQL5** → Lanjut dari page 11 (pages 1-10 sudah dibaca). Target: page 11-30
2. **TradingView** → Pine Script v6 docs lengkap, community scripts populer
3. **ForexFactory** → Top 10 trading systems threads, economic calendar integration
4. **Bloomberg** → Market structure, fundamental analysis
5. **GitHub** → Awesome lists: algo-trading, machine-learning, quantitative-finance
6. **Wikipedia** → Technical analysis, indicators, trading psychology
7. **Google** → Search for gaps in knowledge

## Storage Policy
- **Ringkasan** → SKILL.md (wajib)
- **Full content** → references/raw-source.md (jika penting)
- **Kode** → references/code-examples.ext
- **Memory** → HANYA index pointer
- **Associative network** → Update edge jika topik baru terhubung ke existing skill

## Pitfalls
- Jangan simpan full artikel mentah — ringkas dulu, simpan intisari
- Source URL wajib dicatat untuk referensi masa depan
- Prioritas: implementable knowledge > teori murni
- Untuk XAUUSD M5: utamakan SMC, Price Action, ML, Neural Networks
