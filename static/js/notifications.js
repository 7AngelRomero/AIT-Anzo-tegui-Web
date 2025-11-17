// Funciones auxiliares para el sistema de notificaciones

// Función para mostrar notificación desde JavaScript vanilla
function showNotification(message, type = 'info', duration = 5000) {
    if (window.showNotification) {
        window.showNotification(message, type, duration);
    } else {
        // Fallback si React no está cargado
        console.log(`Notification: ${message} (${type})`);
    }
}

// Funciones específicas para cada tipo
function showSuccess(message, duration = 5000) {
    showNotification(message, 'success', duration);
}

function showError(message, duration = 7000) {
    showNotification(message, 'error', duration);
}

function showWarning(message, duration = 6000) {
    showNotification(message, 'warning', duration);
}

function showInfo(message, duration = 5000) {
    showNotification(message, 'info', duration);
}

// Interceptar formularios para mostrar notificaciones de éxito
document.addEventListener('DOMContentLoaded', function() {
    // Interceptar envío de formularios para feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Mostrar notificación de procesamiento
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
                submitBtn.disabled = true;
                
                // Restaurar después de un tiempo (en caso de error)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
});

// Exportar funciones globalmente
window.showSuccess = showSuccess;
window.showError = showError;
window.showWarning = showWarning;
window.showInfo = showInfo;