from datetime import datetime
from app import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    temperature = db.Column(db.Float)  # Nhiệt độ hiện tại
    humidity = db.Column(db.Float)     # Độ ẩm hiện tại
    light_level = db.Column(db.Float)  # Cường độ ánh sáng
    status = db.Column(db.String(20), default='active')  # active, maintenance, inactive
    capacity = db.Column(db.Integer)   # Sức chứa tối đa
    current_samples = db.Column(db.Integer, default=0)  # Số mẫu hiện tại
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    samples = db.relationship('Sample', backref='room', lazy='dynamic')
    environment_logs = db.relationship('EnvironmentLog', backref='room', lazy='dynamic')
    
    def __repr__(self):
        return f'<Room {self.name}>'
    
    def update_environment(self, temperature=None, humidity=None, light_level=None):
        if temperature is not None:
            self.temperature = temperature
        if humidity is not None:
            self.humidity = humidity
        if light_level is not None:
            self.light_level = light_level
        self.last_updated = datetime.utcnow()
        
        # Create log entry
        log = EnvironmentLog(
            room_id=self.id,
            temperature=self.temperature,
            humidity=self.humidity,
            light_level=self.light_level
        )
        db.session.add(log)

class EnvironmentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light_level = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EnvironmentLog {self.room_id} at {self.timestamp}>' 