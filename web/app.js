document.addEventListener('DOMContentLoaded', () => {
    const statusDot = document.querySelector('.dot');
    const updateTimeEl = document.getElementById('last-update-time');
    
    async function fetchStatus() {
        // Simulate loading state
        document.body.style.cursor = 'wait';
        
        try {
            const response = await fetch('/api/status');
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
});
