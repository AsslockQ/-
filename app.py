from flask import Flask, render_template, request, jsonify, url_for, redirect
import random
import string
import request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class ForumCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    topics = db.relationship('ForumTopic', backref='category', lazy=True)

class ForumTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('forum_category.id'), nullable=False)
    replies = db.relationship('ForumReply', backref='topic', lazy=True)
    views = db.Column(db.Integer, default=0)

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topic.id'), nullable=False)

with app.app_context():
    db.create_all()
    # Создаем начальные категории, если их нет
    if not ForumCategory.query.first():
        categories = [
            {
                'name': 'Основы кибербезопасности',
                'description': 'Обсуждение базовых принципов защиты в интернете'
            },
            {
                'name': 'Защита от фишинга',
                'description': 'Как распознать и избежать фишинговых атак'
            },
            {
                'name': 'Безопасность паролей',
                'description': 'Все о создании и хранении надежных паролей'
            },
            {
                'name': 'Вредоносное ПО',
                'description': 'Обсуждение вирусов, троянов и методов защиты'
            }
        ]
        for cat in categories:
            db.session.add(ForumCategory(**cat))
        
        # Добавляем несколько начальных тем
        topics = [
            {
                'category_id': 1,
                'title': 'Гайд по двухфакторной аутентификации',
                'content': 'Двухфакторная аутентификация (2FA) - это метод подтверждения личности пользователя путем использования двух разных факторов аутентификации. Обычно это что-то, что вы знаете (пароль), и что-то, что у вас есть (телефон).\n\nРекомендуемые приложения для 2FA:\n- Google Authenticator\n- Authy\n- Microsoft Authenticator',
                'author': 'Admin',
                'views': 125
            },
            {
                'category_id': 2,
                'title': 'Как распознать фишинговое письмо?',
                'content': '1. Проверяйте адрес отправителя\n2. Обращайте внимание на ошибки в тексте\n3. Не открывайте подозрительные вложения\n4. Проверяйте URL-адреса, наведя на них курсор\n5. Не поддавайтесь на срочность и угрозы',
                'author': 'SecurityExpert',
                'views': 243
            },
            {
                'category_id': 3,
                'title': 'Лучшие менеджеры паролей 2025',
                'content': 'Топ безопасных менеджеров паролей:\n1. Bitwarden - открытый исходный код, бесплатный\n2. 1Password - отличный интерфейс, синхронизация\n3. KeePassXC - локальное хранение, без облака\n4. LastPass - удобный, но был взломан в 2022\n5. Dashlane - с VPN, но дорогой',
                'author': 'PasswordMaster',
                'views': 189
            }
        ]
        for topic in topics:
            db.session.add(ForumTopic(**topic))
            
        # Добавляем ответы к темам
        replies = [
            {
                'topic_id': 1,
                'content': 'Спасибо за гайд! Использую Google Authenticator уже год, очень удобно.',
                'author': 'User123'
            },
            {
                'topic_id': 1,
                'content': 'А я предпочитаю Authy, там есть синхронизация между устройствами.',
                'author': 'TechGuru'
            },
            {
                'topic_id': 2,
                'content': 'Недавно чуть не попался на фишинг от "банка". Спасло то, что адрес был странный.',
                'author': 'SafeUser'
            },
            {
                'topic_id': 3,
                'content': 'Bitwarden лучший! Использую его на всех устройствах.',
                'author': 'CyberNinja'
            }
        ]
        for reply in replies:
            db.session.add(ForumReply(**reply))
            
        db.session.commit()

def get_security_news():
   
    return [
        {
            "date": "24.01.2025",
            "title": "Новый вид фишинговых атак в России",
            "description": "Мошенники используют поддельные письма от госуслуг для кражи данных",
            "source": "SecurityLab"
        },
        {
            "date": "23.01.2025",
            "title": "Масштабная утечка данных в социальной сети",
            "description": "Рекомендуется сменить пароли в социальных сетях",
            "source": "Хабр"
        },
        {
            "date": "22.01.2025",
            "title": "Обнаружена уязвимость в популярном браузере",
            "description": "Обновите ваш браузер до последней версии",
            "source": "CyberNews"
        }
    ]


def get_threat_data():
    return {
        "Москва": {"фишинг": 45, "вредоносное_по": 30, "социальная_инженерия": 25},
        "Санкт-Петербург": {"фишинг": 40, "вредоносное_по": 35, "социальная_инженерия": 25},
        "Казань": {"фишинг": 35, "вредоносное_по": 40, "социальная_инженерия": 25},
        "Новосибирск": {"фишинг": 30, "вредоносное_по": 45, "социальная_инженерия": 25},
        "Екатеринбург": {"фишинг": 38, "вредоносное_по": 32, "социальная_инженерия": 30},
        "Якутск": {"фишинг": 33, "вредоносное_по": 37, "социальная_инженерия": 30}
    }


@app.route("/")
def home():
    news = get_security_news()
    return render_template("guide.html", news=news)

# Страница с викториной
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    score = 0
    total_questions = 3

    if request.method == "POST":
        
        answers = request.form.getlist("answer")

        # Проверка ответов
        if "3" in answers:  
            score += 1
        if "1" in answers:  
            score += 1
        if "2" in answers: 
            score += 1

        # Отправляем результат на страницу результатов
        return render_template("results.html", score=score, total_questions=total_questions)

    return render_template("quiz.html")

# Страница с видеоматериалами
@app.route("/videos")
def videos():
    video_materials = [
        {
            "title": "Как не попасться на уловки мошенников?",
            "url": url_for('video_scam')
        },
        {
            "title": "Как создать аккаунт на Госуслугах?",
            "url": url_for('video_gosuslugi')
        },
        {
            "title": "Что такое прокси и DNS?",
            "url": url_for('video_proxy_dns')
        }
    ]
    return render_template("videos.html", videos=video_materials)

# Маршруты для отдельных видео
@app.route("/video/scam")
def video_scam():
    return render_template("video_scam.html")

@app.route("/video/gosuslugi")
def video_gosuslugi():
    return render_template("video_gosuslugi.html")

@app.route("/video/proxy_dns")
def video_proxy_dns():
    return render_template("video_proxy_dns.html")

# Страница FAQ
@app.route("/faq")
def faq():
    return render_template("faq.html")

# Страница генератора паролей
@app.route("/password-generator")
def password_generator():
    return render_template("password_generator.html")

# API для генерации пароля
@app.route("/api/generate-password")
def generate_password():
    length = int(request.args.get('length', 12))
    use_uppercase = request.args.get('uppercase', 'true') == 'true'
    use_numbers = request.args.get('numbers', 'true') == 'true'
    use_special = request.args.get('special', 'true') == 'true'

    chars = string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = ''.join(random.choice(chars) for _ in range(length))
    return jsonify({"password": password})

# Страница карты угроз
@app.route("/threat-map")
def threat_map():
    threats = get_threat_data()
    return render_template("threat_map.html", threats=threats)

@app.route("/security-check", methods=["GET", "POST"])
def security_check():
    if request.method == "POST":
        score = 0
        max_score = 5
        
        if request.form.get('2fa') == 'yes':
            score += 1
        if request.form.get('password_change') in ['monthly', 'quarterly']:
            score += 1
        if request.form.get('unique_passwords') == 'yes':
            score += 1
        if request.form.get('antivirus') == 'yes':
            score += 1
        if request.form.get('backup') == 'yes':
            score += 1
            
        percentage = (score / max_score) * 100
        return render_template("security_result.html", score=score, max_score=max_score, percentage=percentage)
    
    return render_template("security_check.html")

@app.route("/forum")
def forum():
    categories = ForumCategory.query.all()
    return render_template("forum.html", categories=categories)

@app.route("/forum/category/<int:category_id>")
def forum_category(category_id):
    category = ForumCategory.query.get_or_404(category_id)
    return render_template("forum_category.html", category=category)

@app.route("/forum/topic/<int:topic_id>")
def forum_topic(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    topic.views += 1
    db.session.commit()
    return render_template("forum_topic.html", topic=topic)

@app.route("/forum/topic/<int:topic_id>/reply", methods=["POST"])
def add_reply(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    content = request.form.get('content')
    author = request.form.get('author')
    
    if content and author:
        reply = ForumReply(content=content, author=author, topic_id=topic_id)
        db.session.add(reply)
        db.session.commit()
        
    return redirect(url_for('forum_topic', topic_id=topic_id))

@app.route("/forum/new_topic/<int:category_id>", methods=["GET", "POST"])
def new_topic(category_id):
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        
        if title and content and author:
            topic = ForumTopic(
                title=title,
                content=content,
                author=author,
                category_id=category_id
            )
            db.session.add(topic)
            db.session.commit()
            return redirect(url_for('forum_category', category_id=category_id))
            
    category = ForumCategory.query.get_or_404(category_id)
    return render_template("new_topic.html", category=category)

@app.route("/comments")
def comments():
    all_comments = Comment.query.order_by(Comment.date.desc()).all()
    return render_template("comments.html", comments=all_comments)

@app.route("/add-comment", methods=["POST"])
def add_comment():
    if request.method == "POST":
        author = request.form.get('name')
        text = request.form.get('comment')
        
        if author and text:
            new_comment = Comment(author=author, text=text)
            db.session.add(new_comment)
            db.session.commit()
            
    return redirect(url_for('comments'))

# Страница поддержки
@app.route('/support')
def support():
    return render_template('support.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")