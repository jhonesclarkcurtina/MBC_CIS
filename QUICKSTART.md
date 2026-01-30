# Church Information System - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd "path/to/MBC_CIS"
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Open in Browser
Go to: **http://localhost:5000**

## 🔑 Default Login Credentials

```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT**: Change this password after first login!

## 📋 Initial Setup Tasks

After logging in, complete these setup steps:

### 1. Update Admin Password
- Go to **Settings** → **Account**
- Enter new password
- Click "Save Changes"

### 2. Add Church Information
- Go to **Admin** → **Church Info**
- Enter your church name, address, and contact
- Click "Save Changes"

### 3. Create Users
- Go to **Admin** → **Users** → **Add User**
- Create accounts for:
  - Secretaries (Role: Viewer)
  - Care Group Leaders (Role: Leader)
  - Other Admins if needed

### 4. Assign Care Group Leaders
- Go to **Care Groups**
- Click "Edit" on each care group
- Assign a leader from the dropdown

### 5. Add Members
- Go to **Members** → **Add Member**
- Fill in member details
- Assign to ministry and care group
- Click "Save Member"

## 🎨 Customize Appearance

### Change Theme
- Click the **Moon/Sun icon** (top right) to toggle Dark/Light mode
- Or go to **Settings** → **Appearance**

### Customize Care Group Colors
- Go to **Admin** → **Care Groups** (for admins)
- Click "Edit" and select a new color for each group

## 📊 Dashboard Features

The main dashboard shows:
- **Total Members**: Count of active members
- **Care Groups**: Number of care groups
- **Members by Ministry**: Bar chart of ministry distribution
- **Care Groups Overview**: Members and leaders per group
- **Recent Members**: Latest added members
- **Quick Actions**: Shortcuts to common tasks

## 👥 Managing Different User Types

### Admin (System Manager)
- Can do everything
- Manages users and roles
- Configures system settings

### Care Group Leader
- Manages members in their care group
- Can view member details
- Cannot delete members or manage system

### Secretary / Viewer
- Can view all members
- Can add and edit members
- Cannot delete or deactivate
- Cannot access admin features

## 🔍 Finding Members

### By Name
- Go to **Members**
- Type name in search box
- Results appear instantly

### By Ministry
- Go to **Members**
- Select ministry from dropdown
- Filter results

### By Care Group
- Go to **Care Groups**
- Click on care group
- See all members in that group

## 💾 Backup Your Data

Your database is stored in: `church_system.db`

**Weekly Backup Steps:**
1. Locate `church_system.db` file
2. Copy to backup location
3. Store securely

## 🛠️ Troubleshooting

### Application won't start
```bash
# Make sure you're in the correct directory
cd "path/to/MBC_CIS"

# Reinstall dependencies
pip install -r requirements.txt

# Try running again
python run.py
```

### Can't login
- Check username and password (case-sensitive)
- Verify user account is "Active" (not "Inactive")
- Contact your system admin

### Lost admin password
- Delete `church_system.db` (⚠️ loses all data)
- Restart application - new admin account will be created
- Default: admin / admin123

### Database issues
```bash
# Backup first!
# Then delete database to reset
del church_system.db

# Restart app - database recreates automatically
python run.py
```

## 📝 Common Tasks

### Add a New Member
1. Click **"Add Member"** button (dashboard or Members page)
2. Fill in:
   - Full Name (required)
   - Age
   - Gender
   - Address
   - Contact Number
   - Baptism Date (optional)
   - Ministry (dropdown)
   - Care Group (dropdown)
3. Click **"Save Member"**

### Edit Member Information
1. Go to **Members**
2. Click **View** next to member
3. Click **Edit** button
4. Update information
5. Click **"Save Changes"**

### Deactivate a Member
1. Go to **Members**
2. Click ⋮ (more options)
3. Click **Deactivate**
- Note: Not permanently deleted, can be reactivated

### Assign Member to Care Group
1. Go to **Members** → Edit member
2. Select care group from dropdown
3. Click "Save Changes"

### Create Care Group
1. Go to **Care Groups** → **Add Care Group**
2. Enter name (e.g., "Yellow", "Blue")
3. Select color
4. Assign leader (optional)
5. Click **"Create Care Group"**

## 🌐 Access from Other Computers

If others need to access from another computer:

1. Find your computer's IP address:
   ```bash
   ipconfig  (Windows)
   ifconfig  (Mac/Linux)
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. In `run.py`, change:
   ```python
   app.run(host='0.0.0.0', port=5000)  # Already set!
   ```

3. Others can access:
   ```
   http://YOUR_IP:5000
   Example: http://192.168.1.100:5000
   ```

## 📚 Feature Guide

| Feature | User Types | Location |
|---------|-----------|----------|
| View Members | All | Members page |
| Add/Edit Members | Admin, Viewer | Members page |
| Deactivate Members | Admin | Members page |
| Manage Care Groups | Admin | Care Groups page |
| Manage Users | Admin | Admin → Users |
| Manage Ministries | Admin | Admin → Ministries |
| Church Settings | Admin | Admin → Church Info |
| System Settings | Admin | Admin → System |
| Appearance Settings | All | Settings → Appearance |
| Account Settings | All | Settings → Account |

## ✅ System Health Check

Before going live, verify:

- [ ] Admin password changed
- [ ] Church information updated
- [ ] Care groups created and leaders assigned
- [ ] Default ministries configured
- [ ] At least one test member added
- [ ] All users created with correct roles
- [ ] Theme preferences working
- [ ] Search and filters working
- [ ] Database backup taken

## 📞 Need Help?

Refer to the full **README.md** for:
- Detailed feature descriptions
- Technical documentation
- Security recommendations
- Database schema
- Troubleshooting guide

---

**You're all set!** Start using the Church Information System. 🙏
