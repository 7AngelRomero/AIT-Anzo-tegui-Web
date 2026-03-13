// Sistema de notificaciones sin React - JavaScript Vanilla

class NotificationSystem {
    constructor() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    init() {
        // Crear contenedor de notificaciones
        this.container = document.getElementById('notification-root');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notification-root';
            document.body.appendChild(this.container);
        }

        // Estilos CSS
        this.injectStyles();

        // Procesar mensajes de Django al cargar
        this.processDjangoMessages();
    }

    injectStyles() {
        if (document.getElementById('notification-styles')) return;

        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            #notification-root {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                pointer-events: none;
            }

            .notification {
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                padding: 16px 20px;
                margin-bottom: 10px;
                min-width: 300px;
                max-width: 400px;
                display: flex;
                align-items: center;
                gap: 12px;
                pointer-events: auto;
                animation: slideIn 0.3s ease-out;
                border-left: 4px solid;
            }

            .notification.removing {
                animation: slideOut 0.3s ease-out forwards;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }

            .notification-icon {
                font-size: 24px;
                flex-shrink: 0;
            }

            .notification-content {
                flex: 1;
            }

            .notification-message {
                margin: 0;
                font-size: 14px;
                line-height: 1.4;
                color: #333;
            }

            .notification-close {
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #999;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }

            .notification-close:hover {
                color: #333;
            }

            .notification.success {
                border-left-color: #27ae60;
            }

            .notification.success .notification-icon {
                color: #27ae60;
            }

            .notification.error {
                border-left-color: #e74c3c;
            }

            .notification.error .notification-icon {
                color: #e74c3c;
            }

            .notification.warning {
                border-left-color: #f39c12;
            }

            .notification.warning .notification-icon {
                color: #f39c12;
            }

            .notification.info {
                border-left-color: #3498db;
            }

            .notification.info .notification-icon {
                color: #3498db;
            }
        `;
        document.head.appendChild(style);
    }

    getIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        notification.innerHTML = `
            <div class="notification-icon">${this.getIcon(type)}</div>
            <div class="notification-content">
                <p class="notification-message">${message}</p>
            </div>
            <button class="notification-close" aria-label="Cerrar">×</button>
        `;

        this.container.appendChild(notification);

        // Cerrar al hacer clic en el botón
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.remove(notification));

        // Auto-cerrar después de la duración
        if (duration > 0) {
            setTimeout(() => this.remove(notification), duration);
        }

        return notification;
    }

    remove(notification) {
        notification.classList.add('removing');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    processDjangoMessages() {
        const messages = document.querySelectorAll('.django-message');
        messages.forEach(msg => {
            const type = msg.getAttribute('data-type') || 'info';
            const message = msg.textContent.trim();
            if (message) {
                this.show(message, type);
            }
        });
    }
}

// Inicializar sistema de notificaciones
let notificationSystem;

document.addEventListener('DOMContentLoaded', function() {
    notificationSystem = new NotificationSystem();

    // Funciones globales
    window.showNotification = (message, type = 'info', duration = 5000) => {
        return notificationSystem.show(message, type, duration);
    };

    window.showSuccess = (message, duration = 5000) => {
        return notificationSystem.show(message, 'success', duration);
    };

    window.showError = (message, duration = 7000) => {
        return notificationSystem.show(message, 'error', duration);
    };

    window.showWarning = (message, duration = 6000) => {
        return notificationSystem.show(message, 'warning', duration);
    };

    window.showInfo = (message, duration = 5000) => {
        return notificationSystem.show(message, 'info', duration);
    };
});
