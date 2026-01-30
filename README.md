# Church Information System (CIS)

A modern, secure, and user-friendly web application for managing church members, care groups, and ministries.

## 🎯 Features

### Member Management
- ✅ Add, edit, and view member information
- ✅ Track member details: age, gender, contact, address, baptism date
- ✅ Assign members to ministries and care groups
- ✅ Search and filter members by multiple criteria
- ✅ Mark members as active or inactive (no permanent deletion)

### Care Group Management
- ✅ Create and manage care groups with custom colors
- ✅ Assign leaders to care groups
- ✅ View members within each care group
- ✅ Color-coded care group identification

### Ministry Management
- ✅ Create and manage church ministries
- ✅ Track members by ministry
- ✅ Enable/disable ministries

### User & Role Management
- ✅ **Admin**: Full access to all features
- ✅ **Care Group Leader**: View and manage members in assigned care group
- ✅ **Viewer/Secretary**: View all members, add and edit information

### Security Features
- ✅ Secure login authentication
- ✅ Password hashing with Werkzeug
- ✅ Session management
- ✅ Role-based access control (RBAC)

### Appearance & UX
- ✅ Light and Dark mode support
- ✅ Responsive design (mobile-friendly)
- ✅ Modern, clean UI with Font Awesome icons
- ✅ Smooth transitions and interactive elements

### Settings
- ✅ **Appearance Settings**: Theme selection (Light/Dark)
- ✅ **Account Settings**: Username and password management
- ✅ **Church Settings**: Church information (name, address, contact)
- ✅ **System Settings**: Default theme, pagination options
- ✅ **User Management**: Create and manage users and roles
- ✅ **Ministry Management**: Configure available ministries

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ with Flask 2.3 |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Database | SQLite (file-based) |
| ORM | SQLAlchemy 2.0 |
| Authentication | Flask-Login with Werkzeug hashing |
| Styling | Custom CSS with CSS Variables |

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database (First Time)

The database is automatically created when you run the application. On first run:
- Default admin user: `admin` / `admin123`
- Default care groups: Yellow, Blue, Red
- Default ministries: Youth, Adult, Choir, Ladies, Laymen, Children

### 3. Run the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

### 4. Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Change the admin password immediately in production!**

## 📁 Project Structure

```
MBC_CIS/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes & blueprints
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js      # JavaScript functionality
│   │   └── images/          # Static images
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── auth/            # Authentication pages
│       ├── main/            # Main dashboard pages
│       ├── members/         # Member management pages
│       ├── caregroups/      # Care group pages
│       ├── settings/        # Settings pages
│       └── admin/           # Admin pages
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── church_system.db         # SQLite database (created at runtime)
└── README.md                # This file
```

## 👥 User Roles & Permissions

### Admin
- ✅ View all members
- ✅ Add, edit, deactivate members
- ✅ Manage care groups (create, edit, assign leaders)
- ✅ Manage ministries
- ✅ Manage users (create, edit, assign roles)
- ✅ Access all settings
- ✅ Church information settings
- ✅ System settings

### Care Group Leader
- ✅ View members in their assigned care group only
- ✅ Cannot delete or deactivate members
- ✅ Cannot manage users or system settings
- ✅ Can customize appearance settings

### Viewer / Secretary
- ✅ View all members
- ✅ Add new members
- ✅ Edit member information
- ✅ Cannot delete or deactivate members
- ✅ Cannot manage users
- ✅ Cannot access system settings

## 🗄️ Database Schema

### Users Table
- id, username, password (hashed), role, caregroup_id, theme, status, created_at, updated_at

### Members Table
- id, fullname, age, gender, address, contact, baptism_date, ministry_id, caregroup_id, status, created_at, updated_at

### Care Groups Table
- id, name, color, leader_id, status, created_at, updated_at

### Ministries Table
- id, name, description, status, created_at, updated_at

### Settings Table
- id, setting_name, setting_value, created_at, updated_at

## 🎨 Theme System

The application supports Light and Dark modes:
- **Light Mode**: Clean white interface with blue accents
- **Dark Mode**: Dark theme for reduced eye strain

Theme preference is saved per user in the database.

## 🔒 Security Notes

1. **Password Hashing**: All passwords are hashed using Werkzeug's security functions
2. **Session Management**: Secure session cookies with HTTP-only flag
3. **Database Protection**: SQLite database file is not web-accessible
4. **CSRF Protection**: Available through Flask-WTF (can be enabled)
5. **Role-Based Access**: All routes check user permissions

### Security Recommendations for Production

1. Change the SECRET_KEY in `config.py`:
```python
SECRET_KEY = os.urandom(24).hex()  # Generate random key
```

2. Enable HTTPS:
```python
SESSION_COOKIE_SECURE = True
```

3. Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

4. Set up a proper database:
   - For production, consider PostgreSQL instead of SQLite

5. Enable environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-key
```

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop browsers (1920px and above)
- Tablets (768px - 1024px)
- Mobile phones (320px - 767px)

Mobile view includes:
- Collapsible sidebar navigation
- Touch-friendly buttons and inputs
- Optimized table layouts

## 🎓 Usage Examples

### Adding a New Member
1. Click "Add Member" button on dashboard
2. Fill in member details
3. Select ministry and care group
4. Click "Save Member"

### Creating a Care Group
1. Go to Care Groups → Add Care Group
2. Enter group name and select a color
3. Optionally assign a leader
4. Click "Create Care Group"

### Managing Users
1. Go to Admin → Users
2. Click "Add User" to create new users
3. Assign roles and care groups
4. Edit user details as needed

### Searching Members
1. Go to Members
2. Use search box to find by name
3. Filter by Ministry, Care Group, or Status
4. Results update automatically

## 🐛 Troubleshooting

### Database Issues
- Delete `church_system.db` to reset database (will lose all data)
- Database is recreated automatically on next run

### Port Already in Use
```bash
# Change port in run.py
app.run(port=5001)  # Use different port
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Login Issues
- Verify credentials match exactly (case-sensitive)
- Check that user account is marked as "Active"

## 📞 Support & Maintenance

### Regular Backups
- Copy `church_system.db` regularly for backup
- Consider automated backup solutions in production

### Database Cleanup
- Periodically review inactive members
- Archive old data as needed

### Updates & Upgrades
- Test changes in development environment first
- Keep dependencies updated periodically

## 📄 License

This system is built for church use. Feel free to customize and extend as needed.

## 🙏 Acknowledgments

Built with:
- Flask - Web framework
- SQLAlchemy - ORM
- Flask-Login - Authentication
- Font Awesome - Icons

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Status**: Production Ready
