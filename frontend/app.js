const API_URL = 'http://127.0.0.1:8000';

let employees = [];
let tasks = [];
let currentEmployeeId = null;
let currentTaskId = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadEmployees();
    loadTasks();
});

// Tab switching
function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'employees') {
        loadEmployees();
    } else {
        loadTasks();
    }
}

// Notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// ========== EMPLOYEES ==========

async function loadEmployees() {
    try {
        const response = await fetch(`${API_URL}/employees/`);
        employees = await response.json();
        // Ensure each employee has an id field
        employees = employees.map(emp => ({
            ...emp,
            id: emp.id || emp._id
        }));
        renderEmployees();
        updateEmployeeDropdown();
    } catch (error) {
        console.error('Error loading employees:', error);
        showNotification('Failed to load employees', 'error');
    }
}

function renderEmployees() {
    const container = document.getElementById('employees-list');
    
    if (employees.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No Employees Yet</h3>
                <p>Click "Add Employee" to create your first employee</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = employees.map(emp => `
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">${emp.name}</div>
                    <div class="card-subtitle">${emp.email}</div>
                </div>
                <span class="badge ${emp.is_active ? 'badge-active' : 'badge-inactive'}">
                    ${emp.is_active ? 'Active' : 'Inactive'}
                </span>
            </div>
            <div class="card-body">
                <div class="card-info">
                    ${emp.position ? `
                        <div class="info-item">
                            <span class="info-label">Position:</span>
                            <span>${emp.position}</span>
                        </div>
                    ` : ''}
                    <div class="info-item">
                        <span class="info-label">ID:</span>
                        <span>${emp.id}</span>
                    </div>
                </div>
            </div>
            <div class="card-actions">
                <button class="btn btn-edit" onclick="editEmployee('${emp.id}')">Edit</button>
                <button class="btn btn-danger" onclick="deleteEmployee('${emp.id}')">Delete</button>
            </div>
        </div>
    `).join('');
}

function showEmployeeForm() {
    document.getElementById('employee-form').style.display = 'block';
    document.getElementById('employee-form-title').textContent = 'Add New Employee';
    document.getElementById('employeeForm').reset();
    document.getElementById('employee-id').value = '';
    document.getElementById('employee-active').checked = true;
    currentEmployeeId = null;
}

function cancelEmployeeForm() {
    document.getElementById('employee-form').style.display = 'none';
    currentEmployeeId = null;
}

async function handleEmployeeSubmit(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('employee-name').value,
        email: document.getElementById('employee-email').value,
        position: document.getElementById('employee-position').value || null,
        is_active: document.getElementById('employee-active').checked
    };
    
    try {
        let response;
        if (currentEmployeeId) {
            response = await fetch(`${API_URL}/employees/${currentEmployeeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch(`${API_URL}/employees/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            showNotification(currentEmployeeId ? 'Employee updated successfully' : 'Employee created successfully');
            cancelEmployeeForm();
            loadEmployees();
        } else {
            throw new Error('Failed to save employee');
        }
    } catch (error) {
        console.error('Error saving employee:', error);
        showNotification('Failed to save employee', 'error');
    }
}

async function editEmployee(id) {
    const employee = employees.find(e => e.id === id);
    if (!employee) return;
    
    currentEmployeeId = id;
    document.getElementById('employee-form-title').textContent = 'Edit Employee';
    document.getElementById('employee-id').value = id;
    document.getElementById('employee-name').value = employee.name;
    document.getElementById('employee-email').value = employee.email;
    document.getElementById('employee-position').value = employee.position || '';
    document.getElementById('employee-active').checked = employee.is_active;
    document.getElementById('employee-form').style.display = 'block';
}

async function deleteEmployee(id) {
    if (!confirm('Are you sure you want to delete this employee?')) return;
    
    try {
        const response = await fetch(`${API_URL}/employees/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Employee deleted successfully');
            loadEmployees();
        } else {
            throw new Error('Failed to delete employee');
        }
    } catch (error) {
        console.error('Error deleting employee:', error);
        showNotification('Failed to delete employee', 'error');
    }
}

// ========== TASKS ==========

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks/`);
        tasks = await response.json();
        // Ensure each task has an id field
        tasks = tasks.map(task => ({
            ...task,
            id: task.id || task._id
        }));
        renderTasks();
    } catch (error) {
        console.error('Error loading tasks:', error);
        showNotification('Failed to load tasks', 'error');
    }
}

function renderTasks() {
    const container = document.getElementById('tasks-list');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No Tasks Yet</h3>
                <p>Click "Add Task" to create your first task</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => {
        const assignedEmployee = task.employee_id ? employees.find(e => e.id === task.employee_id) : null;
        const statusBadge = task.status === 'done' ? 'badge-done' : 
                           task.status === 'in_progress' ? 'badge-in-progress' : 'badge-pending';
        const statusText = task.status === 'in_progress' ? 'In Progress' : 
                          task.status.charAt(0).toUpperCase() + task.status.slice(1);
        
        return `
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">${task.title}</div>
                    </div>
                    <span class="badge ${statusBadge}">${statusText}</span>
                </div>
                <div class="card-body">
                    <div class="card-info">
                        ${task.description ? `
                            <div class="info-item">
                                <span class="info-label">Description:</span>
                                <span>${task.description}</span>
                            </div>
                        ` : ''}
                        ${assignedEmployee ? `
                            <div class="info-item">
                                <span class="info-label">Assigned to:</span>
                                <span>${assignedEmployee.name}</span>
                            </div>
                        ` : '<div class="info-item"><span class="badge badge-pending">Unassigned</span></div>'}
                        <div class="info-item">
                            <span class="info-label">ID:</span>
                            <span>${task.id}</span>
                        </div>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="btn btn-edit" onclick="editTask('${task.id}')">Edit</button>
                    <button class="btn btn-danger" onclick="deleteTask('${task.id}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function updateEmployeeDropdown() {
    const select = document.getElementById('task-employee');
    select.innerHTML = '<option value="">-- Unassigned --</option>' +
        employees.map(emp => `<option value="${emp.id}">${emp.name}</option>`).join('');
}

function showTaskForm() {
    document.getElementById('task-form').style.display = 'block';
    document.getElementById('task-form-title').textContent = 'Add New Task';
    document.getElementById('taskForm').reset();
    document.getElementById('task-id').value = '';
    currentTaskId = null;
    loadEmployees(); // Refresh employee dropdown
}

function cancelTaskForm() {
    document.getElementById('task-form').style.display = 'none';
    currentTaskId = null;
}

async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const employeeId = document.getElementById('task-employee').value;
    
    const data = {
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-description').value || null,
        status: document.getElementById('task-status').value,
        employee_id: employeeId || null
    };
    
    try {
        let response;
        if (currentTaskId) {
            response = await fetch(`${API_URL}/tasks/${currentTaskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch(`${API_URL}/tasks/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            showNotification(currentTaskId ? 'Task updated successfully' : 'Task created successfully');
            cancelTaskForm();
            loadTasks();
        } else {
            throw new Error('Failed to save task');
        }
    } catch (error) {
        console.error('Error saving task:', error);
        showNotification('Failed to save task', 'error');
    }
}

async function editTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    
    currentTaskId = id;
    document.getElementById('task-form-title').textContent = 'Edit Task';
    document.getElementById('task-id').value = id;
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-description').value = task.description || '';
    document.getElementById('task-status').value = task.status;
    document.getElementById('task-employee').value = task.employee_id || '';
    document.getElementById('task-form').style.display = 'block';
}

async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Task deleted successfully');
            loadTasks();
        } else {
            throw new Error('Failed to delete task');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        showNotification('Failed to delete task', 'error');
    }
}
