from flask import abort, redirect, request, url_for
from flask_admin import Admin, AdminIndexView as DefaultAdminIndexView, expose
from flask_admin.contrib.sqla import ModelView as _ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import Select2Widget
from flask_login import current_user
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired
from .models import Area


class AdminIndexView(DefaultAdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_administrator:
            abort(403)
        return self.render('admin.html')


class ModelView(_ModelView):
    can_delete = True
    can_view_details = True
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        else:
            return redirect(url_for('auth.login', next=request.url))


class AreaModelView(ModelView):
    column_hide_backrefs = False
    form_extra_fields = {
        'ancestor': QuerySelectField(
            label='Ancestor',
            query_factory=lambda: Area.query.all(),
            widget=Select2Widget()
        )
    }

    def on_model_change(self, form, model, is_created):
        if not is_created and form.ancestor.data.id == model.id:
            model.ancestor_id = 1


class UserModelView(ModelView):
    column_exclude_list = form_excluded_columns = column_details_exclude_list = ['password_hash']
    form_extra_fields = {
        'password': PasswordField('Password', validators=[DataRequired()])
    }

    def on_model_change(self, form, model, is_created):
        model.password = form.password.data


admin = Admin(name='Viajes UH', template_mode='bootstrap3', index_view=AdminIndexView())
