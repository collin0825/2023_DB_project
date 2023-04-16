import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    data = Member.get_role(userid)
    try:
        user.role = data[0]
        user.name = data[1]
    except:
        pass
    return user

@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['mid']
        password = request.form['password']
        data = Member.get_member(account) 

        try:
            member_id = data[0][0]
            DB_password = data[0][2]
            identity = data[0][3]

        except:
            flash('*沒有此帳號')
            return redirect(url_for('api.login'))

        if(DB_password == password ):
            user = User()
            user.id = member_id 
            login_user(user)

            if( identity == 'user'):
                print(identity)
                return redirect(url_for('bookstore.bookstore'))
            else:
                print(identity)
                return redirect(url_for('manager.productManager'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    
    return render_template('login.html')

@api.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_mid = request.form['mid']
        exist_account = Member.get_all_account()
        account_list = []
        for i in exist_account:
            account_list.append(i[0])

        if(user_mid in account_list):
            flash('Falied!')
            return redirect(url_for('api.register'))
        else:
            input = { 
                'mid':user_mid, 
                'name': request.form['username'], 
                'password':request.form['password'], 
                'identity':request.form['identity'] 
            }
            Member.create_member(input)
            return redirect(url_for('api.login'))

    return render_template('register.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))