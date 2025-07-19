// Main JavaScript functionality for the Bus Pass System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc2626';
                } else {
                    field.style.borderColor = '#e5e7eb';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Registration number formatting
    const regNoField = document.querySelector('input[name="reg_no"]');
    if (regNoField) {
        regNoField.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }

    // Password strength indicator (for registration)
    const passwordField = document.querySelector('input[name="password"]');
    if (passwordField && passwordField.form.querySelector('input[name="reg_no"]')) {
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength';
        passwordField.parentNode.appendChild(strengthIndicator);

        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            let message = '';

            if (password.length >= 6) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;

            switch (strength) {
                case 0:
                case 1:
                    message = 'Weak';
                    strengthIndicator.style.color = '#dc2626';
                    break;
                case 2:
                    message = 'Fair';
                    strengthIndicator.style.color = '#f59e0b';
                    break;
                case 3:
                    message = 'Good';
                    strengthIndicator.style.color = '#2563EB';
                    break;
                case 4:
                    message = 'Strong';
                    strengthIndicator.style.color = '#16a34a';
                    break;
            }

            strengthIndicator.textContent = password ? `Password strength: ${message}` : '';
        });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Mobile menu toggle (if needed in future)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Table sorting functionality for admin dashboard
    const tableHeaders = document.querySelectorAll('th[data-sort]');
    tableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const column = this.cellIndex;
            const isAscending = this.classList.contains('sort-asc');

            rows.sort((a, b) => {
                const aValue = a.cells[column].textContent.trim();
                const bValue = b.cells[column].textContent.trim();
                
                if (isAscending) {
                    return bValue.localeCompare(aValue);
                } else {
                    return aValue.localeCompare(bValue);
                }
            });

            // Remove existing sort classes
            tableHeaders.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            
            // Add new sort class
            this.classList.add(isAscending ? 'sort-desc' : 'sort-asc');

            // Reorder table rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });

    // QR code download functionality
    window.downloadQR = function(filename, url) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(function() {
            // Create temporary notification
            const notification = document.createElement('div');
            notification.textContent = 'Copied to clipboard!';
            notification.style.position = 'fixed';
            notification.style.top = '20px';
            notification.style.right = '20px';
            notification.style.background = '#16a34a';
            notification.style.color = 'white';
            notification.style.padding = '10px 20px';
            notification.style.borderRadius = '5px';
            notification.style.zIndex = '1000';
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 2000);
        });
    };

    // Offline detection
    window.addEventListener('online', function() {
        showNetworkStatus('Connection restored', 'success');
    });

    window.addEventListener('offline', function() {
        showNetworkStatus('No internet connection', 'error');
    });

    function showNetworkStatus(message, type) {
        const notification = document.createElement('div');
        notification.className = `flash-message flash-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'wifi' : 'exclamation-triangle'}"></i>
            ${message}
            <button class="close-flash" onclick="this.parentElement.remove()">×</button>
        `;
        
        const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
        flashContainer.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    function createFlashContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }
});

// Service Worker registration (for future PWA functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// Performance monitoring
window.addEventListener('load', function() {
    // Log page load time
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log('Page load time:', loadTime + 'ms');
    
    // Monitor for slow network
    if (navigator.connection) {
        const connection = navigator.connection;
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
            console.log('Slow network detected');
            // Could implement data-saving features here
        }
    }
});