import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "wellness_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Mood entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                mood TEXT,
                score REAL,
                note TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Wellness tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wellness_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                task_name TEXT,
                points INTEGER,
                completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP,
                date DATE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Streak tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_activity_date DATE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Screen time tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screen_time (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                date DATE,
                hours REAL,
                app_sessions INTEGER,
                notifications INTEGER,
                night_usage REAL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Sleep tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sleep_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                date DATE,
                quality_score REAL,
                hours_slept REAL,
                bedtime TIME,
                wake_time TIME,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Education progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS education_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                article_id INTEGER,
                path_level TEXT,
                completed BOOLEAN DEFAULT FALSE,
                completion_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # User goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                goal_type TEXT,
                target_value REAL,
                current_value REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_user(self, user_id: str) -> int:
        """Get existing user or create new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            # Initialize streak for new user
            cursor.execute("INSERT INTO streaks (user_id, current_streak, longest_streak) VALUES (?, 0, 0)", (user_id,))
        
        conn.commit()
        conn.close()
        return result[0] if result else None
    
    def save_mood_entry(self, user_id: str, mood: str, score: float, note: str = None) -> bool:
        """Save mood entry and update streak"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Save mood entry
            cursor.execute('''
                INSERT INTO mood_entries (user_id, mood, score, note) 
                VALUES (?, ?, ?, ?)
            ''', (user_id, mood, score, note))
            
            # Update streak
            self._update_streak(cursor, user_id)
            
            # Update last active
            cursor.execute('''
                UPDATE users SET last_active = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving mood entry: {e}")
            return False
        finally:
            conn.close()
    
    def _update_streak(self, cursor, user_id: str):
        """Update user streak based on daily activity"""
        today = datetime.now().date()
        
        cursor.execute('''
            SELECT last_activity_date, current_streak, longest_streak 
            FROM streaks WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        if not result:
            return
        
        last_activity, current_streak, longest_streak = result
        
        if last_activity:
            last_date = datetime.strptime(last_activity, '%Y-%m-%d').date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Already updated today
                return
            elif days_diff == 1:
                # Consecutive day
                new_streak = current_streak + 1
            else:
                # Streak broken
                new_streak = 1
        else:
            # First activity
            new_streak = 1
        
        # Update streak
        cursor.execute('''
            UPDATE streaks 
            SET current_streak = ?, longest_streak = ?, last_activity_date = ?
            WHERE user_id = ?
        ''', (new_streak, max(longest_streak, new_streak), today, user_id))
    
    def get_streak_data(self, user_id: str) -> Dict:
        """Get current streak data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT current_streak, longest_streak, last_activity_date 
            FROM streaks WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            current_streak, longest_streak, last_activity = result
            
            # Calculate completion rate for this week
            completion_rate = self._calculate_weekly_completion(user_id)
            
            return {
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'last_activity': last_activity,
                'completion_rate': completion_rate
            }
        
        return {'current_streak': 0, 'longest_streak': 0, 'completion_rate': 0}
    
    def _calculate_weekly_completion(self, user_id: str) -> float:
        """Calculate weekly task completion rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        week_ago = (datetime.now() - timedelta(days=7)).date()
        
        cursor.execute('''
            SELECT COUNT(*) as total_tasks,
                   SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_tasks
            FROM wellness_tasks 
            WHERE user_id = ? AND date >= ?
        ''', (user_id, week_ago))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] > 0:
            return round((result[1] / result[0]) * 100, 0)
        
        return 0
    
    def save_wellness_task(self, user_id: str, task_name: str, points: int, completed: bool = True) -> bool:
        """Save wellness task completion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            today = datetime.now().date()
            
            # Check if task already exists for today
            cursor.execute('''
                SELECT id FROM wellness_tasks 
                WHERE user_id = ? AND task_name = ? AND date = ?
            ''', (user_id, task_name, today))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing task
                cursor.execute('''
                    UPDATE wellness_tasks 
                    SET completed = ?, completed_at = ?, points = ?
                    WHERE id = ?
                ''', (completed, datetime.now() if completed else None, points, existing[0]))
            else:
                # Insert new task
                cursor.execute('''
                    INSERT INTO wellness_tasks (user_id, task_name, points, completed, completed_at, date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, task_name, points, completed, datetime.now() if completed else None, today))
            
            # Update streak if completed
            if completed:
                self._update_streak(cursor, user_id)
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving wellness task: {e}")
            return False
        finally:
            conn.close()
    
    def get_wellness_tasks(self, user_id: str) -> List[Dict]:
        """Get wellness tasks for today"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            SELECT task_name, points, completed, completed_at
            FROM wellness_tasks 
            WHERE user_id = ? AND date = ?
            ORDER BY task_name
        ''', (user_id, today))
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'title': row[0],
                'points': row[1],
                'completed': bool(row[2]),
                'completed_at': row[3]
            })
        
        # If no tasks for today, return default tasks
        if not tasks:
            default_tasks = [
                {"title": "No Phone Before Bed", "points": 10, "completed": False},
                {"title": "Real Connection", "points": 15, "completed": False},
                {"title": "Read Offline", "points": 20, "completed": False},
                {"title": "Stretch Break", "points": 25, "completed": False},
                {"title": "Notification Detox", "points": 30, "completed": False},
                {"title": "Nature Time", "points": 35, "completed": False}
            ]
            conn.close()
            return default_tasks
        
        conn.close()
        return tasks
    
    def get_historical_data(self, user_id: str, days: int = 7) -> Dict:
        """Get historical data for dashboard charts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).date()
        
        # Mood trend data
        cursor.execute('''
            SELECT DATE(timestamp) as date, AVG(score) as avg_score
            FROM mood_entries 
            WHERE user_id = ? AND DATE(timestamp) >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (user_id, start_date))
        
        mood_data = []
        for row in cursor.fetchall():
            mood_data.append({
                'date': self._format_date_label(row[0], days),
                'value': round(row[1], 1)
            })
        
        # If no mood data, generate sample data
        if not mood_data:
            mood_data = self._generate_sample_data(days, 'mood')
        
        # Screen time data
        cursor.execute('''
            SELECT date, hours FROM screen_time 
            WHERE user_id = ? AND date >= ?
            ORDER BY date
        ''', (user_id, start_date))
        
        screen_time_data = []
        existing_dates = set()
        
        for row in cursor.fetchall():
            screen_time_data.append({
                'date': self._format_date_label(row[0], days),
                'value': row[1] * 10  # Convert to match chart scale
            })
            existing_dates.add(row[0])
        
        # Fill missing dates with sample data, but keep real data
        if len(screen_time_data) < days:
            all_dates = [(datetime.now() - timedelta(days=days-i-1)).date() for i in range(days)]
            for date in all_dates:
                if date not in existing_dates:
                    screen_time_data.append({
                        'date': self._format_date_label(date, days),
                        'value': random.uniform(20, 80)  # Chart scale
                    })
        
        # Sort by date
        screen_time_data.sort(key=lambda x: x['date'])
        
        # Sleep data
        cursor.execute('''
            SELECT date, quality_score FROM sleep_data 
            WHERE user_id = ? AND date >= ?
            ORDER BY date
        ''', (user_id, start_date))
        
        sleep_data = []
        existing_sleep_dates = set()
        
        for row in cursor.fetchall():
            sleep_data.append({
                'date': self._format_date_label(row[0], days),
                'value': row[1]
            })
            existing_sleep_dates.add(row[0])
        
        # Fill missing dates with sample data, but keep real data
        if len(sleep_data) < days:
            all_dates = [(datetime.now() - timedelta(days=days-i-1)).date() for i in range(days)]
            for date in all_dates:
                if date not in existing_sleep_dates:
                    sleep_data.append({
                        'date': self._format_date_label(date, days),
                        'value': random.uniform(5, 9)
                    })
        
        # Sort by date
        sleep_data.sort(key=lambda x: x['date'])
        
        conn.close()
        
        return {
            'mood_trend': mood_data,
            'stress_vs_screen_time': screen_time_data,
            'sleep_vs_mental_fatigue': sleep_data,
            'usage_vs_concentration': self._generate_focus_data(days)
        }

    def _format_date_label(self, date_input, days: int) -> str:
        """Format date label based on the period"""
        # Convert string to date object if needed
        if isinstance(date_input, str):
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date_input, '%Y-%m-%d').date()
            except:
                # If parsing fails, use today's date
                date_obj = datetime.now().date()
        else:
            date_obj = date_input
        
        if days >= 30:
            # For month view, show month abbreviations
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return month_names[date_obj.month - 1]
        else:
            # For week view, show day abbreviations
            return date_obj.strftime('%a')

    def _generate_sample_data(self, days: int, data_type: str) -> List[Dict]:
        """Generate sample data for demonstration"""
        import random
        data = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i-1)).date()
            date_label = self._format_date_label(date, days)
            
            if data_type == 'mood':
                value = random.uniform(2.5, 5.0)
            elif data_type == 'screen_time':
                value = random.uniform(20, 80)  # Chart scale
            elif data_type == 'sleep':
                value = random.uniform(5, 9)
            else:
                value = random.uniform(1, 10)
            
            data.append({
                'date': date_label,
                'value': round(value, 1)
            })
        
        return data
    
    def _generate_focus_data(self, days: int) -> List[Dict]:
        """Generate focus data based on recent activity"""
        import random
        data = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i-1)).date()
            date_label = self._format_date_label(date, days)
            data.append({
                'date': date_label,
                'value': random.uniform(1, 10)
            })
        return data
    
    def save_screen_time(self, user_id: str, hours: float, app_sessions: int = 0, notifications: int = 0, night_usage: float = 0):
        """Save screen time data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        # Check if entry exists for today
        cursor.execute('''
            SELECT id FROM screen_time 
            WHERE user_id = ? AND date = ?
        ''', (user_id, today))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE screen_time 
                SET hours = ?, app_sessions = ?, notifications = ?, night_usage = ?
                WHERE user_id = ? AND date = ?
            ''', (hours, app_sessions, notifications, night_usage, user_id, today))
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO screen_time (user_id, date, hours, app_sessions, notifications, night_usage)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, today, hours, app_sessions, notifications, night_usage))
        
        conn.commit()
        conn.close()
        
    def get_dashboard_metrics(self, user_id: str) -> Dict:
        """Calculate dashboard metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent mood average
        cursor.execute('''
            SELECT AVG(score) as avg_mood 
            FROM mood_entries 
            WHERE user_id = ? AND timestamp >= datetime('now', '-7 days')
        ''', (user_id,))
        
        mood_result = cursor.fetchone()
        avg_mood = mood_result[0] if mood_result and mood_result[0] else 3.5
        
        # Get today's screen time
        today = datetime.now().date()
        cursor.execute('''
            SELECT hours FROM screen_time 
            WHERE user_id = ? AND date = ?
        ''', (user_id, today))
        
        screen_time_result = cursor.fetchone()
        daily_screen_time = screen_time_result[0] if screen_time_result else 0
        
        # Get wellness score
        streak_data = self.get_streak_data(user_id)
        
        # Calculate overall wellbeing score
        wellbeing_score = min(95, round(
            (avg_mood / 5.0) * 40 +  # Mood contribution
            streak_data['completion_rate'] * 0.4 +  # Streak contribution
            (1 - min(daily_screen_time / 8, 1)) * 20  # Screen time contribution
        ))
        
        conn.close()
        
        return {
            'wellbeing_score': wellbeing_score,
            'avg_mood': round(avg_mood, 1),
            'daily_screen_time': daily_screen_time,
            'streak': streak_data['current_streak'],
            'completion_rate': streak_data['completion_rate']
        }
    
    def save_education_progress(self, user_id: str, article_id: int, path_level: str) -> bool:
        """Save education progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO education_progress 
                (user_id, article_id, path_level, completed, completion_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, article_id, path_level, True, datetime.now()))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving education progress: {e}")
            return False
        finally:
            conn.close()
    
    def get_education_progress(self, user_id: str) -> Dict:
        """Get education progress data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT path_level, COUNT(*) as completed
            FROM education_progress 
            WHERE user_id = ? AND completed = 1
            GROUP BY path_level
        ''', (user_id,))
        
        progress = {}
        for row in cursor.fetchall():
            progress[row[0]] = row[1]
        
        conn.close()
        return progress

# Global database instance
db = DatabaseManager()
