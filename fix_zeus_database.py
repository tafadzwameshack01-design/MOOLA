#!/usr/bin/env python3
# ============================================================================
# ZEUS NBA APP - DATABASE MIGRATION FIX
# ============================================================================
# This script fixes the "no such column: league_id" error
# Run this ONCE to migrate your database schema

import sqlite3
import sys
from datetime import datetime

def migrate_database(db_path="moola.db"):
    """Fix missing league_id column in picks_log table"""
    
    print("🔧 ZEUS DATABASE MIGRATION")
    print("=" * 60)
    print(f"Database: {db_path}")
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='picks_log'")
        if not cursor.fetchone():
            print("❌ picks_log table doesn't exist!")
            return False
        
        # Check if league_id column exists
        cursor.execute("PRAGMA table_info(picks_log)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'league_id' in columns:
            print("✅ league_id column already exists - no migration needed")
            conn.close()
            return True
        
        print("🔍 Current picks_log schema:")
        cursor.execute("PRAGMA table_info(picks_log)")
        for row in cursor.fetchall():
            print(f"   • {row[1]} ({row[2]})")
        print()
        
        # Add league_id column with default value
        print("➕ Adding league_id column...")
        cursor.execute("ALTER TABLE picks_log ADD COLUMN league_id TEXT DEFAULT 'NBA'")
        print("✅ league_id column added")
        
        # Update existing records
        print("🔄 Updating existing records...")
        cursor.execute("UPDATE picks_log SET league_id = 'NBA' WHERE league_id IS NULL")
        updated = cursor.rowcount
        print(f"✅ Updated {updated} records")
        
        # Make league_id NOT NULL
        print("🔒 Setting constraints...")
        cursor.execute("ALTER TABLE picks_log MODIFY league_id TEXT NOT NULL DEFAULT 'NBA'")
        print("✅ Column constraints set")
        
        # Verify the fix
        print()
        print("🔍 Updated picks_log schema:")
        cursor.execute("PRAGMA table_info(picks_log)")
        for row in cursor.fetchall():
            print(f"   • {row[1]} ({row[2]})")
        
        # Commit changes
        conn.commit()
        print()
        print("=" * 60)
        print("✅ DATABASE MIGRATION COMPLETE")
        print("=" * 60)
        print()
        print("You can now restart your Zeus app:")
        print("   streamlit run zeus_app.py")
        print()
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def backup_database(db_path="moola.db"):
    """Create backup before migration"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
        return None

if __name__ == "__main__":
    db_file = "moola.db"
    
    # Check if custom path provided
    if len(sys.argv) > 1:
        db_file = sys.argv[1]
    
    print()
    print("=" * 60)
    print("⚠️  BACKUP YOUR DATABASE FIRST!")
    print("=" * 60)
    print()
    
    # Create backup
    backup_path = backup_database(db_file)
    print()
    
    # Ask for confirmation
    response = input("Ready to migrate? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Migration cancelled")
        sys.exit(1)
    
    print()
    
    # Run migration
    success = migrate_database(db_file)
    
    if success:
        print()
        print("🚀 NEXT STEPS:")
        print("   1. Restart your Streamlit app")
        print("   2. The grade_picks() function should now work")
        print("   3. Check the logs for any remaining errors")
        sys.exit(0)
    else:
        print()
        print("⚠️  Migration failed. Restore from backup if needed:")
        if backup_path:
            print(f"   cp {backup_path} {db_file}")
        sys.exit(1)
