// Componente React para mejorar Poll List
const { useState, useEffect } = React;

const PollListEnhanced = ({ initialPolls }) => {
    const [polls, setPolls] = useState(initialPolls || []);
    const [filteredPolls, setFilteredPolls] = useState(initialPolls || []);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState('date');
    const [loading, setLoading] = useState(false);

    // Filtrar y ordenar encuestas
    useEffect(() => {
        let filtered = polls.filter(poll => 
            poll.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            poll.description.toLowerCase().includes(searchTerm.toLowerCase())
        );

        // Ordenar
        filtered.sort((a, b) => {
            switch(sortBy) {
                case 'title':
                    return a.title.localeCompare(b.title);
                case 'questions':
                    return b.questions_count - a.questions_count;
                case 'date':
                default:
                    return new Date(b.star_date) - new Date(a.star_date);
            }
        });

        setFilteredPolls(filtered);
    }, [polls, searchTerm, sortBy]);

    // Componente de tarjeta mejorada
    const EnhancedPollCard = ({ poll }) => (
        <div className="col-lg-4 col-md-6 mb-4">
            <div className="card h-100 border-0 shadow-lg poll-card-enhanced">
                <div className="card-header border-0 bg-gradient-primary text-white">
                    <div className="d-flex justify-content-between align-items-center">
                        <h6 className="mb-0 fw-bold">
                            <i className="fas fa-poll me-2"></i>
                            Encuesta Pública
                        </h6>
                        <span className="badge bg-light text-primary px-3 py-2">
                            <i className="fas fa-eye me-1"></i>Activa
                        </span>
                    </div>
                </div>
                
                <div className="card-body d-flex flex-column p-4">
                    <h5 className="card-title fw-bold text-primary mb-3">{poll.title}</h5>
                    
                    {poll.description && (
                        <p className="card-text text-muted flex-grow-1 mb-4">
                            {poll.description.length > 120 
                                ? poll.description.substring(0, 120) + '...' 
                                : poll.description}
                        </p>
                    )}
                    
                    <div className="row mb-4">
                        <div className="col-6">
                            <div className="text-center p-3 bg-light rounded">
                                <i className="fas fa-question-circle fa-2x text-primary mb-2"></i>
                                <h5 className="fw-bold text-primary mb-0">{poll.questions_count}</h5>
                                <small className="text-muted">Preguntas</small>
                            </div>
                        </div>
                        <div className="col-6">
                            <div className="text-center p-3 bg-light rounded">
                                <i className="fas fa-calendar-alt fa-2x text-info mb-2"></i>
                                <h6 className="fw-bold text-info mb-0">
                                    {new Date(poll.star_date).toLocaleDateString('es-ES', {day: '2-digit', month: 'short'})}
                                </h6>
                                <small className="text-muted">Creada</small>
                            </div>
                        </div>
                    </div>
                    
                    <a 
                        href={`/polls/${poll.id}/`} 
                        className="btn btn-gradient-primary btn-lg w-100 participate-btn"
                    >
                        <i className="fas fa-rocket me-2"></i>Participar Ahora
                    </a>
                </div>
            </div>
        </div>
    );

    return (
        <div className="poll-list-enhanced">
            {/* Panel de control moderno */}
            <div className="row mb-5">
                <div className="col-12">
                    <div className="card border-0 shadow-lg control-panel">
                        <div className="card-header bg-gradient-primary text-white border-0">
                            <div className="d-flex justify-content-between align-items-center">
                                <h5 className="mb-0 fw-bold">
                                    <i className="fas fa-filter me-2"></i>
                                    Panel de Control
                                </h5>
                                <div className="badge bg-light text-primary px-3 py-2 fs-6">
                                    {filteredPolls.length} encuesta{filteredPolls.length !== 1 ? 's' : ''} encontrada{filteredPolls.length !== 1 ? 's' : ''}
                                </div>
                            </div>
                        </div>
                        <div className="card-body p-4">
                            <div className="row g-4">
                                <div className="col-md-8">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-search me-2"></i>Buscar Encuestas
                                    </label>
                                    <div className="input-group input-group-lg">
                                        <span className="input-group-text bg-light border-0">
                                            <i className="fas fa-search text-primary"></i>
                                        </span>
                                        <input
                                            type="text"
                                            className="form-control border-0 shadow-sm"
                                            placeholder="Busca por título, descripción o contenido..."
                                            value={searchTerm}
                                            onChange={(e) => setSearchTerm(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-sort-amount-down me-2"></i>Ordenar Resultados
                                    </label>
                                    <select
                                        className="form-select form-select-lg border-0 shadow-sm"
                                        value={sortBy}
                                        onChange={(e) => setSortBy(e.target.value)}
                                    >
                                        <option value="date">📅 Más Recientes</option>
                                        <option value="title">🔤 Título A-Z</option>
                                        <option value="questions">❓ Más Preguntas</option>
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
                        <EnhancedPollCard key={poll.id} poll={poll} />
                    ))
                ) : (
                    <div className="col-12">
                        <div className="card border-0 shadow-lg">
                            <div className="card-body text-center py-5">
                                <div className="mb-4">
                                    <i className="fas fa-search fa-5x text-primary opacity-50"></i>
                                </div>
                                <h3 className="fw-bold text-primary mb-3">No se encontraron encuestas</h3>
                                <p className="text-muted fs-5 mb-4">
                                    {searchTerm 
                                        ? 'Intenta con otros términos de búsqueda o ajusta los filtros' 
                                        : 'No hay encuestas disponibles en este momento. ¡Vuelve pronto!'}
                                </p>
                                {searchTerm && (
                                    <button 
                                        className="btn btn-outline-primary btn-lg"
                                        onClick={() => setSearchTerm('')}
                                    >
                                        <i className="fas fa-refresh me-2"></i>Limpiar Búsqueda
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

// Estilos mejorados profesionales
const pollListStyles = `
.poll-card-enhanced {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
    border-radius: 15px !important;
    overflow: hidden;
}

.poll-card-enhanced:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 20px 40px rgba(24, 77, 161, 0.2) !important;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #184da1 0%, #2D64BB 50%, #3498db 100%);
}

.btn-gradient-primary {
    background: linear-gradient(135deg, #184da1 0%, #2D64BB 100%);
    border: none;
    transition: all 0.3s ease;
    border-radius: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: white !important;
}

.btn-gradient-primary:hover {
    background: linear-gradient(135deg, #2D64BB 0%, #184da1 100%);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(24, 77, 161, 0.4);
}

.control-panel {
    border-radius: 15px !important;
    overflow: hidden;
}

.text-primary {
    color: #184da1 !important;
}

.form-control:focus, .form-select:focus {
    border-color: #184da1 !important;
    box-shadow: 0 0 0 0.25rem rgba(24, 77, 161, 0.15) !important;
    transform: translateY(-2px);
}

.input-group-text {
    border-radius: 10px 0 0 10px !important;
}

.form-control, .form-select {
    border-radius: 0 10px 10px 0 !important;
}

.badge {
    border-radius: 20px !important;
    font-weight: 600;
}
`;

// Inyectar estilos
if (!document.getElementById('poll-list-styles')) {
    const style = document.createElement('style');
    style.id = 'poll-list-styles';
    style.textContent = pollListStyles;
    document.head.appendChild(style);
}