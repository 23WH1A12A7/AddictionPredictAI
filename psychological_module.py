# 🧠 Psychological & Mood Analysis Module
import numpy as np
from datetime import datetime

class PsychologicalAnalyzer:
    def __init__(self):
        self.mood_questions = [
            "How often do you feel anxious without your phone?",
            "Do you feel lonely even after using social media?",
            "Does phone usage improve or worsen your mood?",
            "Do you feel stressed after long phone usage?",
            "How is your concentration level?"
        ]
        
        self.mental_health_tips = {
            "high_stress": [
                "🧘 You show signs of mental fatigue. Try a 5-minute breathing exercise.",
                "🌿 Spending time offline can help reduce anxiety.",
                "🛌 Your sleep pattern suggests mental exhaustion.",
                "✍️ Journaling your daily thoughts may improve clarity."
            ],
            "moderate_stress": [
                "🚶 Take short breaks between screen sessions.",
                "💧 Stay hydrated and maintain regular sleep patterns.",
                "🎵 Listen to calming music during phone breaks.",
                "📚 Try reading a physical book before bed."
            ],
            "low_stress": [
                "🌟 Maintain your healthy digital habits!",
                "🤝 Continue balancing online and offline activities.",
                "🎯 Set small digital wellness goals.",
                "🏆 Share your healthy habits with friends."
            ],
            "anxiety": [
                "🧘 Practice mindfulness meditation for 10 minutes daily.",
                "🌱 Consider digital detox periods during meals.",
                "💭 Track your mood before and after phone usage.",
                "👥 Connect with friends offline regularly."
            ],
            "loneliness": [
                "🤝 Schedule regular face-to-face meetings.",
                "🎯 Join local clubs or community activities.",
                "📞 Call instead of texting when possible.",
                "🌟 Engage in hobbies that don't involve screens."
            ],
            "poor_concentration": [
                "🎯 Use the Pomodoro technique: 25 min focus, 5 min break.",
                "🌿 Take nature walks without your phone.",
                "📝 Try handwriting notes instead of typing.",
                "🧩 Solve puzzles or brain games offline."
            ]
        }
    
    def analyze_mood_responses(self, responses):
        """Analyze mood questionnaire responses"""
        if len(responses) != 5:
            return None
            
        # Convert responses to numeric scores (1-5 scale)
        scores = []
        for response in responses:
            try:
                score = float(response)
                if 1 <= score <= 5:
                    scores.append(score)
                else:
                    return None
            except:
                return None
        
        # Calculate mood metrics
        avg_mood_score = np.mean(scores)
        stress_level = self._calculate_stress_level(scores)
        anxiety_level = self._calculate_anxiety_level(scores)
        concentration_level = scores[4]  # Last question is about concentration
        
        # Determine emotional state
        emotional_state = self._determine_emotional_state(avg_mood_score, stress_level, anxiety_level)
        
        return {
            "emotional_state": emotional_state,
            "mood_score": round(avg_mood_score, 2),
            "stress_level": stress_level,
            "anxiety_level": anxiety_level,
            "concentration_level": concentration_level,
            "phone_dependency": self._assess_phone_dependency(scores),
            "sleep_impact": self._assess_sleep_impact(scores)
        }
    
    def _calculate_stress_level(self, scores):
        """Calculate stress level based on responses"""
        stress_indicators = [scores[3]]  # Stress after phone usage
        if np.mean(stress_indicators) >= 4:
            return "High"
        elif np.mean(stress_indicators) >= 3:
            return "Moderate"
        else:
            return "Low"
    
    def _calculate_anxiety_level(self, scores):
        """Calculate anxiety level based on responses"""
        anxiety_indicators = [scores[0], scores[1]]  # Anxiety without phone, loneliness
        if np.mean(anxiety_indicators) >= 4:
            return "High"
        elif np.mean(anxiety_indicators) >= 3:
            return "Moderate"
        else:
            return "Low"
    
    def _determine_emotional_state(self, mood_score, stress_level, anxiety_level):
        """Determine overall emotional state"""
        if stress_level == "High" or anxiety_level == "High":
            return "Digitally Overstimulated"
        elif stress_level == "Moderate" or anxiety_level == "Moderate":
            return "Stressed"
        elif mood_score <= 2:
            return "Anxious"
        else:
            return "Calm"
    
    def _assess_phone_dependency(self, scores):
        """Assess emotional dependency on phone"""
        dependency_score = (scores[0] + scores[1]) / 2  # Anxiety + loneliness
        if dependency_score >= 4:
            return "High"
        elif dependency_score >= 3:
            return "Moderate"
        else:
            return "Low"
    
    def _assess_sleep_impact(self, scores):
        """Assess sleep-related mental fatigue"""
        # Based on stress and concentration levels
        sleep_impact = (scores[3] + (5 - scores[4])) / 2  # Stress + poor concentration
        if sleep_impact >= 4:
            return "Severe"
        elif sleep_impact >= 3:
            return "Moderate"
        else:
            return "Minimal"
    
    def get_personalized_tips(self, analysis_result):
        """Get personalized mental health tips based on analysis"""
        if not analysis_result:
            return []
        
        tips = []
        stress_level = analysis_result.get("stress_level", "Low")
        anxiety_level = analysis_result.get("anxiety_level", "Low")
        concentration_level = analysis_result.get("concentration_level", 3)
        
        # Add stress-related tips
        if stress_level == "High":
            tips.extend(self.mental_health_tips["high_stress"])
        elif stress_level == "Moderate":
            tips.extend(self.mental_health_tips["moderate_stress"])
        else:
            tips.extend(self.mental_health_tips["low_stress"])
        
        # Add specific condition tips
        if anxiety_level == "High":
            tips.extend(self.mental_health_tips["anxiety"][:2])
        
        if concentration_level <= 2:  # Poor concentration
            tips.extend(self.mental_health_tips["poor_concentration"][:2])
        
        return tips[:4]  # Return top 4 most relevant tips
    
    def get_interaction_suggestions(self, analysis_result):
        """Get AI-based interaction suggestions"""
        if not analysis_result:
            return []
        
        stress_level = analysis_result.get("stress_level", "Low")
        emotional_state = analysis_result.get("emotional_state", "Calm")
        
        suggestions = {
            "Digitally Overstimulated": [
                "🚶 Short walk without phone",
                "🎵 Music break (no screen)",
                "🌿 5-minute breathing exercise",
                "💧 Hydration break"
            ],
            "Stressed": [
                "🧘 2-minute meditation",
                "📖 Read a physical page",
                "👁️ Eye relaxation exercise",
                "🌱 Plant care activity"
            ],
            "Anxious": [
                "🤝 Call a friend",
                "📝 Write down thoughts",
                "🎨 Creative activity",
                "🏃 Physical movement"
            ],
            "Calm": [
                "🎯 Set wellness goal",
                "📚 Learn something new",
                "🎵 Enjoy favorite music",
                "🌟 Practice gratitude"
            ]
        }
        
        return suggestions.get(emotional_state, suggestions["Calm"])
    
    def generate_digital_detox_plans(self):
        """Generate digital detox planner options"""
        return {
            "30_min": {
                "title": "30-Minute Digital Detox",
                "benefits": [
                    "Reduced eye strain",
                    "Improved focus",
                    "Mental clarity boost",
                    "Stress reduction"
                ],
                "activities": [
                    "Stretch and move",
                    "Drink water mindfully",
                    "Look out window",
                    "Deep breathing"
                ]
            },
            "1_hour": {
                "title": "1-Hour Digital Detox",
                "benefits": [
                    "Enhanced creativity",
                    "Better mood",
                    "Improved sleep preparation",
                    "Social connection boost"
                ],
                "activities": [
                    "Walk outdoors",
                    "Read physical book",
                    "Cook or bake",
                    "Call loved one"
                ]
            },
            "night_detox": {
                "title": "Night Digital Detox",
                "benefits": [
                    "Better sleep quality",
                    "Reduced blue light exposure",
                    "Hormone balance",
                    "Morning freshness"
                ],
                "activities": [
                    "Journaling",
                    "Meditation",
                    "Warm bath",
                    "Herbal tea"
                ]
            }
        }
