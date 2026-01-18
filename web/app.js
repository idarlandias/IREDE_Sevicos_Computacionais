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
                
                container.innerHTML = logs.map(log => 
                    `<div><span style="color: #4ade80">●</span> <b>${log.name}</b> <span style="opacity: 0.6">em ${log.timestamp.split('T')[1].split('.')[0]}</span></div>`
                ).join('');
            }
        } catch (e) {
            console.error(e);
        }
    }
    
    fetchVisits(); // Initial load of visits
});
