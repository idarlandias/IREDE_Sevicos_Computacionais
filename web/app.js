document.addEventListener('DOMContentLoaded', () => {
    const statusDot = document.querySelector('.dot');
    const updateTimeEl = document.getElementById('last-update-time');
    
    async function fetchStatus() {
        // Simulate loading state
        document.body.style.cursor = 'wait';
        
        try {
            // Add timestamp to prevent caching
            const response = await fetch(`/api/status?_=${new Date().getTime()}`);
            if (!response.ok) throw new Error('Network error');
            
            const data = await response.json();
            
            // Update metrics
            document.getElementById('api-version').textContent = data.version;
            document.getElementById('api-uptime').textContent = data.uptime;
            document.getElementById('api-env').textContent = data.env;
            document.getElementById('api-visits').textContent = data.visit_count;
            
            // Update time
            const now = new Date();
            updateTimeEl.textContent = now.toLocaleTimeString();
            
            // Visual feedback
            statusDot.style.backgroundColor = '#10b981';
            statusDot.style.boxShadow = '0 0 10px #10b981';
            
        } catch (error) {
            console.error('Error fetching status:', error);
            statusDot.style.backgroundColor = '#ef4444';
            statusDot.style.boxShadow = '0 0 10px #ef4444';
        } finally {
            document.body.style.cursor = 'default';
        }
    }

    // Initial load
    fetchStatus();

    // Button handler
    document.getElementById('refresh-btn').addEventListener('click', fetchStatus);
    // Register Visit Handler
    document.getElementById('register-btn').addEventListener('click', async () => {
        const nameInput = document.getElementById('visitor-name');
        const name = nameInput.value.trim();
        
        if (!name) {
            alert("Por favor, digite um nome.");
            return;
        }
        
        try {
            const res = await fetch('/api/visit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            
            if (res.ok) {
                nameInput.value = '';
                fetchVisits(); // Refresh list
            } else {
                alert("Erro ao salvar visita.");
            }
        } catch (e) {
            console.error(e);
            alert("Erro de conexão.");
        }
    });

    async function fetchVisits() {
        try {
            const res = await fetch(`/api/visits?_=${new Date().getTime()}`);
            if (res.ok) {
                const logs = await res.json();
                const container = document.getElementById('visits-log');
                
                if (logs.length === 0) {
                    container.innerHTML = '<div style="opacity: 0.5; font-style: italic;">Nenhuma visita gravada ainda...</div>';
                    return;
                }
                
                container.innerHTML = logs.map(log => {
                    // Force UTC interpretation by appending 'Z' if missing
                    const timeStr = log.timestamp.endsWith('Z') ? log.timestamp : log.timestamp + 'Z';
                    const localTime = new Date(timeStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
                    return `<div><span style="color: #4ade80">●</span> <b>${log.name}</b> <span style="opacity: 0.6">em ${localTime}</span></div>`;
                }).join('');
            }
        } catch (e) {
            console.error(e);
        }
    }
    
    // Advanced Features
    const tokenInput = document.getElementById('auth-token');
    
    // Charts
    const ctx = document.getElementById('visitsChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Visitas (Tempo Real)',
                data: [],
                borderColor: '#10b981',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: { 
                y: { 
                    beginAtZero: true, 
                    grid: { color: 'rgba(128,128,128,0.2)' },
                    ticks: { color: document.body.classList.contains('light-mode') ? '#1e293b' : '#94a3b8' }
                }, 
                x: { 
                    grid: { color: 'rgba(128,128,128,0.2)' },
                    ticks: { color: document.body.classList.contains('light-mode') ? '#1e293b' : '#94a3b8' }
                } 
            },
            plugins: { 
                legend: { 
                    labels: { color: document.body.classList.contains('light-mode') ? '#1e293b' : '#cbd5e1' } 
                } 
            }
        }
    });

    // Update Chart Colors on Theme Toggle
    document.getElementById('theme-toggle').addEventListener('click', () => {
        const isLight = document.body.classList.contains('light-mode');
        const textColor = isLight ? '#1e293b' : '#94a3b8';
        
        chart.options.scales.x.ticks.color = textColor;
        chart.options.scales.y.ticks.color = textColor;
        chart.options.plugins.legend.labels.color = textColor;
        chart.update();
    });

    // Update interval
    setInterval(async () => {
        const token = tokenInput.value;
        const now = new Date().toLocaleTimeString();

        // 1. Logs
        try {
            const res = await fetch('/api/logs');
            const data = await res.json();
            const logsContainer = document.getElementById('realtime-logs');
            logsContainer.innerHTML = data.logs.map(l => `<div>${l}</div>`).join('');
            logsContainer.scrollTop = logsContainer.scrollHeight;
        } catch(e) {}

        // 2. Health & Metrics
        try {
            const res = await fetch(`/api/healthcheck?token=${token}`);
            const data = await res.json();
            
            // Health UI
            const hStatus = document.getElementById('health-status');
            hStatus.innerHTML = `Health: ${data.status === 'healthy' ? '✅' : '❌'} | Auth: ${data.auth === 'authenticated' ? '🔓' : '🔒'}`;
            
            // Metrics Chart update
            const mRes = await fetch('/api/metrics');
            const mData = await mRes.json();
            
            if(chart.data.labels.length > 10) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }
            chart.data.labels.push(now);
            chart.data.datasets[0].data.push(mData.total_visits);
            chart.update();
            
        } catch(e) {}
        
    }, 5000);
});
