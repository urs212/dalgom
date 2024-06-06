from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 사용자 데이터 및 로그인 내역
users = {}
login_history = []
admin_credentials = {'username': 'dalgom_admin', 'password': 'dalgom_admin'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        if not name or not phone or not password:
            return render_template('register.html', error='모두 입력해주세요')
        user_id = f'user{len(users) + 1}'
        users[user_id] = {'name': name, 'phone': phone, 'password': password}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        for user in users.values():
            if (user['name'] == identifier or user['phone'] == identifier) and user['password'] == password:
                login_history.append(user['name'])
                return render_template('login.html', success='로그인 완료!')
        return render_template('login.html', error='로그인 실패!')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            return render_template('admin_dashboard.html', login_history=login_history, login_count=len(login_history))
        return render_template('admin.html', error='로그인 실패!')
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
