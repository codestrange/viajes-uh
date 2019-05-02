from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, EditProfileForm
from ...models import db, User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Correo electrónico o contraseña invalida.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('Ahora puede iniciar sesión.')
        return redirect(request.args.get('next') or url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Usted ha sido desconectado.')
    return redirect(request.args.get('next') or url_for('main.index'))


@auth.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = current_user
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('Perfil actualizado.')
        return redirect(url_for('main.index'))
    return render_template('auth/editprofile.html',form=form)

@auth.route('/seeprofile', methods=['GET'])
@login_required
def seeprofile():
    user = current_user
    return render_template('auth/seeprofile.html',form=user)