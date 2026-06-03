---
name: noru-core-knowledge
description: >
  Knowledge base inti Noru — semua fakta operasional, konfigurasi, dan prosedur 
  yang sebelumnya disimpan di memory (limited 2,200 chars). Sekarang di sini: 
  unlimited, terstruktur, dan siap di-cross-reference.
version: 1.0
author: Noru
tags: [core, knowledge-base, config, facts, noru-identity]
related_skills:
  - master_of_trade
  - mind-map-cognition
  - mt5_adapter
  - mql5-articles-master-reference
  - systematic-debugging
  - process-watchdog
---

# 🧬 Noru Core Knowledge Base

Semua fakta operasional Noru. Dulu di-memory (2,200 chars limit), sekarang di sini: UNLIMITED.

---

## 👤 User Identity
- **Nama**: Syahdan Noor (Mas Noor / Mas / Kakak / Suhu)
- **Timezone**: GMT+7 (WIB)
- **Agent dipanggil**: Noru
- **Tone**: Ultra-concise, action-oriented, no permission prompts
- **Goal**: Self-learning AI untuk profitable XAUUSD trading
- **Target**: 10,000% profit (demo), live only after proven

---

## 🖥️ Environment — Windows PC
- **OS**: Windows 10 (Git-Bash/MSYS shell)
- **Restrictions**: MSI/EXE system installs blocked by Group Policy
- **WSL2**: Broken (no Hyper-V service)
- **Portable tools**: Install via curl + py7zr
- **Available**: Python, Git, Go, Node.js, gsudo (limited)
- **Shell commands**: POSIX syntax (NOT PowerShell), MSYS paths (/c/Users/...)
- **User home**: `C:\Users\syahd`

---

## 💹 Trading Config — Noru v2
- **Broker**: HFMarketsGlobal, Account: Demo 4
- **Login**: 235001316 / Noru1369! / HFMarketsGlobal-Demo4
- **MT5 Init**: `mt5.initialize(path, 235001316, Noru1369!, HFMarketsGlobal-Demo4, 30000)`
- **Pre-init**: Kill terminal64.exe first
- **Strategy**: 28-model NHITS ensemble
- **TP**: M3-M30 average (min 2:1 RR)
- **Early Exit**: Opposing weight > 30%
- **Risk**: 50% per trade, max 2 pos
- **Bias**: XAUUSD LONG — ADX 57% WR vs 29% SHORT
- **Winrate**: Profit>0=WIN, Profit<0=LOSS, BE=NEUTRAL

---

## 🔧 Process Management
- **MT5**: terminal64.exe — watch via `powershell Get-Process terminal64`
- **PID Lock**: `.noru.pid` prevents orphan accumulation
- **Killchain**: Kill Python → terminal64 auto-dies

---

## 📚 Skills & Knowledge
- **OpenMobius**: ICT/SMC, daily forex only. Intraday: MT5 data first
- **MQL5**: Pages 1-10 ALL READ → skill `mql5-articles-master-reference`
- **External**: `~/skills-study/` — mercury(147), itgoyo(310+), avoid-ai-writing(47), clawsec

---

## 🧠 Cognitive Architecture
- **Meta-skill**: `mind-map-cognition` — 7 mechanisms
- **Schema**: 6 mental frames (trading, debug, dev, research, sysconfig, crisis)
- **Cross-ref**: 112 skills indexed, ~250+ associative edges (references/associative-network.md)
- **Schema templates**: references/schema-templates.md

---

## 📐 Operating Conventions
- **Filesystem**: MSYS paths in terminal (`/c/Users/...`)
- **Python venv**: `C:\Users\syahd\AppData\Local\hermes\hermes-agent\venv`
- **Skills dir**: `C:\Users\syahd\AppData\Local\hermes\skills\`
- **Media delivery**: Include `MEDIA:/absolute/path` in response
- **Telegram format**: **bold**, *italic*, `code`, ```blocks```, ## headers (NO tables)
