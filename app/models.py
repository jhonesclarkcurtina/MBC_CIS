"""
Church Information System - Database Models
"""
from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='viewer', nullable=False)  # admin, leader, viewer
    caregroup_id = db.Column(db.Integer, db.ForeignKey('caregroups.id'))
    theme = db.Column(db.String(10), default='light')  # light or dark
    status = db.Column(db.String(20), default='active')  # active or inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    caregroup = db.relationship('CareGroup', backref='users', foreign_keys=[caregroup_id])
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password, password)
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_leader(self):
        """Check if user is care group leader"""
        return self.role == 'leader'
    
    def is_active_user(self):
        """Check if user account is active"""
        return self.status == 'active'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Member(db.Model):
    """Member model for church members"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False, index=True)
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))  # Male, Female, Other
    address = db.Column(db.Text)
    contact = db.Column(db.String(20))
    baptism_date = db.Column(db.Date)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.id'))
    caregroup_id = db.Column(db.Integer, db.ForeignKey('caregroups.id'))
    status = db.Column(db.String(20), default='active')  # active or inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ministry = db.relationship('Ministry', backref='members')
    caregroup = db.relationship('CareGroup', backref='members')
    
    def __repr__(self):
        return f'<Member {self.fullname}>'


class CareGroup(db.Model):
    """Care group model"""
    __tablename__ = 'caregroups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    color = db.Column(db.String(7), default='#000000')  # Hex color
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leader = db.relationship('User', backref='led_caregroups', foreign_keys=[leader_id])
    
    def get_member_count(self):
        """Get count of members in this care group"""
        return Member.query.filter_by(caregroup_id=self.id, status='active').count()
    
    def __repr__(self):
        return f'<CareGroup {self.name}>'


class Ministry(db.Model):
    """Ministry model"""
    __tablename__ = 'ministries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_member_count(self):
        """Get count of members in this ministry"""
        return Member.query.filter_by(ministry_id=self.id, status='active').count()
    
    def __repr__(self):
        return f'<Ministry {self.name}>'


class Setting(db.Model):
    """Settings model for system and user preferences"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    setting_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Setting {self.setting_name}>'
