from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import Analysis

analysis = Blueprint('analysis', __name__, template_folder='../templates')

@analysis.route('/dashboard')
@login_required
def dashboard():
    if(current_user.role == 'user'):
        flash('No permission')
        return redirect(url_for('index'))
    dataa = []
    for i in range(1,13):
        row = Analysis.month_apply(i)

        if not row:
            dataa.append(0)
        else:
            for j in row:
                dataa.append(j[1])
        

        
    row = Analysis.category_vacancy()
    datab = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datab.append(temp)
    
    row = Analysis.category_vacancy_all()
    datac = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datac.append(temp)
    
        
    return render_template('dashboard.html', dataa = dataa, datab = datab, datac = datac, user=current_user.name)