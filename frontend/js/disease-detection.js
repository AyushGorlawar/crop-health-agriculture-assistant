// Disease Detection Module
class DiseaseDetectionModule {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.imageInput = document.getElementById('imageInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.resultsArea = document.getElementById('resultsArea');
        this.selectedFile = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Upload area click
        this.uploadArea.addEventListener('click', () => {
            this.imageInput.click();
        });

        // File input change
        this.imageInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            this.handleFileSelect(file);
        });

        // Analyze button
        this.analyzeBtn.addEventListener('click', () => {
            this.analyzeImage();
        });
    }

    handleFileSelect(file) {
        if (!file) return;

        try {
            // Validate file
            window.app.validateImage(file);
            
            this.selectedFile = file;
            this.displayImagePreview(file);
            this.analyzeBtn.disabled = false;
            
            // Show success message
            window.app.showNotification('Image selected successfully!', 'success');
            
        } catch (error) {
            window.app.showNotification(error.message, 'danger');
        }
    }

    displayImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.uploadArea.innerHTML = `
                <img src="${e.target.result}" alt="Preview" class="image-preview">
                <div class="mt-2">
                    <small class="text-muted">${file.name}</small>
                </div>
            `;
        };
        reader.readAsDataURL(file);
    }

    async analyzeImage() {
        if (!this.selectedFile) {
            window.app.showNotification('Please select an image first', 'warning');
            return;
        }

        try {
            window.app.showLoading('Analyzing image for diseases...');
            
            const formData = new FormData();
            formData.append('image', this.selectedFile);
            
            const response = await fetch(`${window.app.apiBaseUrl}/detect-disease`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                this.displayResults(result.result);
            } else {
                throw new Error(result.error || 'Analysis failed');
            }

        } catch (error) {
            window.app.handleError(error, 'disease detection');
        } finally {
            window.app.hideLoading();
        }
    }

    displayResults(result) {
        const confidence = (result.confidence * 100).toFixed(1);
        const severityClass = this.getSeverityClass(result.severity);
        
        this.resultsArea.innerHTML = `
            <div class="result-item ${severityClass} fade-in">
                <div class="d-flex align-items-center mb-3">
                    <span class="status-indicator status-${severityClass}"></span>
                    <h5 class="mb-0">${result.disease}</h5>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Crop Type:</strong> ${result.crop_type}</p>
                        <p><strong>Confidence:</strong> ${confidence}%</p>
                        <p><strong>Severity:</strong> ${result.severity}</p>
                    </div>
                    <div class="col-md-6">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${confidence}%"></div>
                        </div>
                        <small class="text-muted">Detection confidence</small>
                    </div>
                </div>
                
                <div class="mt-3">
                    <h6>Description:</h6>
                    <p>${result.description}</p>
                </div>
                
                <div class="mt-3">
                    <button class="btn btn-primary btn-sm" onclick="diseaseDetectionModule.getRemedies('${result.disease}', '${result.crop_type}')">
                        <i class="fas fa-medkit me-2"></i>
                        Get Remedies
                    </button>
                    <button class="btn btn-info btn-sm ms-2" onclick="diseaseDetectionModule.getYieldTips('${result.crop_type}')">
                        <i class="fas fa-lightbulb me-2"></i>
                        Yield Tips
                    </button>
                </div>
            </div>
        `;
    }

    getSeverityClass(severity) {
        switch (severity.toLowerCase()) {
            case 'high':
                return 'severe';
            case 'medium':
                return 'disease';
            case 'low':
            default:
                return 'healthy';
        }
    }

    async getRemedies(disease, cropType) {
        try {
            window.app.showLoading('Fetching remedies...');
            
            const response = await window.app.makeApiCall(`/remedies?disease=${encodeURIComponent(disease)}&crop=${encodeURIComponent(cropType)}`);
            
            if (response.success) {
                this.displayRemedies(response.remedies);
            } else {
                throw new Error(response.error || 'Failed to fetch remedies');
            }

        } catch (error) {
            window.app.handleError(error, 'remedies');
        } finally {
            window.app.hideLoading();
        }
    }

    displayRemedies(remedies) {
        const remediesHtml = `
            <div class="mt-4">
                <h6><i class="fas fa-medkit me-2"></i>Treatment Options</h6>
                
                ${remedies.organic ? `
                    <div class="tip-card">
                        <h6><i class="fas fa-leaf me-2"></i>Organic Remedies</h6>
                        <ul class="mb-0">
                            ${remedies.organic.map(remedy => `<li>${remedy}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${remedies.chemical ? `
                    <div class="tip-card">
                        <h6><i class="fas fa-flask me-2"></i>Chemical Treatments</h6>
                        <ul class="mb-0">
                            ${remedies.chemical.map(remedy => `<li>${remedy}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${remedies.preventive ? `
                    <div class="tip-card">
                        <h6><i class="fas fa-shield-alt me-2"></i>Preventive Measures</h6>
                        <ul class="mb-0">
                            ${remedies.preventive.map(remedy => `<li>${remedy}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
        
        this.resultsArea.insertAdjacentHTML('beforeend', remediesHtml);
    }

    async getYieldTips(cropType) {
        try {
            window.app.showLoading('Fetching yield tips...');
            
            const response = await window.app.makeApiCall(`/yield-tips?crop=${encodeURIComponent(cropType)}`);
            
            if (response.success) {
                this.displayYieldTips(response.tips);
            } else {
                throw new Error(response.error || 'Failed to fetch yield tips');
            }

        } catch (error) {
            window.app.handleError(error, 'yield tips');
        } finally {
            window.app.hideLoading();
        }
    }

    displayYieldTips(tips) {
        const tipsHtml = `
            <div class="mt-4">
                <h6><i class="fas fa-chart-line me-2"></i>Yield Improvement Tips</h6>
                
                ${Object.entries(tips).map(([category, tipList]) => `
                    <div class="tip-card">
                        <h6><i class="fas fa-seedling me-2"></i>${this.formatCategoryName(category)}</h6>
                        <ul class="mb-0">
                            ${tipList.map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>
                `).join('')}
            </div>
        `;
        
        this.resultsArea.insertAdjacentHTML('beforeend', tipsHtml);
    }

    formatCategoryName(category) {
        return category.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    reset() {
        this.selectedFile = null;
        this.analyzeBtn.disabled = true;
        this.uploadArea.innerHTML = `
            <div class="upload-content">
                <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                <p>Click to upload or drag and drop</p>
                <p class="text-muted">Supports: JPG, PNG, JPEG (Max: 16MB)</p>
            </div>
        `;
        this.resultsArea.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-microscope fa-3x mb-3"></i>
                <p>Upload an image to get started</p>
            </div>
        `;
    }
}

// Initialize disease detection module
document.addEventListener('DOMContentLoaded', () => {
    window.diseaseDetectionModule = new DiseaseDetectionModule();
}); 