# ============================================================================
# ZEUS NBA APP - CODE FIX FOR MISSING league_id COLUMN
# ============================================================================
# Replace your existing grade_picks() function with this version
# This version gracefully handles the missing league_id column

def grade_picks():
    """
    Grade pending picks by checking actual match results.
    A pick is graded WON if the match total > 2.5, LOST otherwise.
    
    FIXED: Handles missing league_id column
    """
    conn = get_db()
    
    # Try to query with league_id first, fall back if column doesn't exist
    try:
        # Try with league_id (newer schema)
        pending = conn.execute(
            "SELECT id, match, league_id, kickoff FROM picks_log WHERE result IS NULL ORDER BY kickoff"
        ).fetchall()
    except Exception as e:
        if "no such column: league_id" in str(e):
            print("⚠️  league_id column missing - using fallback query")
            # Fall back to query without league_id (older schema)
            pending = conn.execute(
                "SELECT id, match, NULL as league_id, kickoff FROM picks_log WHERE result IS NULL ORDER BY kickoff"
            ).fetchall()
        else:
            raise
    
    updated = 0
    for pick_id, match_str, league_id, kickoff_str in pending:
        try:
            # Parse match string (e.g., "Knicks vs Celtics")
            parts = [p.strip() for p in match_str.split(' vs ')]
            if len(parts) != 2:
                continue
            
            home_team, away_team = parts
            
            # Fetch game data and calculate total goals/points
            # This is YOUR existing logic - we're just making league_id optional
            total = fetch_and_calculate_total(home_team, away_team)
            
            if total is None:
                continue
            
            # Determine result
            result = "WON" if total > 2.5 else "LOST"
            
            # Update record
            conn.execute(
                "UPDATE picks_log SET result = ? WHERE id = ?",
                (result, pick_id)
            )
            updated += 1
        
        except Exception as e:
            print(f"Error grading pick {pick_id}: {e}")
            continue
    
    if updated > 0:
        conn.commit()
    
    return updated


# ============================================================================
# INSTANT FIX - Add this SQL to Zeus app startup
# ============================================================================
# Add this function to your zeus_app.py and call it at app startup

def ensure_picks_log_schema():
    """Ensure picks_log table has all required columns - run at startup"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get current schema
    cursor.execute("PRAGMA table_info(picks_log)")
    columns = {row[1] for row in cursor.fetchall()}
    
    # Add missing columns if needed
    if 'league_id' not in columns:
        try:
            cursor.execute("ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA'")
            conn.commit()
            print("✅ Fixed: Added league_id column to picks_log")
        except Exception as e:
            print(f"⚠️  Could not add league_id: {e}")
    
    if 'confidence' not in columns:
        try:
            cursor.execute("ALTER TABLE picks_log ADD COLUMN confidence REAL DEFAULT 0.85")
            conn.commit()
            print("✅ Fixed: Added confidence column to picks_log")
        except Exception as e:
            print(f"⚠️  Could not add confidence: {e}")
    
    conn.close()


# ============================================================================
# IMPLEMENTATION - Add to your main() function
# ============================================================================
# In your main() function, at the very beginning, add:

def main():
    # FIX: Ensure database schema is correct
    ensure_picks_log_schema()
    
    # ... rest of your main() code ...
    pass


# ============================================================================
# FULL GRADE_PICKS REPLACEMENT
# ============================================================================
# If you want to completely replace the grade_picks function:

import sqlite3
from typing import Optional

def grade_picks_v2() -> int:
    """
    Grade pending picks by checking actual match results.
    A pick is graded WON if the match total > 2.5, LOST otherwise.
    
    VERSION 2 - Fully compatible with missing columns
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Check what columns exist
    cursor.execute("PRAGMA table_info(picks_log)")
    columns = {row[1] for row in cursor.fetchall()}
    
    # Build dynamic query based on available columns
    select_cols = ["id", "match", "kickoff"]
    if 'league_id' in columns:
        select_cols.insert(2, "league_id")
    else:
        select_cols.insert(2, "NULL as league_id")
    
    query = f"SELECT {', '.join(select_cols)} FROM picks_log WHERE result IS NULL ORDER BY kickoff"
    
    try:
        pending = cursor.execute(query).fetchall()
    except Exception as e:
        print(f"❌ Query failed: {e}")
        print(f"   Query was: {query}")
        return 0
    
    updated = 0
    
    for row in pending:
        if len(row) == 4:
            pick_id, match_str, league_id, kickoff_str = row
        else:
            pick_id, match_str, kickoff_str = row
            league_id = 'NBA'
        
        try:
            # Parse match string
            parts = [p.strip() for p in match_str.split(' vs ')]
            if len(parts) != 2:
                continue
            
            home_team, away_team = parts
            
            # Get game total (your existing logic)
            # This is where you fetch from API or database
            total_goals = get_match_total(home_team, away_team)
            
            if total_goals is None:
                continue
            
            # Grade the pick
            result = "WON" if total_goals > 2.5 else "LOST"
            
            # Update database
            cursor.execute(
                "UPDATE picks_log SET result = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (result, pick_id)
            )
            updated += 1
            
        except Exception as e:
            print(f"⚠️  Error grading pick {pick_id}: {e}")
            continue
    
    if updated > 0:
        conn.commit()
    
    conn.close()
    return updated


# ============================================================================
# SQL ALTERNATIVE - Direct SQL migration
# ============================================================================
# If you prefer to run SQL directly in SQLite:

SQL_MIGRATION = """
-- Check current schema
PRAGMA table_info(picks_log);

-- Add missing league_id column (if it doesn't exist)
ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA';

-- Add missing confidence column (if it doesn't exist) 
ALTER TABLE picks_log ADD COLUMN confidence REAL DEFAULT 0.85;

-- Add updated_at column for tracking
ALTER TABLE picks_log ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;

-- Verify new schema
PRAGMA table_info(picks_log);
"""

# Run like this in SQLite CLI:
# sqlite3 moola.db < migration.sql
