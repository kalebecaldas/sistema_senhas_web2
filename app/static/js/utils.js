/**
 * Utilitários JavaScript para o Sistema de Senhas
 */

// Configurações globais
window.SISTEMA_CONFIG = {
    TIMEOUT_PING: 2000,
    TIMEOUT_RECONEXAO: 3000,
    INTERVALO_ATUALIZACAO: 3000,
    DURACAO_TOAST: 4000
};

/**
 * Sistema de notificações toast
 */
class ToastManager {
    constructor() {
        this.container = document.getElementById('notification-container');
        if (!this.container) {
            console.warn('Container de notificações não encontrado');
        }
    }

    show(message, type = 'info', duration = SISTEMA_CONFIG.DURACAO_TOAST) {
        if (!this.container) return;

        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show`;
        toast.role = 'alert';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        this.container.appendChild(toast);

        // Auto-dismiss
        setTimeout(() => {
            toast.classList.remove('show');
            toast.addEventListener('transitionend', () => toast.remove());
            toast.classList.add('hide');
        }, duration);

        return toast;
    }

    success(message) { return this.show(message, 'success'); }
    error(message) { return this.show(message, 'danger'); }
    warning(message) { return this.show(message, 'warning'); }
    info(message) { return this.show(message, 'info'); }
}

/**
 * Gerenciador de conexão
 */
class ConnectionManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.setupEventListeners();
    }

    setupEventListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.onReconnect();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            console.warn("📴 Dispositivo offline.");
        });
    }

    async ping() {
        try {
            const response = await fetch('/ping', { 
                method: 'GET',
                timeout: SISTEMA_CONFIG.TIMEOUT_PING 
            });
            return response.ok;
        } catch (error) {
            console.warn("⚠️ Ping falhou:", error);
            return false;
        }
    }

    async testConnection() {
        const isConnected = await this.ping();
        if (!isConnected && this.isOnline) {
            console.warn("⚠️ Servidor inacessível. Aguardando reconexão...");
            toastManager.warning("Servidor inacessível. Aguardando reconexão...");
        }
        return isConnected;
    }

    onReconnect() {
        console.log("📶 Dispositivo online.");
        this.reconnectAttempts = 0;
        toastManager.success("Conexão restaurada!");
    }

    async waitForConnection() {
        return new Promise((resolve) => {
            const checkConnection = async () => {
                if (await this.ping()) {
                    resolve(true);
                } else {
                    setTimeout(checkConnection, SISTEMA_CONFIG.TIMEOUT_RECONEXAO);
                }
            };
            checkConnection();
        });
    }
}

/**
 * Utilitários de formatação
 */
class Formatters {
    static formatSenha(sigla, numero) {
        if (numero === 0) return sigla;
        return `${sigla}${String(numero).padStart(4, '0')}`;
    }

    static formatTime(date) {
        return new Date(date).toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    static formatDateTime(date) {
        return new Date(date).toLocaleString('pt-BR');
    }

    static formatGuiche(guiche) {
        return guiche ? `Guichê ${guiche}` : 'Guichê não informado';
    }
}

/**
 * Utilitários de validação
 */
class Validators {
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    static isValidGuiche(guiche) {
        return guiche && guiche.toString().trim() !== '';
    }

    static isValidSenha(senha) {
        return senha && senha.toString().trim() !== '';
    }
}

/**
 * Gerenciador de sessão
 */
class SessionManager {
    static setGuiche(guiche) {
        if (guiche) {
            sessionStorage.setItem('guiche', guiche.toString().trim());
        }
    }

    static getGuiche() {
        return sessionStorage.getItem('guiche') || '';
    }

    static setRechamadaInfo(info) {
        if (info) {
            sessionStorage.setItem('rechamada_info', JSON.stringify(info));
        }
    }

    static getRechamadaInfo() {
        const info = sessionStorage.getItem('rechamada_info');
        return info ? JSON.parse(info) : null;
    }

    static clearRechamadaInfo() {
        sessionStorage.removeItem('rechamada_info');
    }
}

/**
 * Utilitários de API
 */
class ApiUtils {
    static async fetchWithTimeout(url, options = {}, timeout = 10000) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    static async postJson(url, data) {
        const response = await this.fetchWithTimeout(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return response.json();
    }

    static async getJson(url) {
        const response = await this.fetchWithTimeout(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return response.json();
    }
}

/**
 * Gerenciador de áudio
 */
class AudioManager {
    constructor() {
        this.beepAudio = null;
        this.initBeepAudio();
    }

    initBeepAudio() {
        const beepElement = document.getElementById('beep-som');
        if (beepElement) {
            this.beepAudio = beepElement;
        }
    }

    playBeep() {
        if (this.beepAudio) {
            this.beepAudio.play().catch(err => {
                console.warn('Erro ao tocar beep:', err);
            });
        }
    }

    async playTTS(texto) {
        try {
            const response = await fetch(`/tts_audio?texto=${encodeURIComponent(texto)}`);
            if (!response.ok) {
                console.error('Erro TTS:', response.status, response.statusText);
                return;
            }
            
            const blob = await response.blob();
            const audio = new Audio(URL.createObjectURL(blob));
            await audio.play();
        } catch (error) {
            console.error('Erro TTS:', error);
        }
    }
}

// Instâncias globais
const toastManager = new ToastManager();
const connectionManager = new ConnectionManager();
const audioManager = new AudioManager();

// Função global para compatibilidade
window.flashToast = (message, type) => toastManager.show(message, type);

// Exportar para uso em outros módulos
window.SistemaUtils = {
    ToastManager,
    ConnectionManager,
    Formatters,
    Validators,
    SessionManager,
    ApiUtils,
    AudioManager,
    toastManager,
    connectionManager,
    audioManager,
    toast: {
        show: function(message, type = 'success', duration = 5000) {
            const toastContainer = document.querySelector('.toast-container');
            if (!toastContainer) {
                console.warn('Toast container não encontrado');
                return;
            }

            const toastId = 'toast-' + Date.now();
            const icon = type === 'success' ? 'fa-check-circle' : 
                         type === 'error' ? 'fa-exclamation-circle' : 
                         type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';

            const toastHtml = `
                <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
                    <div class="d-flex">
                        <div class="toast-body">
                            <i class="fas ${icon} me-2"></i>
                            ${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                </div>
            `;

            toastContainer.insertAdjacentHTML('beforeend', toastHtml);
            const toastElement = document.getElementById(toastId);
            const toast = new bootstrap.Toast(toastElement, { delay: duration });
            toast.show();

            // Auto remove after animation
            toastElement.addEventListener('hidden.bs.toast', () => {
                toastElement.remove();
            });
        },

        success: function(message, duration) {
            this.show(message, 'success', duration);
        },

        error: function(message, duration) {
            this.show(message, 'danger', duration);
        },

        warning: function(message, duration) {
            this.show(message, 'warning', duration);
        },

        info: function(message, duration) {
            this.show(message, 'info', duration);
        }
    },
    loading: {
        set: function(button, text = 'Carregando...') {
            if (!button) return;
            
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
            button.disabled = true;
        },

        reset: function(button) {
            if (!button || !button.dataset.originalText) return;
            
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
        },

        autoReset: function(button, timeout = 5000) {
            setTimeout(() => {
                this.reset(button);
            }, timeout);
        }
    },
    validation: {
        showError: function(input, message) {
            input.classList.add('is-invalid');
            let feedback = input.parentNode.querySelector('.invalid-feedback');
            
            if (!feedback) {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                input.parentNode.appendChild(feedback);
            }
            
            feedback.textContent = message;
        },

        clearError: function(input) {
            input.classList.remove('is-invalid');
            const feedback = input.parentNode.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.textContent = '';
            }
        },

        validateEmail: function(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        },

        validatePassword: function(password, minLength = 6) {
            return password && password.length >= minLength;
        }
    },
    animation: {
        fadeIn: function(element, duration = 300) {
            element.style.opacity = '0';
            element.style.display = 'block';
            
            let start = null;
            const animate = (timestamp) => {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                const opacity = Math.min(progress / duration, 1);
                
                element.style.opacity = opacity;
                
                if (progress < duration) {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        },

        fadeOut: function(element, duration = 300, callback) {
            let start = null;
            const animate = (timestamp) => {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                const opacity = Math.max(1 - (progress / duration), 0);
                
                element.style.opacity = opacity;
                
                if (progress < duration) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.display = 'none';
                    if (callback) callback();
                }
            };
            
            requestAnimationFrame(animate);
        },

        slideDown: function(element, duration = 300) {
            element.style.height = '0';
            element.style.overflow = 'hidden';
            element.style.display = 'block';
            
            const targetHeight = element.scrollHeight;
            let start = null;
            
            const animate = (timestamp) => {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                const height = Math.min((progress / duration) * targetHeight, targetHeight);
                
                element.style.height = height + 'px';
                
                if (progress < duration) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.height = 'auto';
                    element.style.overflow = 'visible';
                }
            };
            
            requestAnimationFrame(animate);
        }
    },
    datetime: {
        formatTime: function(date) {
            return date.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        },

        formatDate: function(date) {
            return date.toLocaleDateString('pt-BR');
        },

        timeAgo: function(date) {
            const now = new Date();
            const diff = now - date;
            const minutes = Math.floor(diff / 60000);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);

            if (days > 0) return `${days} dia${days > 1 ? 's' : ''}`;
            if (hours > 0) return `${hours} hora${hours > 1 ? 's' : ''}`;
            if (minutes > 0) return `${minutes} minuto${minutes > 1 ? 's' : ''}`;
            return 'Agora mesmo';
        }
    },
    dom: {
        createElement: function(tag, className, innerHTML) {
            const element = document.createElement(tag);
            if (className) element.className = className;
            if (innerHTML) element.innerHTML = innerHTML;
            return element;
        },

        addClass: function(element, className) {
            if (element && element.classList) {
                element.classList.add(className);
            }
        },

        removeClass: function(element, className) {
            if (element && element.classList) {
                element.classList.remove(className);
            }
        },

        toggleClass: function(element, className) {
            if (element && element.classList) {
                element.classList.toggle(className);
            }
        },

        // Busca em tempo real
        liveSearch: function(input, items, filterFunction) {
            input.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                
                items.forEach(item => {
                    const matches = filterFunction(item, searchTerm);
                    item.style.display = matches ? '' : 'none';
                });
            });
        }
    },
    api: {
        request: async function(url, options = {}) {
            try {
                const response = await fetch(url, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error('API request failed:', error);
                throw error;
            }
        },

        get: function(url) {
            return this.request(url);
        },

        post: function(url, data) {
            return this.request(url, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        put: function(url, data) {
            return this.request(url, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        delete: function(url) {
            return this.request(url, {
                method: 'DELETE'
            });
        }
    },
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (error) {
                console.error('Error saving to localStorage:', error);
            }
        },

        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (error) {
                console.error('Error reading from localStorage:', error);
                return defaultValue;
            }
        },

        remove: function(key) {
            try {
                localStorage.removeItem(key);
            } catch (error) {
                console.error('Error removing from localStorage:', error);
            }
        },

        clear: function() {
            try {
                localStorage.clear();
            } catch (error) {
                console.error('Error clearing localStorage:', error);
            }
        }
    },
    init: {
        tooltips: function() {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        },

        popovers: function() {
            const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
            popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        },

        formValidation: function() {
            const forms = document.querySelectorAll('.needs-validation');
            forms.forEach(form => {
                form.addEventListener('submit', function(event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                });
            });
        },

        autoHideAlerts: function() {
            const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
            alerts.forEach(alert => {
                setTimeout(() => {
                    SistemaUtils.animation.fadeOut(alert, 500, () => alert.remove());
                }, 5000);
            });
        }
    }
};

// Auto-inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    SistemaUtils.init.tooltips();
    SistemaUtils.init.popovers();
    SistemaUtils.init.formValidation();
    SistemaUtils.init.autoHideAlerts();
});

// Export para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SistemaUtils;
} 