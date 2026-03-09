# 🧠 AI-Based Digital Addiction Predictor

A comprehensive psychological and behavioral analysis system for digital addiction prediction with mental health support features.

## 🌟 Features Overview

### 1️⃣ **Core Prediction Module**
- **Machine Learning Model**: Random Forest classifier trained on digital usage patterns
- **Risk Assessment**: Predicts digital addiction levels with confidence scores
- **Behavioral Analysis**: Analyzes screen time, app usage, notifications, and night usage

### 2️⃣ **Psychological & Mood Analysis**
- **Human-Centered Questions**: Instead of direct addiction questions
- **Emoji-Based Interface**: Likert scale with visual feedback
- **Emotional State Detection**: Calm, Stressed, Anxious, Digitally Overstimulated
- **Psychological Indicators**: Phone dependency, stress levels, concentration issues

### 3️⃣ **Personalized Mental Health Tips**
- **Smart Suggestions**: Based on addiction level, mood score, and stress indicators
- **Categorized Recommendations**: High stress, moderate stress, anxiety-specific tips
- **Actionable Advice**: Breathing exercises, digital detox, journaling suggestions

### 4️⃣ **AI-Based Interaction & Guidance**
- **Rule-Based Suggestions**: Context-aware activity recommendations
- **Digital Detox Planner**: 30-min, 1-hour, and night detox programs
- **Progress Tracking**: Real-time detox completion with benefits display
- **Interactive Engagement**: Accept/skip mechanism for user control

### 5️⃣ **Psychological Dashboard**
- **Interactive Charts**: Stress vs Screen Time, Mood Trends, Sleep Analysis
- **Visual Analytics**: Usage patterns vs concentration levels
- **Progress Monitoring**: Weekly trends and insights
- **Data Visualization**: Chart.js integration for dynamic graphs

### 6️⃣ **Self-Improvement & Wellness**
- **Daily Tasks**: 6 wellness activities with point system
- **Reflection Module**: Mood and focus tracking questions
- **Streak Calendar**: Visual progress tracking
- **Achievement System**: Gamification with rewards and notifications

### 7️⃣ **Awareness & Education**
- **Educational Content**: Effects of digital addiction on mental health
- **Dopamine Science**: Simple explanations of phone addiction mechanisms
- **Sleep Health**: Blue light effects and sleep hygiene
- **Interactive Quiz**: Knowledge testing with feedback

### 8️⃣ **Ethical & Safety Features**
- **Medical Disclaimer**: Clear statement about educational purpose
- **Professional Resources**: Links to mental health support
- **Responsible AI**: Transparent about limitations
- **User Safety**: Crisis information and guidance

### 9️⃣ **Advanced Features**
- **Emotional Check-Ins**: Periodic mood monitoring with popups
- **Motivational Insights**: Context-aware encouraging messages
- **Session Management**: User data tracking across modules
- **Responsive Design**: Mobile-friendly interface

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- scikit-learn
- pandas
- numpy
- joblib

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install flask scikit-learn pandas numpy joblib
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open browser to `http://127.0.0.1:5000`

## 📊 Project Structure

```
Phone-Addiction-Prediction/
├── app.py                    # Main Flask application
├── model.py                  # ML model training script
├── psychological_module.py     # Psychological analysis engine
├── templates/
│   ├── index.html            # Main prediction page
│   ├── mood_analysis.html     # Psychological assessment
│   ├── dashboard.html         # Analytics dashboard
│   ├── wellness.html         # Self-improvement features
│   ├── detox_plans.html     # Digital detox programs
│   └── education.html       # Educational content
├── static/
│   ├── style.css            # Styling
│   └── emotional-checkin.js # Check-in system
├── random_forest_addiction_model.pkl  # Trained ML model
└── mobile_phone_addiction_dataset.csv   # Training data
```

## 🎯 Usage Guide

### Step 1: Initial Assessment
1. Enter your digital usage data on the main page
2. Receive addiction prediction with confidence level
3. Get your session ID for tracking

### Step 2: Psychological Analysis
1. Complete the mood questionnaire with emoji-based responses
2. Receive personalized mental health tips
3. View AI-based interaction suggestions

### Step 3: Digital Detox
1. Choose from 30-min, 1-hour, or night detox plans
2. Follow guided activities during detox
3. Track completion and receive feedback

### Step 4: Wellness Activities
1. Complete daily wellness tasks
2. Track mood and reflections
3. Monitor progress with streak calendar

### Step 5: Dashboard Insights
1. View psychological trends and patterns
2. Analyze stress vs screen time correlations
3. Monitor progress over time

## 🔧 Technical Implementation

### Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Features**: 6 behavioral metrics
- **Training**: 80/20 train-test split
- **Performance**: Optimized for balanced accuracy

### Psychological Analysis
- **Scoring System**: 1-5 Likert scale conversion
- **Emotional States**: Multi-factor assessment
- **Personalization**: Context-aware tip generation
- **Safety**: Non-diagnostic approach

### Frontend Features
- **Responsive Design**: Mobile-first approach
- **Interactive Elements**: Real-time feedback
- **Data Visualization**: Chart.js integration
- **User Experience**: Smooth transitions and animations

## 🛡️ Ethical Considerations

### Medical Disclaimer
- Educational purpose only
- Not a substitute for professional medical advice
- Encourages professional consultation for severe cases

### Data Privacy
- Session-based data storage
- No persistent personal data collection
- Local storage for demo purposes only

### Responsible AI
- Transparent about limitations
- Avoids definitive medical claims
- Provides resources for professional help

## 📈 Future Enhancements

### Planned Features
- [ ] Real wearable device integration
- [ ] Multi-language support
- [ ] Advanced ML models
- [ ] Professional healthcare API integration
- [ ] Mobile application development

### Research Opportunities
- [ ] Clinical validation studies
- [ ] Long-term user behavior analysis
- [ ] Cross-cultural adaptation
- [ ] Effectiveness measurement

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper documentation
4. Submit pull request with detailed description

## 📄 License

This project is for educational and research purposes. Please ensure compliance with healthcare regulations in your region.

## 📞 Support

For technical issues:
- Check the troubleshooting section
- Review the documentation
- Create an issue with detailed description

For mental health support:
- Contact local healthcare professionals
- Use emergency services for crises
- Access provided mental health resources

---

**Note**: This system demonstrates the integration of machine learning with psychological principles for digital wellbeing. Always prioritize professional medical advice for mental health concerns.
