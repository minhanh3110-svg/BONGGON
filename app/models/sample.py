from datetime import datetime
from app import db

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # Mã mẫu
    name = db.Column(db.String(200), nullable=False)  # Tên mẫu
    species = db.Column(db.String(200))  # Loài
    variety = db.Column(db.String(200))  # Giống
    source = db.Column(db.String(200))   # Nguồn gốc
    description = db.Column(db.Text)     # Mô tả
    status = db.Column(db.String(20), default='active')  # active, completed, failed, disposed
    stage = db.Column(db.String(50))     # Giai đoạn phát triển
    medium = db.Column(db.String(200))   # Môi trường nuôi cấy
    
    # Thông tin thời gian
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    expected_completion = db.Column(db.DateTime)  # Ngày dự kiến kết thúc
    
    # Foreign Keys
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    
    # Relationships
    images = db.relationship('SampleImage', backref='sample', lazy='dynamic')
    logs = db.relationship('SampleLog', backref='sample', lazy='dynamic')
    
    def __repr__(self):
        return f'<Sample {self.code}>'
    
    def add_log(self, action, notes=None, user_id=None):
        log = SampleLog(
            sample_id=self.id,
            action=action,
            notes=notes,
            user_id=user_id or self.creator_id
        )
        db.session.add(log)
        self.last_updated = datetime.utcnow()

class SampleImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    image_path = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SampleImage {self.id} for Sample {self.sample_id}>'

class SampleLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(50), nullable=False)  # created, updated, transferred, disposed, etc.
    notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SampleLog {self.action} on Sample {self.sample_id}>' 