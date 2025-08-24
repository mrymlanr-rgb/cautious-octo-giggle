import streamlit as st
import json
import os

class ProgressTracker:
    def __init__(self):
        self.progress_file = "user_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load user progress from session state or create new"""
        if 'user_progress' not in st.session_state:
            st.session_state.user_progress = {
                'completed_lessons': [],
                'completed_exercises': [],
                'quiz_scores': {},
                'total_code_runs': 0,
                'last_lesson': 1
            }
    
    def mark_lesson_completed(self, lesson_id):
        """Mark a lesson as completed"""
        if lesson_id not in st.session_state.user_progress['completed_lessons']:
            st.session_state.user_progress['completed_lessons'].append(lesson_id)
            st.session_state.user_progress['last_lesson'] = max(
                st.session_state.user_progress['last_lesson'], lesson_id + 1
            )
    
    def mark_exercise_completed(self, exercise_id):
        """Mark an exercise as completed"""
        if exercise_id not in st.session_state.user_progress['completed_exercises']:
            st.session_state.user_progress['completed_exercises'].append(exercise_id)
    
    def save_quiz_score(self, lesson_id, score):
        """Save quiz score for a lesson"""
        st.session_state.user_progress['quiz_scores'][str(lesson_id)] = score
    
    def increment_code_runs(self):
        """Increment the counter for code executions"""
        st.session_state.user_progress['total_code_runs'] += 1
    
    def get_completed_lessons_count(self):
        """Get number of completed lessons"""
        return len(st.session_state.user_progress['completed_lessons'])
    
    def get_completed_exercises_count(self):
        """Get number of completed exercises"""
        return len(st.session_state.user_progress['completed_exercises'])
    
    def get_overall_progress(self):
        """Calculate overall progress percentage"""
        total_lessons = 10  # Total number of lessons
        completed_lessons = self.get_completed_lessons_count()
        return (completed_lessons / total_lessons) * 100
    
    def is_lesson_completed(self, lesson_id):
        """Check if a lesson is completed"""
        return lesson_id in st.session_state.user_progress['completed_lessons']
    
    def is_exercise_completed(self, exercise_id):
        """Check if an exercise is completed"""
        return exercise_id in st.session_state.user_progress['completed_exercises']
    
    def get_quiz_score(self, lesson_id):
        """Get quiz score for a lesson"""
        return st.session_state.user_progress['quiz_scores'].get(str(lesson_id), 0)
    
    def get_next_lesson(self):
        """Get the next lesson to study"""
        return st.session_state.user_progress['last_lesson']
    
    def reset_progress(self):
        """Reset all progress"""
        st.session_state.user_progress = {
            'completed_lessons': [],
            'completed_exercises': [],
            'quiz_scores': {},
            'total_code_runs': 0,
            'last_lesson': 1
        }
    
    def get_progress_stats(self):
        """Get detailed progress statistics"""
        return {
            'completed_lessons': self.get_completed_lessons_count(),
            'completed_exercises': self.get_completed_exercises_count(),
            'total_code_runs': st.session_state.user_progress['total_code_runs'],
            'overall_progress': self.get_overall_progress(),
            'next_lesson': self.get_next_lesson(),
            'quiz_scores': st.session_state.user_progress['quiz_scores']
        }
