"""

======================

@author:sunqiucheng

@time:2022/10/8:11:58 上午

======================

"""
import wtforms
from wtforms import FileField,Form
from wtforms.validators import length, email, EqualTo,InputRequired
from STPService.comment.models.products import Products
from STPService.comment.models.apps import Apps
from STPService.comment.models.submit_test_info import SubmitTestInfo
from flask_wtf.file import FileRequired, FileAllowed



class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=10)])
    password = wtforms.StringField(validators=[length(min=4, max=10)])

class AddUserForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=1, max=10)])
    password = wtforms.StringField(validators=[length(min=1, max=10)])
    mail=wtforms.StringField(validators=[email()])

class ProductForm(wtforms.Form):
    version = wtforms.IntegerField()
    id = wtforms.IntegerField()

    def validate_version(self,field):
        if field:
            version = field.data
            id = self.id.data
            print(version)
            product_model = Products.query.filter(Products.id == id).first()
            if product_model and version != product_model.version:
                raise wtforms.ValidationError("数据版本不一致")

class AppsForm(wtforms.Form):
    version = wtforms.IntegerField()
    id = wtforms.IntegerField()
    def validate_version(self, field):
        if field:
            version = field.data
            id = self.id.data
            app_model = Apps.query.filter(Apps.id == id).first()
            if app_model and version != app_model.version:
                raise wtforms.ValidationError("数据版本不一致")

class SubmitTestForm(wtforms.Form):
    version = wtforms.IntegerField()
    id = wtforms.IntegerField()
    def validate_version(self, field):
        if field:
            version = field.data
            id = self.id.data
            test_model = SubmitTestInfo.query.filter(SubmitTestInfo.id == id).first()
            print(version,test_model.version)
            if (test_model and version != test_model.version):
                raise wtforms.ValidationError("数据版本不一致")

class FileForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'pdf', 'zip', 'xmind'])])
