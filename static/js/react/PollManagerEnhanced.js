// Componente React para mejorar Poll Manager
const { useState, useEffect } = React;

const PollManagerEnhanced = ({ initialPolls, userRole }) => {
    const [polls, setPolls] = useState(initialPolls || []);
    const [filteredPolls, setFilteredPolls] = useState(initialPolls || []);
    const [filters, setFilters] = useState({
        search: '',
        status: '',
        sortBy: 'date'
    });
    const [viewMode, setViewMode] = useState('grid'); // grid o table

    // Filtrar y ordenar encuestas
    useEffect(() => {
        let filtered = polls.filter(poll => {
            const matchesSearch = poll.title.toLowerCase().includes(filters.search.toLowerCase()) ||
                                poll.description.toLowerCase().includes(filters.search.toLowerCase());
            const matchesStatus = !filters.status || poll.status === filters.status;
            return matchesSearch && matchesStatus;
        });

        // Ordenar
        filtered.sort((a, b) => {
            switch(filters.sortBy) {
                case 'title':
                    return a.title.localeCompare(b.title);
                case 'status':
                    return a.status.localeCompare(b.status);
                case 'questions':
                    return b.questions_count - a.questions_count;
                case 'responses':
                    return b.responses_count - a.responses_count;
                case 'date':
                default:
                    return new Date(b.star_date) - new Date(a.star_date);
            }
        });

        setFilteredPolls(filtered);
    }, [polls, filters]);

    // Obtener estadísticas
    const stats = {
        total: polls.length,
        active: polls.filter(p => p.status === 'ACTIVA').length,
        draft: polls.filter(p => p.status === 'BORRADOR').length,
        closed: polls.filter(p => p.status === 'CERRADA').length,
        totalResponses: polls.reduce((sum, p) => sum + (p.responses_count || 0), 0)
    };

    // Componente de estadísticas mejorado
    const StatsCards = () => (
        <div className="row mb-5">
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-primary text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-poll fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-primary px-3 py-2">
                                <i className="fas fa-chart-line"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.total}</h2>
                        <p className="mb-0 fw-semibold">Total Encuestas</p>
                        <small className="opacity-75">Todas las encuestas creadas</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-success text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-check-circle fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-success px-3 py-2">
                                <i className="fas fa-arrow-up"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.active}</h2>
                        <p className="mb-0 fw-semibold">Encuestas Activas</p>
                        <small className="opacity-75">Disponibles para participar</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-warning text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-edit fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-warning px-3 py-2">
                                <i className="fas fa-clock"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.draft}</h2>
                        <p className="mb-0 fw-semibold">Borradores</p>
                        <small className="opacity-75">En proceso de creación</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-info text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-users fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-info px-3 py-2">
                                <i className="fas fa-star"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.totalResponses}</h2>
                        <p className="mb-0 fw-semibold">Total Respuestas</p>
                        <small className="opacity-75">Participaciones recibidas</small>
                    </div>
                </div>
            </div>
        </div>
    );

    // Componente de tarjeta de encuesta para manager mejorado
    const ManagerPollCard = ({ poll }) => {
        const getStatusInfo = (status) => {
            const statusMap = {
                'ACTIVA': { class: 'bg-success', icon: 'fas fa-play-circle', text: 'Activa' },
                'BORRADOR': { class: 'bg-warning', icon: 'fas fa-edit', text: 'Borrador' },
                'CERRADA': { class: 'bg-secondary', icon: 'fas fa-stop-circle', text: 'Cerrada' }
            };
            return statusMap[status] || { class: 'bg-primary', icon: 'fas fa-circle', text: status };
        };

        const statusInfo = getStatusInfo(poll.status);

        return (
            <div className="col-lg-4 col-md-6 mb-4">
                <div className="card h-100 border-0 shadow-lg manager-poll-card">
                    <div className="card-header border-0 bg-light">
                        <div className="d-flex justify-content-between align-items-center">
                            <h6 className="mb-0 fw-bold text-primary">
                                <i className="fas fa-cog me-2"></i>
                                Panel de Gestión
                            </h6>
                            <span className={`badge ${statusInfo.class} px-3 py-2`}>
                                <i className={`${statusInfo.icon} me-1`}></i>
                                {statusInfo.text}
                            </span>
                        </div>
                    </div>
                    
                    <div className="card-body d-flex flex-column p-4">
                        <h5 className="card-title fw-bold text-primary mb-3">{poll.title}</h5>
                        
                        {poll.description && (
                            <p className="card-text text-muted flex-grow-1 mb-4">
                                {poll.description.length > 100 
                                    ? poll.description.substring(0, 100) + '...' 
                                    : poll.description}
                            </p>
                        )}
                        
                        <div className="row mb-4">
                            <div className="col-4">
                                <div className="text-center p-3 bg-primary bg-opacity-10 rounded">
                                    <i className="fas fa-question-circle fa-2x text-primary mb-2"></i>
                                    <h6 className="fw-bold text-primary mb-0">{poll.questions_count}</h6>
                                    <small className="text-muted">Preguntas</small>
                                </div>
                            </div>
                            <div className="col-4">
                                <div className="text-center p-3 bg-success bg-opacity-10 rounded">
                                    <i className="fas fa-users fa-2x text-success mb-2"></i>
                                    <h6 className="fw-bold text-success mb-0">{poll.responses_count || 0}</h6>
                                    <small className="text-muted">Respuestas</small>
                                </div>
                            </div>
                            <div className="col-4">
                                <div className="text-center p-3 bg-info bg-opacity-10 rounded">
                                    <i className="fas fa-calendar-alt fa-2x text-info mb-2"></i>
                                    <h6 className="fw-bold text-info mb-0">
                                        {new Date(poll.star_date).toLocaleDateString('es-ES', {day: '2-digit', month: 'short'})}
                                    </h6>
                                    <small className="text-muted">Creada</small>
                                </div>
                            </div>
                        </div>
                        
                        <div className="d-grid gap-2">
                            <div className="row g-2">
                                <div className="col-6">
                                    <a href={`/polls/${poll.id}/edit/`} className="btn btn-outline-primary w-100">
                                        <i className="fas fa-edit me-2"></i>Editar
                                    </a>
                                </div>
                                <div className="col-6">
                                    <a href={`/polls/${poll.id}/results/`} className="btn btn-info w-100">
                                        <i className="fas fa-chart-bar me-2"></i>Resultados
                                    </a>
                                </div>
                            </div>
                            {userRole === 'Administrador' && (
                                <a href={`/polls/${poll.id}/delete/`} className="btn btn-outline-danger mt-2">
                                    <i className="fas fa-trash me-2"></i>Eliminar Encuesta
                                </a>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="poll-manager-enhanced">
            {/* Estadísticas */}
            <StatsCards />

            {/* Panel de control avanzado */}
            <div className="row mb-5">
                <div className="col-12">
                    <div className="card border-0 shadow-lg control-panel-manager">
                        <div className="card-header bg-gradient-primary text-white border-0">
                            <div className="d-flex justify-content-between align-items-center">
                                <h5 className="mb-0 fw-bold">
                                    <i className="fas fa-filter me-2"></i>
                                    Filtros de Búsqueda
                                </h5>
                                <div className="badge bg-light text-primary px-3 py-2 fs-6">
                                    <i className="fas fa-eye me-1"></i>
                                    {filteredPolls.length} visible{filteredPolls.length !== 1 ? 's' : ''}
                                </div>
                            </div>
                        </div>
                        <div className="card-body p-4">
                            <div className="row g-4">
                                <div className="col-md-5">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-search me-2"></i>Búsqueda Inteligente
                                    </label>
                                    <div className="input-group input-group-lg">
                                        <span className="input-group-text bg-light border-0">
                                            <i className="fas fa-search text-primary"></i>
                                        </span>
                                        <input
                                            type="text"
                                            className="form-control border-0 shadow-sm"
                                            placeholder="Buscar por título, descripción o contenido..."
                                            value={filters.search}
                                            onChange={(e) => setFilters({...filters, search: e.target.value})}
                                        />
                                    </div>
                                </div>
                                <div className="col-md-3">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-filter me-2"></i>Filtrar por Estado
                                    </label>
                                    <select
                                        className="form-select form-select-lg border-0 shadow-sm"
                                        value={filters.status}
                                        onChange={(e) => setFilters({...filters, status: e.target.value})}
                                    >
                                        <option value="">📊 Todos los Estados</option>
                                        <option value="ACTIVA">✅ Encuestas Activas</option>
                                        <option value="BORRADOR">✏️ Borradores</option>
                                        <option value="CERRADA">🚫 Cerradas</option>
                                    </select>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-sort-amount-down me-2"></i>Ordenar Resultados
                                    </label>
                                    <select
                                        className="form-select form-select-lg border-0 shadow-sm"
                                        value={filters.sortBy}
                                        onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
                                    >
                                        <option value="date">📅 Más Recientes</option>
                                        <option value="title">🔤 Título A-Z</option>
                                        <option value="status">🏷️ Por Estado</option>
                                        <option value="questions">❓ Más Preguntas</option>
                                        <option value="responses">👥 Más Respuestas</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Lista de encuestas */}
            <div className="row">
                {filteredPolls.length > 0 ? (
                    filteredPolls.map(poll => (
                        <ManagerPollCard key={poll.id} poll={poll} />
                    ))
                ) : (
                    <div className="col-12">
                        <div className="card border-0 shadow-lg">
                            <div className="card-body text-center py-5">
                                <div className="mb-4">
                                    <i className="fas fa-search-minus fa-5x text-primary opacity-50"></i>
                                </div>
                                <h3 className="fw-bold text-primary mb-3">No se encontraron encuestas</h3>
                                <p className="text-muted fs-5 mb-4">
                                    {filters.search || filters.status 
                                        ? 'Intenta ajustar los filtros de búsqueda o crear una nueva encuesta' 
                                        : 'Aún no hay encuestas creadas. ¡Comienza creando tu primera encuesta!'}
                                </p>
                                <div className="d-flex gap-3 justify-content-center">
                                    {(filters.search || filters.status) && (
                                        <button 
                                            className="btn btn-outline-primary btn-lg"
                                            onClick={() => setFilters({search: '', status: '', sortBy: 'date'})}
                                        >
                                            <i className="fas fa-refresh me-2"></i>Limpiar Filtros
                                        </button>
                                    )}
                                    <a href="/polls/create/" className="btn btn-primary btn-lg">
                                        <i className="fas fa-plus me-2"></i>Crear Nueva Encuesta
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

// Estilos profesionales para manager
const managerStyles = `
.stats-card {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-radius: 15px !important;
    overflow: hidden;
}

.stats-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
}

.manager-poll-card {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-radius: 15px !important;
    overflow: hidden;
}

.manager-poll-card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 15px 35px rgba(24, 77, 161, 0.2) !important;
}

.control-panel-manager {
    border-radius: 15px !important;
    overflow: hidden;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #184da1 0%, #2D64BB 50%, #3498db 100%) !important;
}

.bg-gradient-success {
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
}

.bg-gradient-warning {
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%) !important;
}

.bg-gradient-info {
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
}

.text-primary {
    color: #184da1 !important;
}

.btn-primary {
    background: linear-gradient(135deg, #184da1 0%, #2D64BB 100%);
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #2D64BB 0%, #184da1 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(24, 77, 161, 0.3);
}

.form-control:focus, .form-select:focus {
    border-color: #184da1 !important;
    box-shadow: 0 0 0 0.25rem rgba(24, 77, 161, 0.15) !important;
    transform: translateY(-2px);
}

.badge {
    border-radius: 20px !important;
    font-weight: 600;
}

.input-group-text {
    border-radius: 10px 0 0 10px !important;
}

.form-control, .form-select {
    border-radius: 0 10px 10px 0 !important;
}
`;

// Inyectar estilos
if (!document.getElementById('manager-styles')) {
    const style = document.createElement('style');
    style.id = 'manager-styles';
    style.textContent = managerStyles;
    document.head.appendChild(style);
}