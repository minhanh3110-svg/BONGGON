from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app.models.sample import Sample, SampleLog, SampleImage
from app.models.room import Room, EnvironmentLog
from app.models.user import User
from app.forms.main import SampleForm, RoomForm, SampleFilterForm, EnvironmentLogFilterForm
from app import db
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Lấy thống kê tổng quan
    total_samples = Sample.query.count()
    active_samples = Sample.query.filter_by(status='active').count()
    total_rooms = Room.query.count()
    recent_logs = SampleLog.query.order_by(SampleLog.timestamp.desc()).limit(5).all()
    
    return render_template('main/index.html',
                         total_samples=total_samples,
                         active_samples=active_samples,
                         total_rooms=total_rooms,
                         recent_logs=recent_logs)

@bp.route('/rooms')
@login_required
def rooms():
    rooms = Room.query.all()
    return render_template('main/rooms.html', rooms=rooms)

@bp.route('/room/<int:id>')
@login_required
def room_detail(id):
    room = Room.query.get_or_404(id)
    samples = room.samples.all()
    env_logs = room.environment_logs.order_by(EnvironmentLog.timestamp.desc()).limit(24).all()
    return render_template('main/room_detail.html', room=room, samples=samples, env_logs=env_logs)

@bp.route('/samples')
@login_required
def samples():
    page = request.args.get('page', 1, type=int)
    samples = Sample.query.order_by(Sample.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/samples.html', samples=samples)

@bp.route('/sample/<int:id>')
@login_required
def sample_detail(id):
    sample = Sample.query.get_or_404(id)
    logs = sample.logs.order_by(SampleLog.timestamp.desc()).all()
    return render_template('main/sample_detail.html', sample=sample, logs=logs)

@bp.route('/profile')
@login_required
def profile():
    stats = {
        'managing_samples': Sample.query.filter_by(creator_id=current_user.id).count(),
        'total_logs': SampleLog.query.filter_by(user_id=current_user.id).count(),
        'success_rate': calculate_success_rate(current_user.id)
    }
    return render_template('main/profile.html', stats=stats)

def calculate_success_rate(user_id):
    total = Sample.query.filter_by(creator_id=user_id).count()
    if total == 0:
        return 0
    successful = Sample.query.filter_by(
        creator_id=user_id, status='completed').count()
    return round((successful / total) * 100, 1)

@bp.route('/room/create', methods=['GET', 'POST'])
@login_required
def room_create():
    form = RoomForm()
    form.manager_id.choices = [(u.id, u.full_name) for u in User.query.all()]
    
    if form.validate_on_submit():
        room = Room(
            name=form.name.data,
            description=form.description.data,
            temperature=form.temperature.data,
            humidity=form.humidity.data,
            light_level=form.light_level.data,
            capacity=form.capacity.data,
            status=form.status.data,
            manager_id=form.manager_id.data
        )
        db.session.add(room)
        db.session.commit()
        flash('Phòng mới đã được tạo thành công.', 'success')
        return redirect(url_for('main.rooms'))
    
    return render_template('main/room_form.html', form=form, title='Tạo phòng mới')

@bp.route('/room/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def room_edit(id):
    room = Room.query.get_or_404(id)
    form = RoomForm(obj=room)
    form.manager_id.choices = [(u.id, u.full_name) for u in User.query.all()]
    
    if form.validate_on_submit():
        room.name = form.name.data
        room.description = form.description.data
        room.temperature = form.temperature.data
        room.humidity = form.humidity.data
        room.light_level = form.light_level.data
        room.capacity = form.capacity.data
        room.status = form.status.data
        room.manager_id = form.manager_id.data
        db.session.commit()
        flash('Thông tin phòng đã được cập nhật.', 'success')
        return redirect(url_for('main.room_detail', id=room.id))
    
    return render_template('main/room_form.html', form=form, room=room, title='Chỉnh sửa phòng')

@bp.route('/sample/create', methods=['GET', 'POST'])
@login_required
def sample_create():
    form = SampleForm()
    form.room_id.choices = [(r.id, r.name) for r in Room.query.filter_by(status='active').all()]
    
    if form.validate_on_submit():
        sample = Sample(
            code=form.code.data,
            name=form.name.data,
            species=form.species.data,
            variety=form.variety.data,
            source=form.source.data,
            description=form.description.data,
            stage=form.stage.data,
            medium=form.medium.data,
            room_id=form.room_id.data,
            expected_completion=form.expected_completion.data,
            creator_id=current_user.id
        )
        
        # Xử lý upload hình ảnh
        if form.images.data:
            for image in form.images.data:
                filename = secure_filename(image.filename)
                image_path = os.path.join('uploads', filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
                sample_image = SampleImage(
                    sample=sample,
                    image_path=image_path
                )
                db.session.add(sample_image)
        
        db.session.add(sample)
        sample.add_log('created', 'Mẫu mới được tạo')
        db.session.commit()
        
        flash('Mẫu mới đã được tạo thành công.', 'success')
        return redirect(url_for('main.sample_detail', id=sample.id))
    
    return render_template('main/sample_form.html', form=form, title='Tạo mẫu mới')

@bp.route('/sample/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def sample_edit(id):
    sample = Sample.query.get_or_404(id)
    form = SampleForm(obj=sample)
    form.room_id.choices = [(r.id, r.name) for r in Room.query.filter_by(status='active').all()]
    
    if form.validate_on_submit():
        sample.code = form.code.data
        sample.name = form.name.data
        sample.species = form.species.data
        sample.variety = form.variety.data
        sample.source = form.source.data
        sample.description = form.description.data
        sample.stage = form.stage.data
        sample.medium = form.medium.data
        sample.room_id = form.room_id.data
        sample.expected_completion = form.expected_completion.data
        
        # Xử lý upload hình ảnh mới
        if form.images.data:
            for image in form.images.data:
                filename = secure_filename(image.filename)
                image_path = os.path.join('uploads', filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
                sample_image = SampleImage(
                    sample=sample,
                    image_path=image_path
                )
                db.session.add(sample_image)
        
        sample.add_log('updated', 'Thông tin mẫu được cập nhật')
        db.session.commit()
        flash('Thông tin mẫu đã được cập nhật.', 'success')
        return redirect(url_for('main.sample_detail', id=sample.id))
    
    return render_template('main/sample_form.html', form=form, sample=sample, title='Chỉnh sửa mẫu')

@bp.route('/api/rooms/environment')
@login_required
def get_room_environment():
    rooms = Room.query.all()
    data = [{
        'id': room.id,
        'temperature': room.temperature,
        'humidity': room.humidity,
        'light_level': room.light_level,
        'last_updated': room.last_updated.isoformat()
    } for room in rooms]
    return jsonify(data)

@bp.route('/sample/<int:id>/images/<int:image_id>/delete')
@login_required
def delete_sample_image(id, image_id):
    sample = Sample.query.get_or_404(id)
    image = SampleImage.query.get_or_404(image_id)
    
    if image.sample_id != sample.id:
        flash('Không có quyền xóa hình ảnh này.', 'error')
        return redirect(url_for('main.sample_detail', id=id))
    
    # Xóa file hình ảnh
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image.image_path))
    except:
        pass
    
    db.session.delete(image)
    db.session.commit()
    flash('Đã xóa hình ảnh.', 'success')
    return redirect(url_for('main.sample_edit', id=id))

@bp.route('/reports/samples')
@login_required
def sample_report():
    # Lấy thông tin mẫu và lọc theo form
    form = SampleFilterForm(request.args)
    form.room.choices = [(0, 'Tất cả')] + [(r.id, r.name) for r in Room.query.all()]
    
    query = Sample.query
    if form.status.data:
        query = query.filter_by(status=form.status.data)
    if form.room.data and form.room.data != 0:
        query = query.filter_by(room_id=form.room.data)
    if form.search.data:
        search = f"%{form.search.data}%"
        query = query.filter(
            (Sample.code.like(search)) |
            (Sample.name.like(search)) |
            (Sample.species.like(search))
        )
    
    samples = query.all()
    
    # Tạo DataFrame từ dữ liệu mẫu
    data = []
    for sample in samples:
        data.append({
            'Mã mẫu': sample.code,
            'Tên mẫu': sample.name,
            'Loài': sample.species,
            'Giống': sample.variety,
            'Nguồn gốc': sample.source,
            'Giai đoạn': sample.stage,
            'Phòng': sample.room.name,
            'Trạng thái': sample.status,
            'Ngày tạo': sample.created_at.strftime('%d/%m/%Y'),
            'Dự kiến hoàn thành': sample.expected_completion.strftime('%d/%m/%Y') if sample.expected_completion else ''
        })
    
    df = pd.DataFrame(data)
    
    # Xuất file Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Mẫu nuôi cấy', index=False)
        
        # Tùy chỉnh độ rộng cột
        worksheet = writer.sheets['Mẫu nuôi cấy']
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'bao-cao-mau-nuoi-cay-{datetime.now().strftime("%d%m%Y")}.xlsx'
    )

@bp.route('/reports/environment/<int:room_id>')
@login_required
def environment_report(room_id):
    room = Room.query.get_or_404(room_id)
    form = EnvironmentLogFilterForm(request.args)
    
    # Lấy dữ liệu môi trường trong khoảng thời gian
    query = EnvironmentLog.query.filter_by(room_id=room_id)
    if form.start_date.data:
        query = query.filter(EnvironmentLog.timestamp >= form.start_date.data)
    if form.end_date.data:
        query = query.filter(EnvironmentLog.timestamp <= form.end_date.data + timedelta(days=1))
    
    logs = query.order_by(EnvironmentLog.timestamp).all()
    
    # Tạo biểu đồ
    plt.figure(figsize=(12, 6))
    timestamps = [log.timestamp for log in logs]
    
    if form.parameter.data == 'temperature':
        values = [log.temperature for log in logs]
        plt.plot(timestamps, values, 'r-')
        plt.ylabel('Nhiệt độ (°C)')
    elif form.parameter.data == 'humidity':
        values = [log.humidity for log in logs]
        plt.plot(timestamps, values, 'b-')
        plt.ylabel('Độ ẩm (%)')
    else:
        values = [log.light_level for log in logs]
        plt.plot(timestamps, values, 'y-')
        plt.ylabel('Cường độ ánh sáng (lux)')
    
    plt.title(f'Biểu đồ {dict(form.parameter.choices).get(form.parameter.data)} - {room.name}')
    plt.xlabel('Thời gian')
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Lưu biểu đồ vào buffer
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    plt.close()
    
    return send_file(
        img_buf,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'bieu-do-{form.parameter.data}-{room_id}-{datetime.now().strftime("%d%m%Y")}.png'
    ) 