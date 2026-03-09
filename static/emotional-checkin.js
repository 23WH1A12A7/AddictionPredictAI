// Emotional Check-in and Motivational Insights System
class EmotionalCheckIn {
    constructor() {
        this.motivationalQuotes = [
            "Every small step towards digital wellness is a victory for your mental health.",
            "Your mind is a garden, your thoughts are the seeds. You can grow flowers or weeds.",
            "Digital wellbeing isn't about perfection, it's about progress.",
            "Taking breaks from technology is not laziness, it's intelligence.",
            "Your relationship with technology should serve you, not control you.",
            "Balance is not something you find, it's something you create.",
            "The present moment is the only time over which we have dominion.",
            "Digital detox is not about disconnecting from the world, but reconnecting with yourself.",
            "Your mental health is more important than your screen time.",
            "Every time you choose presence over distraction, you win."
        ];
        
        this.encouragingMessages = [
            "Great job taking care of your digital wellbeing! 🌟",
            "You're making positive changes for your mental health! 💪",
            "Your commitment to digital wellness is inspiring! 🎯",
            "Keep going - you're building healthier habits! 🌱",
            "Your mind will thank you for this digital break! 🧘",
            "You're on the path to digital freedom! 🦋",
            "Every mindful choice matters! ✨",
            "Your future self will appreciate these changes! 🌈",
            "You're stronger than digital distractions! 💎",
            "Wellness is a journey, not a destination! 🚶"
        ];
        
        this.checkInQuestions = [
            "How are you feeling right now?",
            "What's your energy level today?",
            "How's your focus been today?",
            "Are you feeling overwhelmed or balanced?",
            "How's your stress level right now?"
        ];
        
        this.init();
    }
    
    init() {
        setTimeout(() => this.showCheckIn(), 30000);
        
        setInterval(() => this.showCheckIn(), 600000);
        
        setInterval(() => this.showMotivationalInsight(), 450000);
        
        this.addCheckInButton();
    }
    
    addCheckInButton() {
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu) {
            const checkInBtn = document.createElement('a');
            checkInBtn.href = '#';
            checkInBtn.className = 'nav-link';
            checkInBtn.innerHTML = '<i class="fa-solid fa-heart"></i> Check In';
            checkInBtn.onclick = (e) => {
                e.preventDefault();
                this.showCheckIn();
            };
            navMenu.appendChild(checkInBtn);
        }
    }
    
    showCheckIn() {
        if (document.querySelector('.check-in-modal, .detox-modal')) {
            return;
        }
        
        const question = this.checkInQuestions[Math.floor(Math.random() * this.checkInQuestions.length)];
        
        const modal = document.createElement('div');
        modal.className = 'check-in-modal';
        modal.innerHTML = `
            <div class="check-in-content">
                <div class="check-in-header">
                    <i class="fa-solid fa-heart"></i>
                    <h3>Emotional Check-in</h3>
                </div>
                <p class="check-in-question">${question}</p>
                <div class="mood-options">
                    <div class="mood-option" onclick="emotionalCheckIn.selectMood(this, 'amazing')">
                        <span class="mood-emoji">😄</span>
                        <span class="mood-label">Amazing</span>
                    </div>
                    <div class="mood-option" onclick="emotionalCheckIn.selectMood(this, 'good')">
                        <span class="mood-emoji">😊</span>
                        <span class="mood-label">Good</span>
                    </div>
                    <div class="mood-option" onclick="emotionalCheckIn.selectMood(this, 'okay')">
                        <span class="mood-emoji">😐</span>
                        <span class="mood-label">Okay</span>
                    </div>
                    <div class="mood-option" onclick="emotionalCheckIn.selectMood(this, 'low')">
                        <span class="mood-emoji">😔</span>
                        <span class="mood-label">Low</span>
                    </div>
                    <div class="mood-option" onclick="emotionalCheckIn.selectMood(this, 'struggling')">
                        <span class="mood-emoji">😢</span>
                        <span class="mood-label">Struggling</span>
                    </div>
                </div>
                <div class="check-in-actions">
                    <button class="skip-btn" onclick="emotionalCheckIn.skipCheckIn()">Skip</button>
                    <button class="later-btn" onclick="emotionalCheckIn.laterCheckIn()">Later</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        this.addCheckInStyles();
        
        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }
    
    selectMood(element, mood) {
        const modal = document.querySelector('.check-in-modal');
        const message = this.getEncouragingMessage(mood);
        
        this.showNotification(message, mood);
        
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
        
        this.storeMoodData(mood);
    }
    
    getEncouragingMessage(mood) {
        const messages = {
            'amazing': "That's wonderful! Keep spreading that positive energy! 🌟",
            'good': "Great to hear you're feeling good! Keep it up! 💪",
            'okay': "Sometimes okay is exactly where we need to be. You've got this! 🌱",
            'low': "It's okay to have low moments. Be gentle with yourself. 🤗",
            'struggling': "Thank you for being honest. You're stronger than you know. Reach out if you need support. 💙"
        };
        
        return messages[mood] || messages['okay'];
    }
    
    skipCheckIn() {
        const modal = document.querySelector('.check-in-modal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
    }
    
    laterCheckIn() {
        this.skipCheckIn();
        setTimeout(() => this.showCheckIn(), 300000);
    }
    
    showMotivationalInsight() {
        const quote = this.motivationalQuotes[Math.floor(Math.random() * this.motivationalQuotes.length)];
        this.showNotification(quote, 'motivation');
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `motivation-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fa-solid fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        this.addNotificationStyles();
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    getNotificationIcon(type) {
        const icons = {
            'amazing': 'star',
            'good': 'smile',
            'okay': 'meh',
            'low': 'heart',
            'struggling': 'hands-helping',
            'motivation': 'lightbulb'
        };
        return icons[type] || 'info-circle';
    }
    
    storeMoodData(mood) {
        const moodData = {
            mood: mood,
            timestamp: new Date().toISOString(),
            page: window.location.pathname
        };
        
        let moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');
        moodHistory.push(moodData);
        
        if (moodHistory.length > 50) {
            moodHistory = moodHistory.slice(-50);
        }
        
        localStorage.setItem('moodHistory', JSON.stringify(moodHistory));
    }
    
    addCheckInStyles() {
        if (document.getElementById('checkin-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'checkin-styles';
        styles.textContent = `
            .check-in-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .check-in-modal.show {
                opacity: 1;
            }
            
            .check-in-content {
                background: linear-gradient(135deg, #1e293b, #0f172a);
                border-radius: 16px;
                padding: 32px;
                max-width: 400px;
                width: 90%;
                border: 1px solid rgba(56, 189, 248, 0.2);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            }
            
            .check-in-header {
                text-align: center;
                margin-bottom: 20px;
            }
            
            .check-in-header i {
                font-size: 32px;
                color: #38bdf8;
                margin-bottom: 8px;
            }
            
            .check-in-header h3 {
                margin: 0;
                color: #38bdf8;
                font-size: 20px;
            }
            
            .check-in-question {
                text-align: center;
                color: #e5e7eb;
                font-size: 16px;
                margin-bottom: 24px;
            }
            
            .mood-options {
                display: flex;
                justify-content: space-around;
                margin-bottom: 24px;
            }
            
            .mood-option {
                text-align: center;
                cursor: pointer;
                padding: 12px;
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            
            .mood-option:hover {
                background: rgba(56, 189, 248, 0.1);
                transform: scale(1.05);
            }
            
            .mood-emoji {
                font-size: 32px;
                display: block;
                margin-bottom: 4px;
            }
            
            .mood-label {
                font-size: 12px;
                color: #94a3b8;
            }
            
            .check-in-actions {
                display: flex;
                gap: 12px;
                justify-content: center;
            }
            
            .skip-btn, .later-btn {
                padding: 8px 16px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.05);
                color: #94a3b8;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .skip-btn:hover, .later-btn:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #e5e7eb;
            }
        `;
        document.head.appendChild(styles);
    }
    
    addNotificationStyles() {
        if (document.getElementById('notification-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .motivation-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #38bdf8, #0ea5e9);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(56, 189, 248, 0.3);
                z-index: 9999;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                max-width: 300px;
            }
            
            .motivation-notification.show {
                transform: translateX(0);
            }
            
            .motivation-notification.amazing {
                background: linear-gradient(135deg, #22c55e, #16a34a);
            }
            
            .motivation-notification.good {
                background: linear-gradient(135deg, #3b82f6, #2563eb);
            }
            
            .motivation-notification.okay {
                background: linear-gradient(135deg, #f59e0b, #d97706);
            }
            
            .motivation-notification.low {
                background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            }
            
            .motivation-notification.struggling {
                background: linear-gradient(135deg, #ef4444, #dc2626);
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .notification-content i {
                font-size: 18px;
                flex-shrink: 0;
            }
        `;
        document.head.appendChild(styles);
    }
}

let emotionalCheckIn;
document.addEventListener('DOMContentLoaded', function() {
    emotionalCheckIn = new EmotionalCheckIn();
});
