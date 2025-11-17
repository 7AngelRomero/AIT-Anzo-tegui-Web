// Componente React para Poll Detail mejorado
const { useState, useEffect } = React;

const PollDetailEnhanced = ({ pollData, csrfToken }) => {
    const [responses, setResponses] = useState({});
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [progress, setProgress] = useState(0);

    // Calcular progreso
    useEffect(() => {
        const totalQuestions = pollData.questions.length;
        const answeredQuestions = Object.keys(responses).length;
        setProgress((answeredQuestions / totalQuestions) * 100);
    }, [responses, pollData.questions.length]);

    // Manejar respuestas
    const handleResponse = (questionId, value) => {
        setResponses(prev => ({
            ...prev,
            [questionId]: value
        }));
    };

    // Enviar formulario
    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Crear FormData
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        Object.entries(responses).forEach(([questionId, value]) => {
            formData.append(`question_${questionId}`, value);
        });

        try {
            const response = await fetch(`/polls/${pollData.id}/submit/`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                window.showSuccess('¡Gracias por participar en la encuesta!');
                setTimeout(() => {
                    window.location.href = '/polls/';
                }, 2000);
            } else {
                window.showError('Error al enviar las respuestas. Intenta nuevamente.');
            }
        } catch (error) {
            window.showError('Error de conexión. Verifica tu internet.');
        } finally {
            setIsSubmitting(false);
        }
    };

    // Componente de pregunta
    const QuestionCard = ({ question, index }) => {
        const isActive = index === currentQuestion;
        
        return (
            <div className={`question-card ${isActive ? 'active' : ''}`} style={{display: isActive ? 'block' : 'none'}}>
                <div className="card border-0 shadow-lg mb-4">
                    <div className="card-header bg-gradient-primary text-white border-0">
                        <div className="d-flex justify-content-between align-items-center">
                            <h5 className="mb-0 fw-bold">
                                <i className="fas fa-question-circle me-2"></i>
                                Pregunta {index + 1} de {pollData.questions.length}
                            </h5>
                            {question.is_obligatory && (
                                <span className="badge bg-warning text-dark">
                                    <i className="fas fa-asterisk me-1"></i>Obligatoria
                                </span>
                            )}
                        </div>
                    </div>
                    
                    <div className="card-body p-4">
                        <h4 className="question-text mb-4">{question.question_text}</h4>
                        
                        {question.question_type === 'SELECCION_MULTIPLE' && (
                            <div className="options-container">
                                {question.options.map((option, optIndex) => (
                                    <div key={option.id} className="option-item mb-3">
                                        <input
                                            type="radio"
                                            id={`option_${option.id}`}
                                            name={`question_${question.id}`}
                                            value={option.id}
                                            onChange={(e) => handleResponse(question.id, e.target.value)}
                                            className="option-radio"
                                        />
                                        <label htmlFor={`option_${option.id}`} className="option-label">
                                            <div className="option-content">
                                                <div className="option-indicator">
                                                    <span className="option-letter">{String.fromCharCode(65 + optIndex)}</span>
                                                </div>
                                                <span className="option-text">{option.options_text}</span>
                                            </div>
                                        </label>
                                    </div>
                                ))}
                            </div>
                        )}
                        
                        {question.question_type === 'TEXTO_LIBRE' && (
                            <div className="text-response-container">
                                <textarea
                                    className="form-control form-control-lg"
                                    rows="5"
                                    placeholder="Escribe tu respuesta aquí..."
                                    onChange={(e) => handleResponse(question.id, e.target.value)}
                                    style={{borderRadius: '15px', border: '2px solid #e9ecef'}}
                                />
                            </div>
                        )}
                        
                        {question.question_type === 'ESCALA_NUMERICA' && (
                            <div className="scale-container">
                                <div className="scale-labels mb-3">
                                    <span className="text-muted">1 (Muy malo)</span>
                                    <span className="text-muted">5 (Excelente)</span>
                                </div>
                                <div className="scale-options">
                                    {question.options.map((option) => (
                                        <div key={option.id} className="scale-option">
                                            <input
                                                type="radio"
                                                id={`scale_${option.id}`}
                                                name={`question_${question.id}`}
                                                value={option.id}
                                                onChange={(e) => handleResponse(question.id, e.target.value)}
                                                className="scale-radio"
                                            />
                                            <label htmlFor={`scale_${option.id}`} className="scale-label">
                                                {option.options_text}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="poll-detail-enhanced">
            {/* Header mejorado */}
            <div className="poll-header mb-5">
                <div className="card border-0 shadow-lg">
                    <div className="card-header bg-gradient-primary text-white border-0">
                        <div className="row align-items-center">
                            <div className="col-md-8">
                                <h1 className="display-6 fw-bold mb-2 text-white">{pollData.title}</h1>
                                {pollData.description && (
                                    <p className="lead mb-0 opacity-90">{pollData.description}</p>
                                )}
                            </div>
                            <div className="col-md-4 text-md-end">
                                <div className="poll-stats">
                                    <div className="stat-item mb-2">
                                        <i className="fas fa-user-tie me-2"></i>
                                        <span>Creado por: <strong>{pollData.created_by}</strong></span>
                                    </div>
                                    <div className="stat-item mb-2">
                                        <i className="fas fa-calendar-alt me-2"></i>
                                        <span>{new Date(pollData.star_date).toLocaleDateString('es-ES')}</span>
                                    </div>
                                    <div className="stat-item">
                                        <i className="fas fa-question-circle me-2"></i>
                                        <span>{pollData.questions.length} pregunta{pollData.questions.length !== 1 ? 's' : ''}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {/* Barra de progreso */}
                    <div className="progress-container p-3">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                            <span className="text-muted">Progreso de la encuesta</span>
                            <span className="fw-bold text-primary">{Math.round(progress)}%</span>
                        </div>
                        <div className="progress" style={{height: '8px', borderRadius: '10px'}}>
                            <div 
                                className="progress-bar bg-gradient-success" 
                                style={{width: `${progress}%`, transition: 'width 0.3s ease'}}
                            ></div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Formulario */}
            <form onSubmit={handleSubmit}>
                {/* Preguntas */}
                {pollData.questions.map((question, index) => (
                    <QuestionCard key={question.id} question={question} index={index} />
                ))}

                {/* Navegación */}
                <div className="navigation-controls mb-4">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-center">
                                <button
                                    type="button"
                                    className="btn btn-outline-primary"
                                    onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                                    disabled={currentQuestion === 0}
                                >
                                    <i className="fas fa-chevron-left me-2"></i>Anterior
                                </button>
                                
                                <div className="question-indicators">
                                    {pollData.questions.map((_, index) => (
                                        <button
                                            key={index}
                                            type="button"
                                            className={`question-dot ${index === currentQuestion ? 'active' : ''} ${responses[pollData.questions[index].id] ? 'answered' : ''}`}
                                            onClick={() => setCurrentQuestion(index)}
                                        >
                                            {index + 1}
                                        </button>
                                    ))}
                                </div>
                                
                                {currentQuestion < pollData.questions.length - 1 ? (
                                    <button
                                        type="button"
                                        className="btn btn-primary"
                                        onClick={() => setCurrentQuestion(currentQuestion + 1)}
                                    >
                                        Siguiente<i className="fas fa-chevron-right ms-2"></i>
                                    </button>
                                ) : (
                                    <button
                                        type="submit"
                                        className="btn btn-success btn-lg"
                                        disabled={isSubmitting}
                                    >
                                        {isSubmitting ? (
                                            <>
                                                <i className="fas fa-spinner fa-spin me-2"></i>Enviando...
                                            </>
                                        ) : (
                                            <>
                                                <i className="fas fa-paper-plane me-2"></i>Enviar Respuestas
                                            </>
                                        )}
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </form>

            {/* Botón volver */}
            <div className="text-center">
                <a href="/polls/" className="btn btn-outline-secondary btn-lg">
                    <i className="fas fa-arrow-left me-2"></i>Volver a Encuestas
                </a>
            </div>
        </div>
    );
};

// Estilos mejorados
const pollDetailStyles = `
.poll-detail-enhanced {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #184da1 0%, #2D64BB 50%, #3498db 100%) !important;
}

.bg-gradient-success {
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
}

.question-card {
    animation: slideIn 0.3s ease-out;
}

.option-item {
    position: relative;
}

.option-radio {
    position: absolute;
    opacity: 0;
    cursor: pointer;
}

.option-label {
    display: block;
    cursor: pointer;
    padding: 0;
    margin: 0;
}

.option-content {
    display: flex;
    align-items: center;
    padding: 15px 20px;
    border: 2px solid #e9ecef;
    border-radius: 15px;
    transition: all 0.3s ease;
    background: white;
}

.option-content:hover {
    border-color: #184da1;
    background: rgba(24, 77, 161, 0.05);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(24, 77, 161, 0.1);
}

.option-radio:checked + .option-label .option-content {
    border-color: #184da1;
    background: rgba(24, 77, 161, 0.1);
    box-shadow: 0 0 0 3px rgba(24, 77, 161, 0.2);
}

.option-indicator {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    font-weight: bold;
    color: #184da1;
    transition: all 0.3s ease;
}

.option-radio:checked + .option-label .option-indicator {
    background: #184da1;
    color: white;
}

.option-text {
    font-size: 16px;
    font-weight: 500;
}

.scale-container {
    text-align: center;
}

.scale-labels {
    display: flex;
    justify-content: space-between;
}

.scale-options {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

.scale-option {
    position: relative;
}

.scale-radio {
    position: absolute;
    opacity: 0;
}

.scale-label {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border: 3px solid #e9ecef;
    border-radius: 50%;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
}

.scale-label:hover {
    border-color: #184da1;
    background: rgba(24, 77, 161, 0.1);
    transform: scale(1.1);
}

.scale-radio:checked + .scale-label {
    border-color: #184da1;
    background: #184da1;
    color: white;
    transform: scale(1.1);
}

.question-indicators {
    display: flex;
    gap: 10px;
}

.question-dot {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid #e9ecef;
    background: white;
    color: #6c757d;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.question-dot:hover {
    border-color: #184da1;
    color: #184da1;
}

.question-dot.active {
    border-color: #184da1;
    background: #184da1;
    color: white;
}

.question-dot.answered {
    border-color: #27ae60;
    background: #27ae60;
    color: white;
}

.question-dot.answered.active {
    border-color: #184da1;
    background: #184da1;
}

.poll-stats {
    font-size: 14px;
}

.stat-item {
    opacity: 0.9;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@media (max-width: 768px) {
    .poll-detail-enhanced {
        padding: 1rem 0.5rem;
    }
    
    .scale-options {
        gap: 10px;
    }
    
    .scale-label {
        width: 50px;
        height: 50px;
        font-size: 16px;
    }
    
    .question-indicators {
        gap: 5px;
    }
    
    .question-dot {
        width: 35px;
        height: 35px;
        font-size: 14px;
    }
}
`;

// Inyectar estilos
if (!document.getElementById('poll-detail-styles')) {
    const style = document.createElement('style');
    style.id = 'poll-detail-styles';
    style.textContent = pollDetailStyles;
    document.head.appendChild(style);
}