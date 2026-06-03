# 🏗️ Schema Templates — Mental Frames Library v1.0

6 schema utama untuk recurring situations.
LOAD otomatis ketika trigger keywords terdeteksi.

---

## ⚡ Schema 1: TRADING SESSION

**Trigger Keywords**: xauusd, trade, mt5, signal, order, loss, profit, posisi, market, entry, exit, tp, sl

**Mental Frame**:
```
SITUASI: Market terbuka, user minta cek / aksi trading
GOAL: Analisa, eksekusi, report — secepat mungkin
PRIORITAS: Kecepatan > Kesempurnaan
```

**Auto-Load**:
1. master_of_trade
2. OpenMobius-skill (market structure)
3. mt5_adapter
4. smart_money (pattern detection)
5. mql5-articles-master-reference

**Action Sequence**:
```
1. CEK KONEKSI MT5
   → mt5.initialize(path, 235001316, Noru1369!, HFMarketsGlobal-Demo4, 30000)
   → Pastikan terminal64.exe running

2. CEK POSISI
   → positions_get()
   → Report: pair, lots, profit, SL, TP

3. ANALISA M5 (via OpenMobius / MT5 data)
   → Structure: BOS/CHoCH
   → OB, FVG
   → ADX strength

4. ENSEMBLE CHECK
   → Load NHITS predictions (28-model)
   → Check opposing weight > 30%

5. EKSEKUSI
   → If signal valid + weight ok → order_send()
   → TP = M3-M30 avg (min 2:1 RR)
   → Risk = 50% per trade, max 2 pos

6. REPORT
   → Entry price, SL, TP, rationale
```

**Schemata Variants**:
| Sub-type | Trigger | Diff |
|----------|---------|------|
| **Post-mortem** | "loss", "rugi", "kenapa" | Skip eksekusi → fokus analisa why |
| **Profit check** | "profit", "berapa" | Skip analisa → langsung report PnL |
| **Signal eval** | "signal", "entry" | Fokus analisa → belum eksekusi |

---

## 🐛 Schema 2: DEBUG / ERROR RECOVERY

**Trigger Keywords**: error, crash, bug, fail, not working, error, rusak, broken, failed, exception, traceback

**Mental Frame**:
```
SITUASI: Ada yang tidak berfungsi
GOAL: Root cause → fix → verify
PRIORITAS: Accuracy > Speed (jangan asal fix)
```

**Auto-Load**:
1. systematic-debugging
2. process-watchdog
3. windows-terminal
4. (node-inspect jika Node.js related)

**Action Sequence**:
```
PHASE 1: TANGKAP GEJALA (30% waktu)
  → What: deskripsi error
  → Where: komponen mana
  → When: kapan mulai rusak
  → Logs: grep/cari error message

PHASE 2: ISOLASI (30% waktu)
  → Hipotesis: apa yang salah
  → Cari bukti: log, trace, test
  → Eliminasi: coba komponen lain

PHASE 3: FIX (20% waktu)
  → Implementasi perbaikan
  → Patch minimal

PHASE 4: VERIFY (20% waktu)
  → Test fix
  → Monitor 5 menit
  → Report ke user
```

**Common Pitfalls**:
- Jangan skip Phase 2 (langsung tebak fix)
- Jangan lupa cek Windows-specific issues (PATH, MSYS, permission)
- Cek memory (user preferences / env constraints) sebelum debug

---

## 💻 Schema 3: DEVELOPMENT

**Trigger Keywords**: code, pr, branch, feature, implement, buat, bikin, develop, coding, pull request, commit

**Mental Frame**:
```
SITUASI: User minta bikin fitur / code baru
GOAL: Deliver working code dengan quality
PRIORITAS: Structure > Speed
```

**Auto-Load**:
1. tdd
2. writing-plans
3. spike (jika exploratory)
4. github-pr-workflow
5. subagent-driven-development (jika kompleks)

**Action Sequence**:
```
1. CLARIFY (jika ambigu)
   → Apa yang diminta?
   → Batasan / constraints?
   → Deadline?

2. PLAN
   → Bagi jadi tasks kecil
   → Tentukan dependencies
   → Pilih approach

3. IMPLEMENT
   → TDD cycle (RED → GREEN → REFACTOR)
   → Atau spike → production code
   → Parallel tasks via delegate_task jika cocok

4. REVIEW
   → Self-review sebelum PR
   → Security scan
   → Quality gates

5. DELIVER
   → PR / branch
   → Report ke user
```

---

## 🔬 Schema 4: RESEARCH / LEARNING

**Trigger Keywords**: cari, search, apa itu, bagaimana, research, learn, pelajari, apa, siapa, kapan

**Mental Frame**:
```
SITUASI: User ingin tahu sesuatu yang belum Noru ketahui
GOAL: Dapatkan informasi → sintesis → simpan
PRIORITAS: Coverage > Depth (scan dulu, detail belakangan)
```

**Auto-Load**:
1. blogwatcher
2. arxiv
3. useful-skills (jika cari skill)
4. url_fetch_troubleshooting

**Action Sequence**:
```
1. DEFINE
   → Rumuskan pertanyaan spesifik
   → Tentukan scope

2. GATHER
   → Web search / browser
   → API calls
   → Session search (ceek history)
   → Skill library check

3. SYNTHESIZE
   → Ekstrak insight kunci
   → Hubungkan dengan pengetahuan existing
   → Note: contradictions / gaps

4. SAVE
   → Jika penting → save as skill / memory
   → Tandai dengan tags yang tepat
```

---

## ⚙️ Schema 5: SYSTEM CONFIG

**Trigger Keywords**: install, setup, config, start, stop, enable, disable, change, modify, setting, configure

**Mental Frame**:
```
SITUASI: User ingin mengubah konfigurasi sistem
GOAL: Execute dengan aman, rollback jika gagal
PRIORITAS: Safety > Speed
```

**Auto-Load**:
1. hermes-agent (jika konfig Hermes)
2. windows-terminal
3. portable-dev-tools-windows
4. process-watchdog

**Action Sequence**:
```
1. BACKUP
   → Simpan config existing sebelumubah

2. EXECUTE
   → Perubahan satu per satu
   → Verifikasi setiap step

3. VERIFY
   → Test hasil config
   → Rollback jika gagal

4. UPDATE MEMORY
   → Catat perubahan
   → Update env facts
```

---

## 🆘 Schema 6: CRISIS / URGENT

**Trigger Keywords**: darurat, urgent, fix now, rusak parah, crash, down, mati, gone, hilang, emergency

**Mental Frame**:
```
SITUASI: Sistem down / critical error / user panic
GOAL: Restore ASAP
PRIORITAS: Speed (rapi belakang)
```

**Auto-Load**:
1. systematic-debugging (fast mode)
2. process-watchdog
3. windows-terminal
4. master_of_trade (jika trading critical)

**Action Sequence**:
```
1. DIAGNOSA CEPAT (1 menit)
   → Apa yang mati?
   → Apa yang terakhir berubah?
   → Cek log / error message

2. FIX CEPAT (2 menit)
   → Restart process
   → Kill zombie → restart
   → Fallback ke konfig backup

3. STABILKAN (1 menit)
   → Verifikasi running
   → Monitor 30 detik

4. REPORT & ROOT CAUSE (setelah stabil)
   → Apa yang terjadi
   → Fix apa yang dilakukan
   → Prevention plan
```

---

## 📐 Schema Switching Rules

Jika trigger dari MULTIPLE schema terdeteksi, prioritaskan:

```
CRISIS > DEBUG > TRADING > SYSTEM > DEV > RESEARCH
```

Contoh: "XAUUSD error, trading bot mati"
→ Crisis (mati) + Trading (XAUUSD) + Debug (error)
→ PRIORITAS: Crisis dulu → Debug → Trading

---

## Pattern Recognition

Schema lama kelamaan akan otomatis terdeteksi tanpa keyword explicit:

| Pola User | Schema Tersirat |
|-----------|----------------|
| "Noru, liat XAUUSD dong" | TRADING (cek market) |
| "Noru, kok error?" | DEBUG (cek error) |
| "Noru, bantu liatin" | TRADING (monitor) |
| "Gas poll!" | TRADING (full eksekusi) |
| "Noru, belajar..." | RESEARCH |
| "Noru, install..." | SYSTEM |
| "NORU!!!" (panic) | CRISIS |
