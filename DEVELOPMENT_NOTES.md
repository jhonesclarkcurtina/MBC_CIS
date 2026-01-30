# Church Information System - Development Notes

## Project Overview

**Name**: Church Information System (CIS)  
**Version**: 1.0.0  
**Framework**: Flask 2.3  
**Database**: SQLite  
**Status**: Production Ready  

## Architecture

### MVC-like Structure
- **Models** (`models.py`) - SQLAlchemy ORM definitions
- **Views** (`templates/`) - Jinja2 HTML templates
- **Controllers** (`routes.py`) - Flask routes and business logic

### Modular Design
- **Blueprints** - 6 separate modules for organization
  - `auth_bp` - Authentication
  - `main_bp` - Dashboard and main pages
  - `members_bp` - Member management
  - `caregroups_bp` - Care group management
  - `settings_bp` - User and system settings
  - `admin_bp` - Admin functions

## Key Design Decisions

### 1. No Hard Delete on Members
- Members marked as "inactive" instead of deletion
- Preserves historical data
- Recoverable if needed
- Complies with church record-keeping practices

### 2. Role-Based Access Control (RBAC)
- 3 roles: Admin, Leader, Viewer
- Decorator-based permission checking
- Routes verify permissions
- Frontend hides unauthorized actions

### 3. Flexible Settings System
- Key-value pair storage in database
- Easy to add new settings
- Per-user preferences (theme)
- System-wide settings (admin)

### 4. Light/Dark Mode as Core Feature
- CSS Variables for easy theming
- Per-user preference storage
- Applies instantly without page reload
- Supports system preference detection

### 5. Care Groups with Visual Identity
- Color coding for quick identification
- Leader assignment for management
- Flexible number of groups
- Easy to rename or modify

## Code Organization

### app/__init__.py
- **Responsibility**: Application factory
- **Key Functions**:
  - `create_app()` - Initialize Flask app
  - Database initialization
  - Blueprint registration
  - User loader setup
- **Why**: Enables testing and multiple configs

### app/models.py
- **Responsibility**: Data models
- **Classes**: User, Member, CareGroup, Ministry, Setting
- **Key Features**:
  - SQLAlchemy ORM
  - Relationships and foreign keys
  - Computed properties (get_member_count)
  - Helper methods (set_password, check_password)

### app/routes.py
- **Responsibility**: All application routes
- **Structure**: 6 blueprints with clear separation
- **Key Patterns**:
  - Decorators for access control
  - Try-except for error handling
  - Flash messages for user feedback
  - Pagination for large datasets

### app/static/css/style.css
- **Responsibility**: All styling
- **Features**:
  - CSS Variables for theming
  - Responsive design with media queries
  - Component classes (btn, card, badge, etc.)
  - Utility classes (mt-1, mb-2, etc.)
  - Dark mode support

### app/static/js/main.js
- **Responsibility**: Client-side functionality
- **Features**:
  - Theme manager class
  - Form validation
  - Modal management
  - Auto-hiding alerts
  - Keyboard shortcuts

## Database Design Principles

### Relationships
```
User
  ├─ CareGroup (many-to-one) - Which care group leads
  ├─ Led_CareGroups (one-to-many) - Which groups they lead
  └─ Created members (implicit)

Member
  ├─ Ministry (many-to-one)
  ├─ CareGroup (many-to-one)
  └─ Timestamps (created_at, updated_at)

CareGroup
  ├─ Leader (User)
  ├─ Members (many-to-many)
  └─ Users (member managers)

Ministry
  ├─ Members (one-to-many)

Settings
  └─ Key-value storage
```

### Indexing Strategy
- User.username - Frequently searched
- Member.fullname - Search by name
- CareGroup.name - Filter by group
- Setting.setting_name - Lookup settings

## Security Measures Implemented

### 1. Password Security
```python
# Hash on set
user.set_password(password)  # Uses generate_password_hash

# Verify on login
user.check_password(password)  # Uses check_password_hash
```

### 2. Route Protection
```python
@login_required  # Prevents unauthenticated access
@admin_required  # Ensures admin role
@leader_or_admin_required  # Role-based access
```

### 3. Session Management
```python
SESSION_COOKIE_HTTPONLY = True  # Prevent XSS
SESSION_COOKIE_SAMESITE = 'Lax'  # Prevent CSRF
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
```

### 4. User Status Control
- Active/Inactive accounts
- Can disable users without deletion
- Checked on login

## Performance Considerations

### Database
- Pagination (10 items per page default)
- Indexes on frequently searched columns
- Efficient queries using SQLAlchemy

### Frontend
- CSS Variables (no runtime calculations)
- Minimal JavaScript
- Font Awesome CDN for icons
- No external framework dependencies

### Network
- Gzip compression (via server)
- Efficient HTML templates
- Minimal CSS/JS files

## Testing Recommendations

### Unit Tests
```python
# Test models
def test_user_password_hashing()
def test_member_creation()
def test_caregroup_member_count()

# Test routes
def test_login_success()
def test_login_failure()
def test_member_add_permission()
def test_member_edit_permission()
```

### Integration Tests
```python
# Test workflows
def test_create_user_and_login()
def test_add_member_to_caregroup()
def test_leader_can_view_group_members()
```

### User Acceptance Tests
- [ ] Login with each role
- [ ] Add and edit members
- [ ] Create care groups
- [ ] Toggle light/dark mode
- [ ] Search and filter
- [ ] Responsive on mobile

## Deployment Guide

### Development
```bash
export FLASK_ENV=development
python run.py
```

### Production
```bash
# 1. Install gunicorn
pip install gunicorn

# 2. Set environment
export FLASK_ENV=production
export SECRET_KEY=your-secure-key

# 3. Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 4. Use reverse proxy (nginx)
# Forward requests from port 80/443 to 5000
```

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Future Enhancements

### Features to Consider
1. **Attendance System** - Track attendance at meetings
2. **Contact Notes** - Add notes to member records
3. **File Storage** - Upload documents for members
4. **Email Integration** - Send emails to groups
5. **SMS Alerts** - Text message notifications
6. **Reports** - Generate member reports
7. **Export** - Export to Excel/PDF
8. **Statistics** - Advanced analytics
9. **Activity Log** - Track system changes
10. **Multi-Language** - Internationalization

### Performance Improvements
1. Add caching (Redis)
2. Optimize database queries
3. Implement database connection pooling
4. Add full-text search
5. Implement lazy loading

### Security Enhancements
1. Two-factor authentication
2. API key authentication
3. Rate limiting
4. HTTPS enforcement
5. Content Security Policy headers
6. CORS configuration

## Troubleshooting Guide

### Common Issues

**Issue**: Database locked
**Solution**: Ensure only one instance running

**Issue**: Static files not loading
**Solution**: Check CSS/JS paths in config

**Issue**: Styling broken in dark mode
**Solution**: Clear browser cache, verify CSS variables

**Issue**: Login fails
**Solution**: Check database, verify admin account

## File Location Reference

| File | Purpose | Size (approx) |
|------|---------|---------------|
| app/__init__.py | App factory | 80 lines |
| app/models.py | Data models | 150 lines |
| app/routes.py | All routes | 600+ lines |
| app/static/css/style.css | Styling | 800 lines |
| app/static/js/main.js | JavaScript | 200 lines |
| config.py | Configuration | 50 lines |
| run.py | Entry point | 15 lines |
| 18 templates | HTML pages | 1000+ lines |

## Version Control Strategy

### Branches
- `main` - Production code
- `develop` - Development branch
- `feature/*` - Feature branches

### Commits
- Meaningful commit messages
- One logical change per commit
- Reference issue numbers

### Tags
- `v1.0.0` - Release versions
- Semantic versioning

## Configuration Management

### Environment Variables
```bash
FLASK_ENV=development|production
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///church_system.db
DEBUG=True|False
```

### Config Files
```python
# Development
SQLALCHEMY_ECHO = True
DEBUG = True

# Production
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
DEBUG = False
```

## Maintenance Tasks

### Weekly
- Review error logs
- Check database size
- Verify backups

### Monthly
- Update dependencies (minor versions)
- Review user access logs
- Clean up inactive sessions

### Quarterly
- Security audit
- Performance review
- Database optimization

### Annually
- Major version updates
- Feature review
- Security assessment

## Documentation Structure

```
/
├── README.md - Full documentation
├── QUICKSTART.md - Getting started guide
├── IMPLEMENTATION_SUMMARY.md - Technical overview
└── DEVELOPMENT_NOTES.md - This file
```

## Key Metrics

- **Number of Templates**: 18
- **Number of Routes**: 31
- **Number of Models**: 5
- **Lines of Code**: 3000+
- **CSS Rules**: 200+
- **Database Tables**: 5
- **User Roles**: 3

## Support & Maintenance

### For Users
- See QUICKSTART.md
- See README.md sections

### For Developers
- Code is well-commented
- Variables are self-documenting
- Consistent naming conventions

### For System Admins
- Database in church_system.db
- Logs available in console
- Config in config.py

## License & Attribution

- Flask - BSD License
- SQLAlchemy - MIT License
- Werkzeug - BSD License
- Flask-Login - MIT License
- Font Awesome - Various (mostly free)

---

**Last Updated**: January 2026  
**Maintained By**: Development Team  
**Status**: Active & Supported
