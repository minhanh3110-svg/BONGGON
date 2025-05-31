from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed

class SampleForm(FlaskForm):
    code = StringField('Mã mẫu', validators=[
        DataRequired(),
        Length(max=50)
    ])
    name = StringField('Tên mẫu', validators=[
        DataRequired(),
        Length(max=200)
    ])
    species = StringField('Loài', validators=[Length(max=200)])
    variety = StringField('Giống', validators=[Length(max=200)])
    source = StringField('Nguồn gốc', validators=[Length(max=200)])
    description = TextAreaField('Mô tả')
    stage = StringField('Giai đoạn phát triển', validators=[Length(max=50)])
    medium = StringField('Môi trường nuôi cấy', validators=[Length(max=200)])
    room_id = SelectField('Phòng nuôi cấy', coerce=int)
    expected_completion = DateField('Ngày dự kiến kết thúc', validators=[Optional()])
    images = FileField('Hình ảnh', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Chỉ chấp nhận file ảnh!')
    ])

class RoomForm(FlaskForm):
    name = StringField('Tên phòng', validators=[
        DataRequired(),
        Length(max=100)
    ])
    description = TextAreaField('Mô tả')
    temperature = FloatField('Nhiệt độ (°C)', validators=[
        Optional(),
        NumberRange(min=0, max=50)
    ])
    humidity = FloatField('Độ ẩm (%)', validators=[
        Optional(),
        NumberRange(min=0, max=100)
    ])
    light_level = FloatField('Cường độ ánh sáng (lux)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    capacity = IntegerField('Sức chứa tối đa', validators=[
        DataRequired(),
        NumberRange(min=1)
    ])
    status = SelectField('Trạng thái', choices=[
        ('active', 'Hoạt động'),
        ('maintenance', 'Bảo trì'),
        ('inactive', 'Không hoạt động')
    ])
    manager_id = SelectField('Người quản lý', coerce=int)

class SampleFilterForm(FlaskForm):
    status = SelectField('Trạng thái', choices=[
        ('', 'Tất cả'),
        ('active', 'Đang nuôi cấy'),
        ('completed', 'Hoàn thành'),
        ('failed', 'Thất bại'),
        ('disposed', 'Đã hủy')
    ])
    room = SelectField('Phòng', coerce=int)
    search = StringField('Tìm kiếm')

class EnvironmentLogFilterForm(FlaskForm):
    start_date = DateField('Từ ngày', validators=[Optional()])
    end_date = DateField('Đến ngày', validators=[Optional()])
    parameter = SelectField('Thông số', choices=[
        ('temperature', 'Nhiệt độ'),
        ('humidity', 'Độ ẩm'),
        ('light_level', 'Cường độ ánh sáng')
    ]) 