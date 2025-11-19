// Componente React para gestión de usuarios mejorada - Versión corregida URLs
const { useState, useEffect } = React;

const UserManagementEnhanced = ({ initialUsers }) => {
    const [users, setUsers] = useState(initialUsers || []);
    const [filteredUsers, setFilteredUsers] = useState(initialUsers || []);
    const [filters, setFilters] = useState({
        search: '',
        role: '',
        sortBy: 'username'
    });

    // Filtrar y ordenar usuarios
    useEffect(() => {
        let filtered = users.filter(user => {
            const matchesSearch = user.username.toLowerCase().includes(filters.search.toLowerCase()) ||
                                user.first_name.toLowerCase().includes(filters.search.toLowerCase()) ||
                                user.last_name.toLowerCase().includes(filters.search.toLowerCase()) ||
                                user.email.toLowerCase().includes(filters.search.toLowerCase());
            const matchesRole = !filters.role || (user.rol && user.rol.name === filters.role);
            return matchesSearch && matchesRole;
        });

        // Ordenar
        filtered.sort((a, b) => {
            switch(filters.sortBy) {
                case 'name':
                    return `${a.first_name} ${a.last_name}`.localeCompare(`${b.first_name} ${b.last_name}`);
                case 'email':
                    return a.email.localeCompare(b.email);
                case 'role':
                    const roleA = a.rol ? a.rol.name : '';
                    const roleB = b.rol ? b.rol.name : '';
                    return roleA.localeCompare(roleB);
                case 'username':
                default:
                    return a.username.localeCompare(b.username);
            }
        });

        setFilteredUsers(filtered);
    }, [users, filters]);

    // Obtener estadísticas de usuarios
    const stats = {
        total: users.length,
        admins: users.filter(u => u.rol && u.rol.name === 'Administrador').length,
        workers: users.filter(u => u.rol && u.rol.name === 'Trabajador').length,
        users: users.filter(u => u.rol && u.rol.name === 'Usuario').length
    };

    // Componente de estadísticas
    const UserStatsCards = () => (
        <div className="row mb-5">
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-primary text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-users fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-primary px-3 py-2">
                                <i className="fas fa-chart-line"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.total}</h2>
                        <p className="mb-0 fw-semibold">Total Usuarios</p>
                        <small className="opacity-75">Usuarios registrados</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-danger text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-user-shield fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-danger px-3 py-2">
                                <i className="fas fa-crown"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.admins}</h2>
                        <p className="mb-0 fw-semibold">Administradores</p>
                        <small className="opacity-75">Control total del sistema</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-warning text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-user-tie fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-warning px-3 py-2">
                                <i className="fas fa-briefcase"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.workers}</h2>
                        <p className="mb-0 fw-semibold">Trabajadores</p>
                        <small className="opacity-75">Gestión de encuestas</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3 mb-4">
                <div className="card border-0 shadow-lg stats-card bg-gradient-info text-white">
                    <div className="card-body text-center p-4">
                        <div className="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <i className="fas fa-user fa-3x opacity-75"></i>
                            </div>
                            <div className="badge bg-light text-info px-3 py-2">
                                <i className="fas fa-poll"></i>
                            </div>
                        </div>
                        <h2 className="display-6 fw-bold mb-2">{stats.users}</h2>
                        <p className="mb-0 fw-semibold">Usuarios</p>
                        <small className="opacity-75">Participan en encuestas</small>
                    </div>
                </div>
            </div>
        </div>
    );

    // Componente de fila de usuario (tabla compacta)
    const UserRow = ({ user }) => {
        // Obtener ID del usuario actual desde el contexto global
        const currentUserId = window.currentUserId;
        const getRoleInfo = (roleName) => {
            const roleMap = {
                'Administrador': { class: 'bg-danger', icon: 'fas fa-user-shield' },
                'Trabajador': { class: 'bg-warning', icon: 'fas fa-user-tie' },
                'Usuario': { class: 'bg-info', icon: 'fas fa-user' }
            };
            return roleMap[roleName] || { class: 'bg-secondary', icon: 'fas fa-user-question' };
        };

        const roleInfo = getRoleInfo(user.rol ? user.rol.name : 'Sin rol');

        return (
            <tr className="user-row">
                <td>
                    <div className="d-flex align-items-center">
                        <div className="avatar-sm me-3">
                            <i className={`${roleInfo.icon} text-primary`}></i>
                        </div>
                        <div>
                            <div className="fw-bold text-primary">@{user.username}</div>
                            <small className="text-muted">{user.first_name} {user.last_name}</small>
                        </div>
                    </div>
                </td>
                <td>
                    <span className="text-muted">{user.email}</span>
                </td>
                <td>
                    <span className={`badge ${roleInfo.class} px-2 py-1`}>
                        <i className={`${roleInfo.icon} me-1`}></i>
                        {user.rol ? user.rol.name : 'Sin rol'}
                    </span>
                </td>
                <td>
                    <small className="text-muted">
                        {new Date(user.date_joined).toLocaleDateString('es-ES')}
                    </small>
                </td>
                <td>
                    {currentUserId && user.id === currentUserId ? (
                        <span className="badge bg-secondary px-3 py-2">
                            <i className="fas fa-lock me-1"></i>Tu cuenta
                        </span>
                    ) : (
                        <div className="dropdown">
                            <button 
                                className="btn btn-sm btn-outline-primary dropdown-toggle" 
                                type="button" 
                                data-bs-toggle="dropdown"
                            >
                                <i className="fas fa-user-cog me-1"></i>Cambiar
                            </button>
                            <ul className="dropdown-menu">
                                <li>
                                    <a className="dropdown-item" href={`/polls/user/${user.id}/role/Usuario/`}>
                                        <i className="fas fa-user me-2 text-info"></i>Usuario
                                    </a>
                                </li>
                                <li>
                                    <a className="dropdown-item" href={`/polls/user/${user.id}/role/Trabajador/`}>
                                        <i className="fas fa-user-tie me-2 text-warning"></i>Trabajador
                                    </a>
                                </li>
                                <li>
                                    <a className="dropdown-item" href={`/polls/user/${user.id}/role/Administrador/`}>
                                        <i className="fas fa-user-shield me-2 text-danger"></i>Administrador
                                    </a>
                                </li>
                            </ul>
                        </div>
                    )}
                </td>
            </tr>
        );
    };

    return (
        <div className="user-management-enhanced">
            {/* Estadísticas */}
            <UserStatsCards />

            {/* Panel de control */}
            <div className="row mb-5">
                <div className="col-12">
                    <div className="card border-0 shadow-lg control-panel-users">
                        <div className="card-header bg-gradient-primary text-white border-0">
                            <div className="d-flex justify-content-between align-items-center">
                                <h5 className="mb-0 fw-bold">
                                    <i className="fas fa-filter me-2"></i>
                                    Filtros de Búsqueda
                                </h5>
                                <div className="badge bg-light text-primary px-3 py-2 fs-6">
                                    {filteredUsers.length} usuario{filteredUsers.length !== 1 ? 's' : ''} encontrado{filteredUsers.length !== 1 ? 's' : ''}
                                </div>
                            </div>
                        </div>
                        <div className="card-body p-4">
                            <div className="row g-4">
                                <div className="col-md-5">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-search me-2"></i>Búsqueda de Usuarios
                                    </label>
                                    <div className="input-group input-group-lg">
                                        <span className="input-group-text bg-light border-0">
                                            <i className="fas fa-search text-primary"></i>
                                        </span>
                                        <input
                                            type="text"
                                            className="form-control border-0 shadow-sm"
                                            placeholder="Nombre, usuario, email..."
                                            value={filters.search}
                                            onChange={(e) => setFilters({...filters, search: e.target.value})}
                                        />
                                    </div>
                                </div>
                                <div className="col-md-3">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-user-tag me-2"></i>Filtrar por Rol
                                    </label>
                                    <select
                                        className="form-select form-select-lg border-0 shadow-sm"
                                        value={filters.role}
                                        onChange={(e) => setFilters({...filters, role: e.target.value})}
                                    >
                                        <option value="">👥 Todos los Roles</option>
                                        <option value="Usuario">👤 Usuarios</option>
                                        <option value="Trabajador">👔 Trabajadores</option>
                                        <option value="Administrador">🛡️ Administradores</option>
                                    </select>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label fw-bold text-primary mb-3">
                                        <i className="fas fa-sort-amount-down me-2"></i>Ordenar por
                                    </label>
                                    <select
                                        className="form-select form-select-lg border-0 shadow-sm"
                                        value={filters.sortBy}
                                        onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
                                    >
                                        <option value="username">📝 Nombre de Usuario</option>
                                        <option value="name">👤 Nombre Completo</option>
                                        <option value="email">📧 Email</option>
                                        <option value="role">🏷️ Rol</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tabla de usuarios */}
            <div className="row">
                <div className="col-12">
                    <div className="card border-0 shadow-lg">
                        <div className="card-body p-0">
                            {filteredUsers.length > 0 ? (
                                <div className="table-responsive">
                                    <table className="table table-hover mb-0">
                                        <thead className="table-light">
                                            <tr>
                                                <th className="border-0 fw-bold text-primary">Usuario</th>
                                                <th className="border-0 fw-bold text-primary">Email</th>
                                                <th className="border-0 fw-bold text-primary">Rol</th>
                                                <th className="border-0 fw-bold text-primary">Registro</th>
                                                <th className="border-0 fw-bold text-primary">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {filteredUsers.map(user => (
                                                <UserRow key={user.id} user={user} />
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <div className="text-center py-5">
                                    <div className="mb-4">
                                        <i className="fas fa-user-slash fa-4x text-primary opacity-50"></i>
                                    </div>
                                    <h4 className="fw-bold text-primary mb-3">No se encontraron usuarios</h4>
                                    <p className="text-muted mb-4">
                                        {filters.search || filters.role 
                                            ? 'Intenta ajustar los filtros de búsqueda' 
                                            : 'No hay usuarios registrados en el sistema'}
                                    </p>
                                    {(filters.search || filters.role) && (
                                        <button 
                                            className="btn btn-outline-primary"
                                            onClick={() => setFilters({search: '', role: '', sortBy: 'username'})}
                                        >
                                            <i className="fas fa-refresh me-2"></i>Limpiar Filtros
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Estilos para gestión de usuarios
const userManagementStyles = `
.user-row {
    transition: all 0.2s ease;
}

.user-row:hover {
    background-color: rgba(24, 77, 161, 0.05) !important;
}

.avatar-sm {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(24, 77, 161, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.control-panel-users {
    border-radius: 15px !important;
    overflow: hidden;
}

.bg-gradient-danger {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
}

.stats-card {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-radius: 15px !important;
    overflow: hidden;
}

.stats-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
}

.user-info {
    background: rgba(24, 77, 161, 0.05);
    border-radius: 10px;
    padding: 15px;
}

.dropdown-menu {
    border-radius: 10px !important;
    border: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.dropdown-item:hover {
    background: rgba(24, 77, 161, 0.1);
}
`;

// Inyectar estilos
if (!document.getElementById('user-management-styles')) {
    const style = document.createElement('style');
    style.id = 'user-management-styles';
    style.textContent = userManagementStyles;
    document.head.appendChild(style);
}