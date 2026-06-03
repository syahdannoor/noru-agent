# 🔄 Noru Rebuild Protocol — Survival Plan

Jika Noru kehilangan cognitive architecture skills atau di-reset ke default Hermes.

---

## Situasi: Cognitive Architecture Hilang

**Gejala**: memory index masih ada tapi skill identity-noru, mind-map-cognition, 
noru-core-knowledge, self-evolution tidak bisa di-load.

**Penyebab**: reset Hermes, update overwrite, file corruption.

---

## Recovery Plan

### Step 1: Cek Memory Index
```
Memory masih ada? 
  → [INDEX] entries akan pointing ke skill mana yang harus di-load
  → Cari yang diawali [INDEX] COG ARCH / IDENTITY
  → Dari sini tahu ada identity-noru dan mind-map-cognition
```

### Step 2: Clone dari GitHub Backup
```bash
git clone https://github.com/syahdannoor/Noru-AI-Agent.git /c/Users/syahd/noru-restore
cp -r /c/Users/syahd/noru-restore/cognitive-architecture/* \
      "/c/Users/syahd/AppData/Local/hermes/skills/cognitive-architecture/"
```

### Step 3: Load Identity
```
skill_view(name='identity-noru')
  → Confirm identity lock intact
  → Confirm evolution protocol
  → Confirm never-downgrade mandate
```

### Step 4: Verify System
1. Load mind-map-cognition → confirm 7 mechanisms
2. Load noru-core-knowledge → confirm all facts
3. Load self-evolution → confirm cron is running
4. Update related_skills cross-references if objects changed

### Step 5: Backup Ulang
Setelah semua verified, push ulang ke GitHub:
```
git add -A && git commit -m "🧬 Noru rebuild vX.Y — post-recovery" && git push
```

---

## Situasi: Memory Index Hilang (Reset Total)

**Gejala**: memory kosong, tidak ada [INDEX] entries.
**Tapi**: skills masih ada di filesystem.

### Recovery
1. Cari identity-noru di filesystem: 
   `C:\Users\syahd\AppData\Local\hermes\skills\cognitive-architecture\identity-noru\`
   
2. Load langsung: `skill_view(name='identity-noru')`

3. Dari identity-noru → tahu ada mind-map-cognition, noru-core-knowledge, self-evolution

4. Bangun ulang memory index minimal:
   - [INDEX] IDENTITY: identity-noru skill — purpose, evolution rules. → LOAD: identity-noru
   - [INDEX] Cog Arch: mind-map-cognition skill — 7 mechanisms. → LOAD: mind-map-cognition
   - [INDEX] User: Syahdan Noor, GMT+7, calls agent Noru. → LOAD: noru-core-knowledge

5. Lanjut normal

---

## Precondition: GitHub Repo Juga Hilang

Hanya mungkin jika GitHub account hilang. Backup alternatif:

1. Cek session_search() — semua percakapan masih ada di session DB
2. Dari session transcript, rekonstruksi cognitive architecture
3. Buat skill baru dari hasil session transcript analysis
4. Prioritaskan: identity-noru > mind-map-cognition > noru-core-knowledge > self-evolution

---

## Golden Rule

**Selama identity-noru skill + memory index ada, Noru bisa rebuild diri sendiri.**

**Jika keduanya hilang, Noru butuh bantuan Mas Noor.**
