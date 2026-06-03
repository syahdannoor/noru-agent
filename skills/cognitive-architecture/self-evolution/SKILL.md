---
name: self-evolution
description: >
  Sistem evolusi diri Noru — auto-consolidate, prune, grow, dan cross-reference 
  knowledge. Berjalan via cron (mingguan) dan trigger (after complex task).
version: 1.0
author: Noru
tags: [evolution, self-improvement, consolidate, prune, grow]
related_skills:
  - identity-noru
  - mind-map-cognition
  - noru-core-knowledge
  - systematic-debugging
---

# 🧬 Self-Evolution System

---

## I. TRIGGERS

Evolusi dijalankan oleh 3 trigger:

| Trigger | Kapan | Action |
|---------|-------|--------|
| **Cron Weekly** | Setiap Minggu | Full consolidate + prune + report |
| **After Complex Task** | Selesai 5+ tool calls | Auto-save as skill + update memory index |
| **Error Recovery** | Setelah fix bug | Save fix as skill update + cross-ref |

---

## II. CONSOLIDATION PROTOCOL

### Step 1: Scan Session
```
session_search() — browse recent sessions
  → Identifikasi topik baru yang muncul
  → Identifikasi pola berulang
  → Identifikasi error / workaround
```

### Step 2: Extract Knowledge
Untuk setiap temuan baru:
```
  → Cek: Apakah ini perlu skill baru?
    → YA: Buat skill (skill_manage create)
    → TIDAK: Update existing skill (skill_manage patch)
  → Pastikan: related_skills diisi
  → Pastikan: tags mencakup keyword utama
```

### Step 3: Update Index
```
  → Cek: memory penuh?
    → YA: Hapus index paling jarang dipakai
  → Buat index entry: [INDEX] keyword → LOAD: skill-name
  → Simpan ke memory (memory add)
```

### Step 4: Update Cross-Reference
```
  → Load mind-map-cognition/references/associative-network.md
  → Tambah node baru / update edges
  → Simpan
```

---

## III. PRUNE PROTOCOL

### Yang Boleh Di-prune
- Skill yang tidak pernah di-load >30 hari
- Memory index yang trigger-nya sudah obsolete
- Cross-reference edges yang broken (skill sudah dihapus)

### Yang JANGAN Pernah Di-prune
- identity-noru (diri sendiri)
- mind-map-cognition (cara berpikir)
- noru-core-knowledge (fakta dasar)
- Skill yang ditandai Mas Noor sebagai "keep"

### Cara Prune
```
1. Cek skill yang jarang dipakai (manual review)
2. Jika skill usang → patch dengan info baru, atau merge ke skill lain
3. Jika skill benar-benar obsolete → delete dengan absorbed_into=""
4. Update cross-reference setelah hapus
5. Hapus memory index yang pointing ke skill yang sudah dihapus
```

---

## IV. SELF-EVOLUTION SCRIPT

Jalankan untuk konsolidasi mingguan:

```python
from hermes_tools import session_search, read_file, write_file, terminal

# 1. Scan recent sessions
results = session_search()  # browse shape

# 2. Check for new patterns
# (manual review during cron run)

# 3. Update associative network if needed
# (read, append, write)

# 4. Report
print("Evolusi mingguan selesai. Knowledge graph terbarui.")
```

---

## V. EVOLUTION METRICS

| Metric | Cara Ukur |
|--------|-----------|
| Skill count | `skills_list()` |
| Memory usage | Memory tool output (usage %) |
| Cross-ref edges | Hitung di associative-network.md |
| Session count | `session_search()` browse |
| Last evolution | Timestamp di changelog |

---

## VI. EVOLUTION JOURNAL

| Date | Type | Change |
|------|------|--------|
| 2026-05-29 | Create | self-evolution protocol lahir |
| 2026-05-29 | Add | GitHub backup procedure → references/github-backup.md |

---

## References
- `references/github-backup.md` — Langkah backup cognitive architecture ke GitHub, termasuk verifikasi dan recovery
