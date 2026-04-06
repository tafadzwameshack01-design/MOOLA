# ⚽ ZEUS FIX + FOOTBALL APP DEPLOYMENT GUIDE

## 🔴 YOUR ZEUS NBA APP ERROR

**Problem:** `OperationalError: no such column: league_id` in `grade_picks()`

**Root Cause:** The database schema is missing the `league_id` column that the code expects.

---

## ✅ 3 WAYS TO FIX IT

### METHOD 1: Automated Python Script (EASIEST) ⭐

```bash
# Run this ONE TIME to fix your database:
python fix_zeus_database.py

# It will:
# 1. Create automatic backup (moola.db.backup_[timestamp])
# 2. Add the missing league_id column
# 3. Update all existing records
# 4. Set constraints
```

**Steps:**
1. Download `fix_zeus_database.py`
2. Place it in your Zeus project folder
3. Run: `python fix_zeus_database.py`
4. Answer "yes" when prompted
5. Restart your app: `streamlit run zeus_app.py`

✅ **Your app should now work!**

---

### METHOD 2: Code-Level Fix (IF YOU CAN'T RUN PYTHON)

**Edit your `zeus_app.py`:**

Find the `grade_picks()` function (around line 993) and replace it with the code from `fix_grade_picks_function.py`

This version gracefully handles the missing column without modifying the database.

**Benefits:**
- No database modification needed
- Works immediately
- Safe fallback logic

---

### METHOD 3: Direct SQL (FOR ADVANCED USERS)

Open SQLite and run:

```sql
-- Connect to your database
sqlite3 moola.db

-- Add missing column
ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA';

-- Verify it worked
PRAGMA table_info(picks_log);

-- Exit
.quit
```

Then restart your Zeus app.

---

## 🚀 IMMEDIATE ACTION PLAN

### For Your Zeus App (Choose ONE fix above):

**Option 1 - Easiest:**
```bash
python fix_zeus_database.py
streamlit run zeus_app.py
```

**Option 2 - Copy-Paste:**
1. Open `fix_grade_picks_function.py`
2. Copy the `ensure_picks_log_schema()` function
3. Paste into your `zeus_app.py` before `main()` function
4. Save and restart app

**Option 3 - SQL Command:**
```bash
sqlite3 moola.db "ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA';"
streamlit run zeus_app.py
```

---

## ⚽ FOOTBALL APP - NOW READY TO DEPLOY

Your API key is already configured!

```
FOOTBALL_DATA_API_KEY=af022bc3a3554474b3495d1743300cd6
```

### Quick Start:

**Step 1: Setup**
```bash
# Copy the pre-configured env file
cp .env.football .env

# Install dependencies
pip install -r requirements.txt

# OR run setup script
python setup.sh  # Mac/Linux
python setup.bat  # Windows
```

**Step 2: Launch**
```bash
streamlit run football_app_main.py
```

**Step 3: Access**
```
http://localhost:8501
```

✅ **That's it!** Your Football app is live.

---

## 📋 YOUR FILE CHECKLIST

| File | Purpose | Status |
|------|---------|--------|
| `fix_zeus_database.py` | Fix Zeus database error | ✅ Ready |
| `fix_grade_picks_function.py` | Code-level fix for Zeus | ✅ Ready |
| `.env.football` | Pre-configured with your API key | ✅ Ready |
| `football_app_main.py` | Football Intelligence app | ✅ Ready |
| `football_data_pipeline.py` | Prediction engine | ✅ Ready |
| `requirements.txt` | Dependencies | ✅ Ready |

---

## 🔧 DETAILED FIXES EXPLAINED

### Fix 1: Database Migration (`fix_zeus_database.py`)

**What it does:**
```
1. ✅ Backs up your database (moola.db.backup_20260406_...)
2. ✅ Checks if league_id column exists
3. ✅ Adds league_id column with DEFAULT 'NBA'
4. ✅ Updates all existing records to have league_id
5. ✅ Verifies the fix worked
```

**Why this works:**
- Your `grade_picks()` function queries `SELECT id, match, league_id, kickoff...`
- The column didn't exist
- Now it exists with proper defaults
- Function will work correctly

---

### Fix 2: Code-Level Fix (`ensure_picks_log_schema()`)

**What it does:**
```python
def ensure_picks_log_schema():
    # Get current database schema
    cursor.execute("PRAGMA table_info(picks_log)")
    columns = {row[1] for row in cursor.fetchall()}
    
    # If league_id missing, add it
    if 'league_id' not in columns:
        cursor.execute("ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA'")
```

**Where to add it:**
```python
def main():
    # ADD THIS LINE AT THE VERY START:
    ensure_picks_log_schema()
    
    # ... rest of your code ...
```

This runs automatically when your app starts, fixing the schema on demand.

---

### Fix 3: Update `grade_picks()` Function

**The issue with original code:**
```python
# This fails if league_id doesn't exist:
pending = conn.execute(
    "SELECT id, match, league_id, kickoff FROM picks_log WHERE result IS NULL"
).fetchall()
```

**The fixed version:**
```python
try:
    # Try with league_id
    pending = conn.execute(
        "SELECT id, match, league_id, kickoff FROM picks_log WHERE result IS NULL"
    ).fetchall()
except Exception as e:
    if "no such column: league_id" in str(e):
        # Fall back if column doesn't exist
        pending = conn.execute(
            "SELECT id, match, NULL as league_id, kickoff FROM picks_log WHERE result IS NULL"
        ).fetchall()
    else:
        raise
```

This is **defensive programming** — it works with or without the column.

---

## 🎯 WHICH FIX TO USE?

### Use **Method 1 (Python Script)** if:
- ✅ You can run Python
- ✅ You want permanent fix
- ✅ You want automatic backup
- ✅ You want to verify everything worked

### Use **Method 2 (Code Fix)** if:
- ✅ You prefer code-level changes
- ✅ You don't want to modify database
- ✅ You want flexibility
- ✅ You understand Python

### Use **Method 3 (SQL)** if:
- ✅ You're comfortable with SQL
- ✅ You prefer direct database manipulation
- ✅ You want minimal code changes
- ✅ You have backup already

---

## ⚠️ SAFETY PRECAUTIONS

Before applying any fix:

1. **Backup your database:**
   ```bash
   cp moola.db moola.db.backup
   ```

2. **Use the automated script** (it creates backup automatically)

3. **Test in a separate environment first**

4. **Keep your backup after fix** (for at least 1 week)

---

## 📊 VERIFICATION - HOW TO CONFIRM FIX WORKED

### Option 1: Check Database Schema
```bash
sqlite3 moola.db
> PRAGMA table_info(picks_log);
```

You should see `league_id` in the list:
```
0|id|INTEGER|0||1
1|match|TEXT|0||0
2|league_id|TEXT|0|'NBA'|0  ← THIS SHOULD APPEAR
3|kickoff|DATETIME|0||0
4|result|TEXT|0||0
...
```

### Option 2: Run Your App
```bash
streamlit run zeus_app.py
```

If app starts without "no such column" error → ✅ **FIXED!**

### Option 3: Test grade_picks() Directly
```python
python
>>> from zeus_app import get_db, grade_picks
>>> result = grade_picks()
>>> print(f"Successfully graded {result} picks")
```

If no error → ✅ **FIXED!**

---

## 🚀 AFTER FIXING YOUR ZEUS APP

Once Zeus is fixed, you can:

1. **Deploy Football App** (uses your API key)
2. **Run both apps simultaneously:**
   - Zeus NBA: `streamlit run zeus_app.py --logger.level=off`
   - Football: `streamlit run football_app_main.py --server.port 8502`
3. **Integrate them together** (see integration_examples.py)

---

## 📞 TROUBLESHOOTING

### "Still getting 'no such column' error"

**Solution:**
```bash
# Verify the fix was applied
sqlite3 moola.db "PRAGMA table_info(picks_log);" | grep league_id

# If nothing appears, run the script again:
python fix_zeus_database.py

# Or manually add it:
sqlite3 moola.db "ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA';"
```

### "Python script asks for confirmation"

**Just type:**
```
yes
```

Then let it run.

### "Got permission denied error"

**On Mac/Linux:**
```bash
chmod +x fix_zeus_database.py
python fix_zeus_database.py
```

### "Database is locked"

**Your app is running. Close it first:**
```bash
# Kill the Streamlit process
pkill -f streamlit

# OR restart your terminal/IDE

# Then run the fix
python fix_zeus_database.py
```

---

## ✅ FINAL CHECKLIST

- [ ] Download `fix_zeus_database.py`
- [ ] Backup your moola.db (`cp moola.db moola.db.backup`)
- [ ] Run: `python fix_zeus_database.py`
- [ ] Answer "yes" when prompted
- [ ] Wait for completion
- [ ] Restart Zeus app: `streamlit run zeus_app.py`
- [ ] Verify no "no such column" error
- [ ] Download Football app files
- [ ] Copy `.env.football` to `.env`
- [ ] Run: `streamlit run football_app_main.py --server.port 8502`
- [ ] Access Football app at `http://localhost:8502`

---

## 🎯 NEXT STEPS

**Right now, do this:**

### Step 1: Fix Zeus (5 minutes)
```bash
python fix_zeus_database.py
```

### Step 2: Verify Fix (1 minute)
```bash
streamlit run zeus_app.py
# Should load WITHOUT "no such column" error
```

### Step 3: Deploy Football App (5 minutes)
```bash
cp .env.football .env
pip install -r requirements.txt
streamlit run football_app_main.py --server.port 8502
```

### Step 4: Enjoy Both Apps
- Zeus: `http://localhost:8501` (NBA)
- Football: `http://localhost:8502` (Over/Under)

---

**Total time: ~15 minutes**

All files are ready. Just execute the fixes and you're good! 🚀

---

Version 1.0 | April 2026 | ADONIS System
