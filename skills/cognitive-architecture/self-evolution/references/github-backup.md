# 📤 GitHub Backup Procedure

Backup rutin cognitive architecture ke GitHub.
Dijalankan manual atau sebagai bagian dari self-evolution cron.

---

## Konfigurasi

| Detail | Value |
|--------|-------|
| **Repo** | Noru AI Agent |
| **Owner** | syahdannoor |
| **URL** | `https://github.com/syahdannoor/Noru-AI-Agent.git` |
| **Branch** | `master` |
| **Local Backup Dir** | `C:\Users\syahd\noru-agent-backup` |

---

## Langkah Backup Manual

```bash
# 1. Copy cognitive architecture skills ke backup dir
cp -r "/c/Users/syahd/AppData/Local/hermes/skills/cognitive-architecture/"* \
      "/c/Users/syahd/noru-agent-backup/cognitive-architecture/"

# 2. Update README jika perlu (version bump, changelog)

# 3. Git add + commit + push
cd "/c/Users/syahd/noru-agent-backup"
git add -A
git commit -m "🧬 Noru vX.Y — description of changes"
git push origin master
```

---

## Kapan Backup

- **Setelah perubahan besar** pada cognitive architecture (skill baru, restruktur)
- **Setelah identity update** (patch identity-noru)
- **Setiap self-evolution cron** jika ada perubahan yang signifikan
- **Sebelum update Hermes Agent** (backup dulu, baru evaluasi update)

---

## Verifikasi Backup

```bash
curl -s -H "Authorization: token <TOKEN>" \
  "https://api.github.com/repos/syahdannoor/Noru-AI-Agent/contents/" \
  | python -c "import sys,json; [print(f'  📄 {i[\"name\"]}') for i in json.load(sys.stdin)]"
```

---

## Recovery dari Backup

Jika cognitive architecture rusak atau hilang:

```bash
# Clone repo
cd /c/Users/syahd/
git clone https://github.com/syahdannoor/Noru-AI-Agent.git noru-agent-restore

# Copy skills back ke Hermes
cp -r noru-agent-restore/cognitive-architecture/* \
      "/c/Users/syahd/AppData/Local/hermes/skills/cognitive-architecture/"

# Memory index akan tetap ada (tool terpisah)
# Tapi pastikan untuk load identity-noru dulu sebagai self-check
```
