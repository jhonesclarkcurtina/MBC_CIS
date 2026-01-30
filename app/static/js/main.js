/* Church Information System - JavaScript */

// Theme Management
class ThemeManager {
    constructor() {
        this.html = document.documentElement;
        this.toggleBtn = document.getElementById('themeToggle');
        this.currentTheme = this.getStoredTheme() || 'light';
        
        this.init();
    }
    
    init() {
        this.applyTheme(this.currentTheme);
        
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }
    
    getStoredTheme() {
        // Check localStorage
        const stored = localStorage.getItem('theme');
        if (stored) return stored;
        
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        return 'light';
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        this.saveTheme();
    }
    
    applyTheme(theme) {
        this.html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update toggle button appearance
        if (this.toggleBtn) {
            const icon = this.toggleBtn.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }
    
    saveTheme() {
        // Send to server
        fetch('/settings/appearance/theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ theme: this.currentTheme })
        })
        .catch(error => console.error('Error saving theme:', error));
    }
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    initializeSidebar();
    initializeSearchForms();
});

// Sidebar Toggle for Mobile
function initializeSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
}

// Initialize Search Forms
function initializeSearchForms() {
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                form.submit();
            });
        });
    });
}

// Utility Functions

// Format date
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format age
function calculateAge(birthDate) {
    if (!birthDate) return '';
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}

// Confirm dialog
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Show loading spinner
function showSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    document.body.appendChild(spinner);
}

// Hide loading spinner
function hideSpinner() {
    const spinner = document.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Auto-hide alerts after 5 seconds
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

document.addEventListener('DOMContentLoaded', autoHideAlerts);

// Modal Management
class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = this.modal?.querySelector('.modal-close');
        
        if (this.modal) {
            this.init();
        }
    }
    
    init() {
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
        
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
    }
    
    show() {
        this.modal.classList.add('show');
    }
    
    close() {
        this.modal.classList.remove('show');
    }
}

// Form Validation
class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.validate(e));
        }
    }
    
    validate(e) {
        const inputs = this.form.querySelectorAll('[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.markInvalid(input);
                isValid = false;
            } else {
                this.markValid(input);
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    }
    
    markInvalid(input) {
        input.classList.add('is-invalid');
        const errorMsg = input.parentElement.querySelector('.invalid-feedback');
        if (!errorMsg) {
            const msg = document.createElement('small');
            msg.className = 'invalid-feedback';
            msg.textContent = 'This field is required';
            input.parentElement.appendChild(msg);
        }
    }
    
    markValid(input) {
        input.classList.remove('is-invalid');
    }
}

// Table Sort
class TableSort {
    constructor(tableId) {
        this.table = document.getElementById(tableId);
        if (this.table) {
            this.init();
        }
    }
    
    init() {
        const headers = this.table.querySelectorAll('thead th[data-sortable]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => this.sort(header));
        });
    }
    
    sort(header) {
        const columnIndex = Array.from(header.parentElement.children).indexOf(header);
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        const isAsc = header.classList.contains('asc');
        
        rows.sort((a, b) => {
            const aVal = a.children[columnIndex].textContent.trim();
            const bVal = b.children[columnIndex].textContent.trim();
            
            if (!isNaN(aVal) && !isNaN(bVal)) {
                return isAsc ? bVal - aVal : aVal - bVal;
            }
            
            return isAsc ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
        });
        
        rows.forEach(row => tbody.appendChild(row));
        
        // Update sort indicator
        this.table.querySelectorAll('thead th').forEach(th => th.classList.remove('asc', 'desc'));
        header.classList.add(isAsc ? 'desc' : 'asc');
    }
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
            new bootstrap.Tooltip(el);
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
});
