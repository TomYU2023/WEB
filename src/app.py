from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 初始化 Flask 应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


# 初始化数据库和登录管理器
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 如果未登录，将重定向到此视图

# 用户模型定义
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 初始化数据库
with app.app_context():
    db.create_all()

# 登录管理器回调，用于加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 默认页面（注册页面）
@app.route('/')
def index():
    return redirect(url_for('register'))

# 注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('用户名或邮箱已存在！')
            return redirect(url_for('register'))

        # 加密密码并创建用户
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录！')
        return redirect(url_for('login'))

    return render_template('register.html')

# 登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查找用户并验证密码
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('home'))

        flash('用户名或密码错误！')
        return redirect(url_for('login'))

    return render_template('login.html')

# 登出视图
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。')
    return redirect(url_for('login'))

# 受保护主页
@app.route('/homepage')
@login_required
def home():
    return render_template('homepage.html', username=current_user.username)

# 启动应用
if __name__ == '__main__':
    app.run(port=6666, debug=False)