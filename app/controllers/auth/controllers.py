from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from . import auth_blueprint
from .forms import EditProfileForm, LoginForm, RegistrationForm
from ...models import db, User, Area
from ...utils import flash_errors


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter_by(email=form.user.data).first()
        user_by_username = User.query.filter_by(username=form.user.data).first()
        user = user_by_email if user_by_email else user_by_username
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Correo electrónico o contraseña invalida.')
    else:
        flash_errors(form)
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.category.choices = [('0', 'Estudiante'), ('1', 'Profesor'), ('2', 'Trabajador')]
    form.area.choices= [
        (str(area.id), area.name)
        for area in Area.query.order_by(Area.name).all()
    ]
    if form.validate_on_submit():
        user = User()
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.username = form.username.data
        print(form.username.data, 'dadsadasd')
        user.email = form.email.data
        user.password = form.password.data
        user.confirmed = True
        user.category = 'student' if form.category.data == '0' else \
            'teacher' if form.category.data == '1' else 'employee'
        area = Area.query.get_or_404(int(form.area.data))
        user.area = area
        db.session.add(user)
        db.session.commit()
        flash('Ahora puede iniciar sesión.')
        return redirect(request.args.get('next') or url_for('auth.login'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Usted ha sido desconectado.')
    return redirect(request.args.get('next') or url_for('main.index'))


@auth_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.add(current_user)
        db.session.commit()
        flash('Perfil actualizado.')
        return redirect(request.args.get('next') or url_for('auth.see_profile'))
    else:
        flash_errors(form)
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    return render_template('auth/edit_profile.html', form=form)


@auth_blueprint.route('/see_profile')
@login_required
def see_profile():
    return render_template('auth/see_profile.html')
