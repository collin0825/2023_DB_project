from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'open' in request.values:
        vid = request.values.get('open')
        status = 'open'
        Product.update_status(vid, status)

    elif 'close' in request.values:
        vid = request.values.get('close')
        status = 'close'
        Product.update_status(vid, status)
        
    elif 'edit' in request.values:
        vid = request.values.get('edit')
        return redirect(url_for('manager.edit', vid=vid))
    
    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)

def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '職缺編號': i[1],
            '職缺名稱': i[3],
            '職缺內容': i[4],
            '上班時間': i[2],
            '技能需求': i[6],
            '薪水': i[5],
            '需求人數': i[7],
            'status': i[8],
            'office': i[9],
            'division': i[10],
            
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = 'v'
            vid = en + number
            data = Product.get_product(vid)

        vName = request.values.get('vName')
        content = request.values.get('content')
        workTime = request.values.get('workTime')
        skill = request.values.get('skill')
        salary = request.values.get('salary')
        people = request.values.get('people')
        office = request.values.get('office')
        unit = request.values.get('unit')

        if (len(vName) < 1 or len(content) < 1):
            return redirect(url_for('manager.productManager'))
        
        dept = Product.get_dept(office, unit)
        did = dept[0]
        
        Product.add_vacancy(
            {'vid' : vid,
             'workTime' : workTime,
             'vName' : vName,
             'content' : content,
             'salary':salary,
             'skill': skill,
             'required': people,
             'status': 1,
             'did': did
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_product(
            {
            'vid' : request.values.get('vid'),
            'vName' : request.values.get('vName'),
            'content' : request.values.get('content'), 
            'workTime' : request.values.get('workTime'),
            'skill' : request.values.get('skill'),
            'salary' : request.values.get('salary'),
            'required' : request.values.get('people')
            }
        )
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    vid = request.args['vid']
    data = Product.get_product(vid)
    vid = data[1]
    vname = data[3]
    content = data[4]
    workTime = data[2]
    skill = data[6]
    salary = data[5]
    required = data[7]
    office = data[9]
    division = data[10]

    product = {
        '職缺編號': vid,
        '職缺名稱': vname,
        '職缺內容': content,
        '上班時間': workTime,
        '技能需求': skill,
        '薪水': salary,
        '需求人數': required,
        'office': office,
        'division': division
    }
    return product


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))

    if 'meet' in request.values:
        aid = request.values.get('meet')
        status = 'meet'
        Apply_List.update_status(aid, status)      

    elif 'offer' in request.values:
        aid = request.values.get('offer')
        status = 'offer'
        Apply_List.update_status(aid, status)   
    
    order_row = Apply_List.get_application()
    order_data = []
    for i in order_row:
        order = {
            '學號': i[0],
            '姓名': i[1],
            '應徵職缺': i[2],
            '應徵編號': i[3],
            '審核狀態': i[4]
        }
        order_data.append(order)
        
    orderdetail_row = Apply_List.get_applydetail()
    order_detail = []

    for j in orderdetail_row:
        orderdetail = {
            '學號': j[0],
            '系所':j[1],
            '年級':j[2],
            '姓名': j[3],
            '職缺名稱': j[4],
            '可工作時段': j[5],
            '加分備註': j[6],
            '應徵時間': j[7],
            '應徵編號':j[8]
        }
        order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)