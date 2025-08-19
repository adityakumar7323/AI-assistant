import sqlite3
from datetime import datetime
import os

DATABASE = 'assistant.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create tasks/reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                task_type TEXT NOT NULL DEFAULT 'reminder',
                datetime TEXT,
                created_at TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully")
    except sqlite3.Error as e:
        print(f"❌ Database initialization error: {e}")
        raise

def add_task(content, task_type='reminder', task_datetime=None):
    """Add a new task or reminder to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO tasks (content, task_type, datetime, created_at)
            VALUES (?, ?, ?, ?)
        ''', (content, task_type, task_datetime, created_at))
        
        task_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Added {task_type}: {content}")
        return task_id
    except sqlite3.Error as e:
        print(f"❌ Error adding task: {e}")
        return None

def get_tasks():
    """Get all tasks and reminders from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE completed = FALSE 
            ORDER BY datetime ASC, created_at ASC
        ''')
        
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert to list of dictionaries for easier JSON serialization
        return [dict(task) for task in tasks]
    except sqlite3.Error as e:
        print(f"❌ Error getting tasks: {e}")
        return []

def delete_task(task_id):
    """Delete a task by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        affected_rows = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            print(f"✅ Deleted task with ID: {task_id}")
            return True
        else:
            print(f"❌ No task found with ID: {task_id}")
            return False
    except sqlite3.Error as e:
        print(f"❌ Error deleting task: {e}")
        return False

def update_task(task_id, new_content=None, new_datetime=None):
    """Update a task's content or datetime"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if new_content and new_datetime:
            cursor.execute('UPDATE tasks SET content = ?, datetime = ? WHERE id = ?', 
                         (new_content, new_datetime, task_id))
        elif new_content:
            cursor.execute('UPDATE tasks SET content = ? WHERE id = ?', (new_content, task_id))
        elif new_datetime:
            cursor.execute('UPDATE tasks SET datetime = ? WHERE id = ?', (new_datetime, task_id))
        else:
            return False
        
        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            print(f"✅ Updated task with ID: {task_id}")
            return True
        else:
            print(f"❌ No task found with ID: {task_id}")
            return False
    except sqlite3.Error as e:
        print(f"❌ Error updating task: {e}")
        return False

def mark_task_completed(task_id):
    """Mark a task as completed"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = ?', (task_id,))
        affected_rows = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            print(f"✅ Marked task {task_id} as completed")
            return True
        else:
            print(f"❌ No task found with ID: {task_id}")
            return False
    except sqlite3.Error as e:
        print(f"❌ Error marking task completed: {e}")
        return False
