// Sistema de Notificaciones React
const { useState, useEffect } = React;

const NotificationSystem = () => {
    const [notifications, setNotifications] = useState([]);

    // Función para agregar notificación
    const addNotification = (message, type = 'info', duration = 5000) => {
        const id = Date.now();
        const notification = { id, message, type, duration };
        
        setNotifications(prev => [...prev, notification]);
        
        // Auto-remover después del tiempo especificado
        setTimeout(() => {
            removeNotification(id);
        }, duration);
    };

    // Función para remover notificación
    const removeNotification = (id) => {
        setNotifications(prev => prev.filter(notif => notif.id !== id));
    };

    // Escuchar eventos globales para mostrar notificaciones
    useEffect(() => {
        // Función global para mostrar notificaciones desde cualquier parte
        window.showNotification = addNotification;
        
        // Procesar mensajes de Django al cargar la página
        const djangoMessages = document.querySelectorAll('.django-message');
        djangoMessages.forEach(msg => {
            const message = msg.textContent.trim();
            const type = msg.dataset.type || 'info';
            addNotification(message, type);
            msg.remove(); // Remover el mensaje original
        });

        return () => {
            delete window.showNotification;
        };
    }, []);

    // Obtener icono según tipo
    const getIcon = (type) => {
        switch(type) {
            case 'success': return 'fas fa-check-circle';
            case 'error': 
            case 'danger': return 'fas fa-exclamation-triangle';
            case 'warning': return 'fas fa-exclamation-circle';
            case 'info': return 'fas fa-info-circle';
            default: return 'fas fa-bell';
        }
    };

    // Obtener clase de color
    const getColorClass = (type) => {
        switch(type) {
            case 'success': return 'notification-success';
            case 'error':
            case 'danger': return 'notification-error';
            case 'warning': return 'notification-warning';
            case 'info': return 'notification-info';
            default: return 'notification-info';
        }
    };

    return (
        <div className="notification-container">
            {notifications.map(notification => (
                <div 
                    key={notification.id}
                    className={`notification ${getColorClass(notification.type)}`}
                >
                    <div className="notification-content">
                        <i className={`${getIcon(notification.type)} notification-icon`}></i>
                        <span className="notification-message">{notification.message}</span>
                        <button 
                            className="notification-close"
                            onClick={() => removeNotification(notification.id)}
                        >
                            <i className="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
};

// Estilos CSS para las notificaciones
const notificationStyles = `
.notification-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    max-width: 400px;
}

.notification {
    margin-bottom: 10px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    animation: slideIn 0.3s ease-out;
    backdrop-filter: blur(10px);
}

.notification-content {
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: white;
}

.notification-icon {
    font-size: 18px;
    flex-shrink: 0;
}

.notification-message {
    flex-grow: 1;
    font-weight: 500;
}

.notification-close {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    opacity: 0.8;
    transition: opacity 0.2s;
}

.notification-close:hover {
    opacity: 1;
    background: rgba(255,255,255,0.1);
}

.notification-success {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
}

.notification-error {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.notification-warning {
    background: linear-gradient(135deg, #f39c12, #e67e22);
}

.notification-info {
    background: linear-gradient(135deg, #184da1, #2D64BB);
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@media (max-width: 768px) {
    .notification-container {
        left: 20px;
        right: 20px;
        max-width: none;
    }
}
`;

// Inyectar estilos
if (!document.getElementById('notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = notificationStyles;
    document.head.appendChild(style);
}