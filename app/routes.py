"""
Church Information System - Routes (Blueprints)
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Member, CareGroup, Ministry, Setting
from functools import wraps
from datetime import datetime

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
members_bp = Blueprint('members', __name__, url_prefix='/members')
caregroups_bp = Blueprint('caregroups', __name__, url_prefix='/caregroups')
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ==================== DECORATORS ====================

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def leader_or_admin_required(f):
    """Decorator to require leader or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        if not (current_user.is_admin() or current_user.is_leader()):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTH ROUTES ====================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.status == 'inactive':
                flash('Your account has been disabled.', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page - redirect to dashboard if authenticated"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    total_members = Member.query.filter_by(status='active').count()
    total_caregroups = CareGroup.query.filter_by(status='active').count()
    
    # Get member count by ministry
    ministry_stats = db.session.query(
        Ministry.name,
        db.func.count(Member.id).label('count')
    ).outerjoin(Member).filter(
        Member.status == 'active'
    ).group_by(Ministry.id).all()
    
    # Get recent members
    recent_members = Member.query.filter_by(status='active').order_by(
        Member.created_at.desc()
    ).limit(5).all()
    
    # Get care groups
    caregroups = CareGroup.query.filter_by(status='active').all()
    
    return render_template('main/dashboard.html',
                         total_members=total_members,
                         total_caregroups=total_caregroups,
                         ministry_stats=ministry_stats,
                         recent_members=recent_members,
                         caregroups=caregroups)

@main_bp.route('/about')
def about():
    """About page"""
    from config import Config
    return render_template('main/about.html',
                         app_name=Config.APP_NAME,
                         app_version=Config.APP_VERSION,
                         app_author=Config.APP_AUTHOR,
                         app_purpose=Config.APP_PURPOSE)

# ==================== MEMBER ROUTES ====================

@members_bp.route('/')
@login_required
def list_members():
    """List all members with search and filter"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    ministry_id = request.args.get('ministry', type=int)
    caregroup_id = request.args.get('caregroup', type=int)
    status = request.args.get('status', 'active')
    
    query = Member.query
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    
    if current_user.is_leader() and not current_user.is_admin():
        # Leaders can only see their care group members
        query = query.filter_by(caregroup_id=current_user.caregroup_id)
    
    if search:
        query = query.filter(Member.fullname.ilike(f'%{search}%'))
    
    if ministry_id:
        query = query.filter_by(ministry_id=ministry_id)
    
    if caregroup_id:
        query = query.filter_by(caregroup_id=caregroup_id)
    
    paginated = query.paginate(page=page, per_page=10)
    members = paginated.items
    
    ministries = Ministry.query.filter_by(status='active').all()
    caregroups = CareGroup.query.filter_by(status='active').all()
    
    return render_template('members/list.html',
                         members=members,
                         paginated=paginated,
                         ministries=ministries,
                         caregroups=caregroups,
                         search=search,
                         selected_ministry=ministry_id,
                         selected_caregroup=caregroup_id,
                         selected_status=status)

@members_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_member():
    """Add new member"""
    if not (current_user.is_admin() or current_user.role == 'viewer'):
        flash('You do not have permission to add members.', 'error')
        return redirect(url_for('members.list_members'))
    
    if request.method == 'POST':
        try:
            member = Member(
                fullname=request.form.get('fullname'),
                gender=request.form.get('gender'),
                address=request.form.get('address'),
                contact=request.form.get('contact'),
                ministry_id=request.form.get('ministry_id', type=int),
                caregroup_id=request.form.get('caregroup_id', type=int),
                status='active'
            )
            
            date_of_birth_str = request.form.get('date_of_birth')
            if date_of_birth_str:
                member.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            
            age_str = request.form.get('age')
            if age_str:
                member.age = int(age_str)
            
            baptism_date_str = request.form.get('baptism_date')
            if baptism_date_str:
                member.baptism_date = datetime.strptime(baptism_date_str, '%Y-%m-%d').date()
            
            db.session.add(member)
            db.session.commit()
            flash(f'Member {member.fullname} added successfully!', 'success')
            return redirect(url_for('members.list_members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding member: {str(e)}', 'error')
    
    ministries = Ministry.query.filter_by(status='active').all()
    caregroups = CareGroup.query.filter_by(status='active').all()
    
    return render_template('members/add.html',
                         ministries=ministries,
                         caregroups=caregroups)

@members_bp.route('/<int:member_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    """Edit member"""
    member = Member.query.get_or_404(member_id)
    
    # Check permissions
    if current_user.is_leader() and not current_user.is_admin():
        if member.caregroup_id != current_user.caregroup_id:
            flash('You can only edit members in your care group.', 'error')
            return redirect(url_for('members.list_members'))
    elif not (current_user.is_admin() or current_user.role == 'viewer'):
        flash('You do not have permission to edit members.', 'error')
        return redirect(url_for('members.list_members'))
    
    if request.method == 'POST':
        try:
            member.fullname = request.form.get('fullname')
            member.gender = request.form.get('gender')
            member.address = request.form.get('address')
            member.contact = request.form.get('contact')
            member.ministry_id = request.form.get('ministry_id', type=int)
            member.caregroup_id = request.form.get('caregroup_id', type=int)
            
            date_of_birth_str = request.form.get('date_of_birth')
            if date_of_birth_str:
                member.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            
            age_str = request.form.get('age')
            if age_str:
                member.age = int(age_str)
            
            baptism_date_str = request.form.get('baptism_date')
            if baptism_date_str:
                member.baptism_date = datetime.strptime(baptism_date_str, '%Y-%m-%d').date()
            
            member.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'Member {member.fullname} updated successfully!', 'success')
            return redirect(url_for('members.list_members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating member: {str(e)}', 'error')
    
    ministries = Ministry.query.filter_by(status='active').all()
    caregroups = CareGroup.query.filter_by(status='active').all()
    
    return render_template('members/edit.html',
                         member=member,
                         ministries=ministries,
                         caregroups=caregroups)

@members_bp.route('/<int:member_id>')
@login_required
def view_member(member_id):
    """View member details"""
    member = Member.query.get_or_404(member_id)
    
    # Check permissions
    if current_user.is_leader() and not current_user.is_admin():
        if member.caregroup_id != current_user.caregroup_id:
            flash('You can only view members in your care group.', 'error')
            return redirect(url_for('members.list_members'))
    
    return render_template('members/view.html', member=member)

@members_bp.route('/<int:member_id>/deactivate', methods=['POST'])
@login_required
def deactivate_member(member_id):
    """Deactivate (mark as inactive) a member"""
    member = Member.query.get_or_404(member_id)
    
    if not current_user.is_admin():
        flash('Only admins can deactivate members.', 'error')
        return redirect(url_for('members.list_members'))
    
    try:
        member.status = 'inactive'
        member.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Member {member.fullname} has been marked as inactive.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deactivating member: {str(e)}', 'error')
    
    return redirect(url_for('members.list_members'))

# ==================== CARE GROUP ROUTES ====================

@caregroups_bp.route('/')
@login_required
def list_caregroups():
    """List all care groups"""
    caregroups = CareGroup.query.filter_by(status='active').all()
    return render_template('caregroups/list.html', caregroups=caregroups)

@caregroups_bp.route('/<int:caregroup_id>')
@login_required
def view_caregroup(caregroup_id):
    """View care group details and members"""
    caregroup = CareGroup.query.get_or_404(caregroup_id)
    
    # Check permissions
    if current_user.is_leader() and not current_user.is_admin():
        if caregroup.id != current_user.caregroup_id:
            flash('You can only view your assigned care group.', 'error')
            return redirect(url_for('caregroups.list_caregroups'))
    
    page = request.args.get('page', 1, type=int)
    members = caregroup.members
    
    return render_template('caregroups/view.html',
                         caregroup=caregroup,
                         members=members)

@caregroups_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_caregroup():
    """Add new care group"""
    if request.method == 'POST':
        try:
            caregroup = CareGroup(
                name=request.form.get('name'),
                color=request.form.get('color', '#000000'),
                status='active'
            )
            
            leader_id = request.form.get('leader_id', type=int)
            if leader_id:
                caregroup.leader_id = leader_id
            
            db.session.add(caregroup)
            db.session.commit()
            flash(f'Care group {caregroup.name} added successfully!', 'success')
            return redirect(url_for('caregroups.list_caregroups'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding care group: {str(e)}', 'error')
    
    leaders = User.query.filter(User.role != 'admin', User.status == 'active').all()
    return render_template('caregroups/add.html', leaders=leaders)

@caregroups_bp.route('/<int:caregroup_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_caregroup(caregroup_id):
    """Edit care group"""
    caregroup = CareGroup.query.get_or_404(caregroup_id)
    
    if request.method == 'POST':
        try:
            caregroup.name = request.form.get('name')
            caregroup.color = request.form.get('color', '#000000')
            
            leader_id = request.form.get('leader_id', type=int)
            caregroup.leader_id = leader_id if leader_id else None
            
            caregroup.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'Care group {caregroup.name} updated successfully!', 'success')
            return redirect(url_for('caregroups.list_caregroups'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating care group: {str(e)}', 'error')
    
    leaders = User.query.filter(User.role != 'admin', User.status == 'active').all()
    return render_template('caregroups/edit.html',
                         caregroup=caregroup,
                         leaders=leaders)

# ==================== SETTINGS ROUTES ====================

@settings_bp.route('/appearance')
@login_required
def appearance():
    """Appearance settings"""
    return render_template('settings/appearance.html')

@settings_bp.route('/appearance/theme', methods=['POST'])
@login_required
def set_theme():
    """Set user theme preference"""
    theme = request.json.get('theme', 'light')
    if theme not in ['light', 'dark']:
        return jsonify({'success': False, 'message': 'Invalid theme'}), 400
    
    try:
        current_user.theme = theme
        db.session.commit()
        return jsonify({'success': True, 'message': 'Theme updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/account')
@login_required
def account():
    """Account settings"""
    return render_template('settings/account.html', user=current_user)

@settings_bp.route('/account/update', methods=['POST'])
@login_required
def update_account():
    """Update account settings"""
    try:
        current_user.username = request.form.get('username', current_user.username)
        
        password = request.form.get('password')
        if password:
            current_user.set_password(password)
        
        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('settings.account'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating account: {str(e)}', 'error')
        return redirect(url_for('settings.account'))

@settings_bp.route('/church', methods=['GET', 'POST'])
@admin_required
def church_settings():
    """Church settings"""
    if request.method == 'POST':
        try:
            church_name = Setting.query.filter_by(setting_name='church_name').first()
            if not church_name:
                church_name = Setting(setting_name='church_name')
            church_name.setting_value = request.form.get('church_name', '')
            
            church_address = Setting.query.filter_by(setting_name='church_address').first()
            if not church_address:
                church_address = Setting(setting_name='church_address')
            church_address.setting_value = request.form.get('church_address', '')
            
            church_contact = Setting.query.filter_by(setting_name='church_contact').first()
            if not church_contact:
                church_contact = Setting(setting_name='church_contact')
            church_contact.setting_value = request.form.get('church_contact', '')
            
            db.session.add_all([church_name, church_address, church_contact])
            db.session.commit()
            flash('Church settings updated successfully!', 'success')
            return redirect(url_for('settings.church_settings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating church settings: {str(e)}', 'error')
    
    church_name = Setting.query.filter_by(setting_name='church_name').first()
    church_address = Setting.query.filter_by(setting_name='church_address').first()
    church_contact = Setting.query.filter_by(setting_name='church_contact').first()
    
    return render_template('settings/church.html',
                         church_name=church_name.setting_value if church_name else '',
                         church_address=church_address.setting_value if church_address else '',
                         church_contact=church_contact.setting_value if church_contact else '')

# ==================== ADMIN ROUTES ====================

@admin_bp.route('/users')
@admin_required
def manage_users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                return redirect(url_for('admin.add_user'))
            
            user = User(
                username=username,
                role=request.form.get('role', 'viewer'),
                status='active'
            )
            user.set_password(request.form.get('password'))
            
            caregroup_id = request.form.get('caregroup_id', type=int)
            if caregroup_id:
                user.caregroup_id = caregroup_id
            
            db.session.add(user)
            db.session.commit()
            flash(f'User {username} added successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding user: {str(e)}', 'error')
    
    caregroups = CareGroup.query.filter_by(status='active').all()
    return render_template('admin/add_user.html', caregroups=caregroups)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            user.role = request.form.get('role', 'viewer')
            user.status = request.form.get('status', 'active')
            
            caregroup_id = request.form.get('caregroup_id', type=int)
            user.caregroup_id = caregroup_id if caregroup_id else None
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'User {user.username} updated successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    caregroups = CareGroup.query.filter_by(status='active').all()
    return render_template('admin/edit_user.html',
                         user=user,
                         caregroups=caregroups)

@admin_bp.route('/ministries')
@admin_required
def manage_ministries():
    """Manage ministries"""
    ministries = Ministry.query.all()
    return render_template('admin/ministries.html', ministries=ministries)

@admin_bp.route('/ministries/add', methods=['GET', 'POST'])
@admin_required
def add_ministry():
    """Add new ministry"""
    if request.method == 'POST':
        try:
            ministry = Ministry(
                name=request.form.get('name'),
                description=request.form.get('description', ''),
                status='active'
            )
            db.session.add(ministry)
            db.session.commit()
            flash(f'Ministry {ministry.name} added successfully!', 'success')
            return redirect(url_for('admin.manage_ministries'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ministry: {str(e)}', 'error')
    
    return render_template('admin/add_ministry.html')

@admin_bp.route('/ministries/<int:ministry_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_ministry(ministry_id):
    """Edit ministry"""
    ministry = Ministry.query.get_or_404(ministry_id)
    
    if request.method == 'POST':
        try:
            ministry.name = request.form.get('name')
            ministry.description = request.form.get('description', '')
            ministry.status = request.form.get('status', 'active')
            ministry.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'Ministry {ministry.name} updated successfully!', 'success')
            return redirect(url_for('admin.manage_ministries'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating ministry: {str(e)}', 'error')
    
    return render_template('admin/edit_ministry.html', ministry=ministry)

@admin_bp.route('/ministries/<int:ministry_id>/delete', methods=['POST'])
@admin_required
def delete_ministry(ministry_id):
    """Delete ministry"""
    ministry = Ministry.query.get_or_404(ministry_id)
    
    try:
        ministry.status = 'inactive'
        db.session.commit()
        flash(f'Ministry {ministry.name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ministry: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_ministries'))

@admin_bp.route('/system')
@admin_required
def system_settings():
    """System settings"""
    default_theme = Setting.query.filter_by(setting_name='default_theme').first()
    items_per_page = Setting.query.filter_by(setting_name='items_per_page').first()
    
    return render_template('admin/system_settings.html',
                         default_theme=default_theme.setting_value if default_theme else 'light',
                         items_per_page=items_per_page.setting_value if items_per_page else '10')

@admin_bp.route('/system/update', methods=['POST'])
@admin_required
def update_system_settings():
    """Update system settings"""
    try:
        default_theme = Setting.query.filter_by(setting_name='default_theme').first()
        if not default_theme:
            default_theme = Setting(setting_name='default_theme')
        default_theme.setting_value = request.form.get('default_theme', 'light')
        
        items_per_page = Setting.query.filter_by(setting_name='items_per_page').first()
        if not items_per_page:
            items_per_page = Setting(setting_name='items_per_page')
        items_per_page.setting_value = request.form.get('items_per_page', '10')
        
        db.session.add_all([default_theme, items_per_page])
        db.session.commit()
        flash('System settings updated successfully!', 'success')
        return redirect(url_for('admin.system_settings'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating system settings: {str(e)}', 'error')
        return redirect(url_for('admin.system_settings'))
