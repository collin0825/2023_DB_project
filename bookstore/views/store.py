import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import Member, Order_List, Vacancy, Record, Cart, Apply_List

store = Blueprint('bookstore', __name__, template_folder='../templates')

@store.route('/', methods=['GET', 'POST'])
@login_required
def bookstore():
    result = Vacancy.count()
    count = math.ceil(result[0]/9)
    flag = 0
    
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))
        
    if request.method == 'POST':
        birthdate = request.values.get('birth')

        input = {
            'mid' : current_user.id,
            'pid' : request.values.get('pid'),
            'birth' : datetime.date(int(birthdate[:4]), int(birthdate[5:7]), int(birthdate[8:10])),
            'phone' : request.values.get('phone'),
            'gender' : request.values.get('gender'),
            'dept' : request.values.get('dept'),
            'grade' : request.values.get('grade'),
            'email' : request.values.get('email')
        }
        
        Member.update_profile(input)
        
        return redirect(url_for('bookstore.bookstore'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM VACANCY WHERE VNAME LIKE :search AND STATUS = 1')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '職缺編號': i[0],
                '職缺名稱': i[2],
                '職缺內容': i[4]
            }
            book_data.append(book)
            total = total + 1
        
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('bookstore.html', single=single, keyword=search, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    

    
    elif 'pid' in request.args:
        vid = request.args['pid']
        data = Vacancy.get_vacancy(vid)
        
        vname = data[3]
        price = data[5]
        worktime = data[2]
        description = data[4]
        requiredNum = data[7]
        image = 'logo.jpg'
        dep = data[9] + '-' + data[10]

        worktimelist = []
        worktimeStr = ''
        
        worktime = worktime.split(';')
        for w in worktime:
            worktimelist.append('星期' + w[0] + w[1] + '午')

        for i in range(0, len(worktimelist)):
            if (i == 0):
                worktimeStr = worktimeStr + worktimelist[i]
            else:
                worktimeStr = worktimeStr + '/' + worktimelist[i]

        print(data[8])
        if(data[8] == 0):
            v_status = '已招滿'
        elif(data[8] == 1):
            v_status = '招募中'

        product = {
            '工讀編號': vid,
            '工讀名稱': vname,
            '單價': price,
            '工作時間': worktimeStr,
            '職缺敘述': description,
            '欲招人數':requiredNum,
            '商品圖片': image,
            '應聘單位': dep,
            '職缺狀態': v_status
        }

        return render_template('product.html', data = product, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        book_row = Vacancy.get_open_vacancy()
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '職缺編號': i[1],
                '職缺名稱': i[3],
                '職缺內容': i[5]
            }
            book_data.append(book)
            
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
        
        return render_template('bookstore.html', book_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM VACANCY WHERE VNAME LIKE :search AND STATUS = 1')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        book_data = []
        total = 0
        
        for i in book_row:
            book = {
                '職缺編號': i[0],
                '職缺名稱': i[2],
                '職缺內容': i[4]
            }

            book_data.append(book)
            total = total + 1
            
        if(len(book_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('bookstore.html', keyword=search, single=single, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        book_row = Vacancy.get_open_vacancy()
        book_data = []
        temp = 0
        for i in book_row:
            book = {
                '職缺編號': i[1],
                '職缺名稱': i[3],
                '職缺內容': i[5]
            }
            if len(book_data) < 9:
                book_data.append(book)
        
        return render_template('bookstore.html', book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)

# 我感興趣
@store.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            vid = request.values.get('pid') # 使用者想要購買的東西

            # 檢查save record裡有沒有mid和vid
            product = Record.check_saveRecord(vid, current_user.id)
            
            if(product == None):
                time = datetime.datetime.now()
                print(time)
                Cart.add_saveInterest(current_user.id, time) # 加入interest
                Cart.add_saveRecord(current_user.id, time, vid)

        elif "delete" in request.form :
            vid = request.values.get('delete')
            mid = current_user.id

            Member.delete_product(mid, vid)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('bookstore.bookstore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('bookstore.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_order( {'mid': current_user.id, 'time':time, 'total':total, 'format':format, 'tno':tno} )

            return render_template('complete.html', user=current_user.name)

    product_data = only_cart()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=product_data, user=current_user.name)

@store.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pname = Vacancy.get_name(i[1])
        product = {
            '商品編號': i[1],
            '商品名稱': pname,
            '商品價格': i[3],
            '數量': i[2]
        }
        product_data.append(product)
    
    total = Record.get_total(tno)[0]

    return render_template('order.html', data=product_data, total=total, user=current_user.name)

@store.route('/orderlist')
def orderlist():
    if "oid" in request.args :
        pass

    check_applied = 0
    if "check_applied" in request.args:
        check_applied = 1
    
    user_id = current_user.id

    data = Member.get_order(user_id)

    orderlist = []
    status = ''
    v_status = ''

    for i in data:
        if(i[6] == 0):
            status = '未審核'
        elif(i[6] == 1):
            status = '審核中'
        elif(i[6] == 2):
            status = '已錄取'
        
        vacancy = Vacancy.get_vacancy(i[4])

        if(vacancy[8] == 0):
            v_status = '已招滿'
        elif(vacancy[8] == 1):
            v_status = '招募中'

        temp = {
            '應徵編號': i[0],
            '應徵時間': str(i[5])[:10],
            '應徵狀態': status,
            '職缺編號': i[4],
            '可工作時段': i[1],
            '加分備註': i[2],
            '職缺名稱': vacancy[3],
            '薪資': vacancy[5],
            '職缺狀態': v_status
        }
        orderlist.append(temp)

    return render_template('orderlist.html', data=orderlist, user=current_user.name, check_applied=check_applied)

def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Record.get_record(data[2])

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Record.update_vacancy({
                'amount':request.form[i[1]],
                'pid':i[1],
                'tno':tno,
                'total':int(request.form[i[1]])*int(i[3])
            })
            print('change')

    return 0


def only_cart():
    
    count = Cart.check(current_user.id)

    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    print(data)

    vlist = []
    for i in data:
        vlist.append(Vacancy.get_vacancy(i[2]))

    print('=====================================')
    print(vlist)

    product_data = []

    for i in vlist:
        vid = i[1]
        print(vid)
        vname = i[3]
        print(vname)
        salary = i[5]
        print(salary)
        required = i[7]
        print(required)
        status = ''
        dep = i[9] + '-' + i[10]
        print(dep)

        if(i[8] == 0):
            status = '已招滿'
        elif(i[8] == 1):
            status = '應徵中'
        
        product = {
            '職缺編號': vid,
            '職缺名稱': vname,
            '薪資': salary,
            '欲招人數': required,
            '職缺狀態': status,
            '工讀單位': dep
        }
        product_data.append(product)
    print('=====================================')
    print(product_data)
    
    return product_data

@store.route('/profile')
def profile():
    mid = current_user.id
    data = list(Member.get_profile(mid))
    # 轉換datetime to yyyy-mm-dd
    if data[5] != None:
        data[5] = data[5].date()

    # 檢查profile是否填寫完整，0代表完整
    check = 0

    return render_template('profile.html', data=data, user=current_user.name, check=check)#, data=orderlist, user=current_user.name)

@store.route('/checking', methods=['POST'] )
def checking():
    mid = current_user.id
    profile = Member.get_profile(mid)
    data = list(profile)
    vid = request.values.get('vid')

    # 檢查profile是否填寫完整，0代表完整
    for i in profile:
        if ((i == None) or (i == 'None')):
            check = 1
            return render_template('profile.html', data=data, user=current_user.name, check=check)

    current_app_list = Apply_List.get_aid()
    max_aid = 0
    for i in current_app_list:
        if(max_aid < int(i[0][1:])):
            max_aid = int(i[0][1:])

    apply_data = Member.get_order(mid)
    print(apply_data)
    for i in apply_data:
        # print(i[4])
        # print(i[5])
        if(mid == i[3] and vid == i[4]):
            check_applied = 1
            return redirect(url_for('bookstore.orderlist', check_applied=check_applied))

    # 寫入APPLICATION
    input = {
        'aid' : 'a'+ str(max_aid+1),
        'avaTime' : request.values.get('avaTime'),
        'bonus' : request.values.get('bonus'),
        'mid' : mid
    }
    Apply_List.insert_application(input)

    input2 = {
        'aid' : 'a'+ str(max_aid+1),
        'vid' : vid,
        'time' : datetime.datetime.now(),
        'status' : 0
    }
    Apply_List.insert_applyrecord(input2)


    return redirect('/bookstore/orderlist')