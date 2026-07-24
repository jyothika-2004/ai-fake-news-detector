document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('detector-form');
    const newsInput = document.getElementById('news-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    
    const resultsSection = document.getElementById('results-section');
    const confidenceCircle = document.getElementById('confidence-circle');
    const confidenceText = document.getElementById('confidence-text');
    const predictionLabel = document.getElementById('prediction-label');
    const predictionDesc = document.getElementById('prediction-desc');
    const indicatorsList = document.getElementById('indicators-list');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = newsInput.value.trim();
        if (!text) return;

        // UI: Show loading state
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
        analyzeBtn.disabled = true;
        resultsSection.classList.add('hidden');

        // Simulate API call to the backend model
        // In a real deployment, this would be a fetch() call to a Flask/FastAPI backend
        try {
            const result = await mockPredict(text);
            displayResults(result);
        } catch (error) {
            console.error("Analysis failed", error);
            alert("Failed to analyze the article. Please try again.");
        } finally {
            // UI: Reset loading state
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        // Unhide results section
        resultsSection.classList.remove('hidden');

        const confidence = data.confidence;
        const isFake = data.prediction === 'Fake News';

        // Update Text
        predictionLabel.textContent = data.prediction;
        predictionLabel.style.color = isFake ? 'var(--danger)' : 'var(--success)';
        
        predictionDesc.textContent = isFake 
            ? "High probability of deceptive or fabricated content."
            : "Content appears consistent with factual reporting.";

        // Update Circular Chart
        // Stroke dasharray max is 100. format: "value, 100"
        setTimeout(() => {
            confidenceCircle.setAttribute('stroke-dasharray', `${confidence}, 100`);
            confidenceCircle.style.stroke = isFake ? 'var(--danger)' : 'var(--success)';
        }, 100); // Small delay to trigger CSS transition

        // Animate counter
        animateValue(confidenceText, 0, confidence, 1000);

        // Update Indicators
        indicatorsList.innerHTML = '';
        data.indicators.forEach(indicator => {
            const li = document.createElement('li');
            li.textContent = indicator;
            indicatorsList.appendChild(li);
        });
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Mock Backend Prediction
    function mockPredict(text) {
        return new Promise(resolve => {
            setTimeout(() => {
                const textLength = text.length;
                // Simple deterministic mock based on text length for demo purposes
                const isFake = textLength % 2 !== 0; 
                
                // Base confidence 60 + random 0-39
                const confidence = 60 + Math.floor(Math.random() * 39);
                
                resolve({
                    prediction: isFake ? 'Fake News' : 'Real News',
                    confidence: confidence,
                    indicators: isFake ? [
                        "High usage of sensationalist language detected.",
                        "Lack of credible sources or verifiable facts.",
                        "Structural anomalies typical of generated text."
                    ] : [
                        "Language structure is consistent with factual reporting.",
                        "Neutral tone detected.",
                        "Absence of common deception markers."
                    ]
                });
            }, 1500); // 1.5s simulated network delay
        });
    }

    // Number animation helper
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start) + '%';
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
