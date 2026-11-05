/**
 * AI Resume Analyzer & Builder - Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initFileUpload();
    initScoreAnimation();
    initPrintResume();
    initCopyToClipboard();
    initFormHelpers();
});

/* ==========================================
   1. Theme Toggle (Dark / Light Mode)
   ========================================== */
function initThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-toggle-icon');

    if (!themeToggleBtn) return;

    // Check existing setting or preferred color scheme
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');

    document.documentElement.setAttribute('data-bs-theme', currentTheme);
    updateThemeIcon(themeIcon, currentTheme);

    themeToggleBtn.addEventListener('click', () => {
        const activeTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = activeTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(themeIcon, newTheme);
    });
}

function updateThemeIcon(iconElement, theme) {
    if (!iconElement) return;
    if (theme === 'dark') {
        iconElement.className = 'bi bi-sun-fill text-warning';
    } else {
        iconElement.className = 'bi bi-moon-stars-fill text-primary';
    }
}

/* ==========================================
   2. Drag & Drop File Upload
   ========================================== */
function initFileUpload() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resume-file-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    const fileDetails = document.getElementById('file-details');
    const fileSizeDisplay = document.getElementById('file-size-display');
    const submitBtn = document.getElementById('upload-submit-btn');
    const uploadSpinner = document.getElementById('upload-spinner');
    const uploadForm = document.getElementById('upload-form');

    if (!dropZone || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-active'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-active'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        const allowedTypes = ['.pdf', '.docx', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        const isAllowed = allowedTypes.some(type => file.name.toLowerCase().endsWith(type) || file.type === type);

        if (!isAllowed) {
            showToast('Invalid file format. Please upload a PDF or DOCX file.', 'danger');
            fileInput.value = '';
            if (fileDetails) fileDetails.classList.add('d-none');
            return;
        }

        if (fileNameDisplay) fileNameDisplay.textContent = file.name;
        if (fileSizeDisplay) fileSizeDisplay.textContent = formatBytes(file.size);
        if (fileDetails) fileDetails.classList.remove('d-none');
    }

    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            if (submitBtn) {
                submitBtn.disabled = true;
            }
            if (uploadSpinner) {
                uploadSpinner.classList.remove('d-none');
            }
        });
    }
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/* ==========================================
   3. Animated ATS Score Ring / Counter
   ========================================== */
function initScoreAnimation() {
    const scoreElement = document.getElementById('ats-score-value');
    const scoreCircle = document.getElementById('score-gauge-circle');

    if (!scoreElement) return;

    const targetScore = parseInt(scoreElement.getAttribute('data-score') || '0', 10);
    let currentScore = 0;
    const duration = 1200; // ms
    const stepTime = Math.abs(Math.floor(duration / (targetScore || 1)));

    const timer = setInterval(() => {
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(timer);
        } else {
            currentScore++;
        }
        scoreElement.textContent = currentScore;
    }, Math.max(stepTime, 12));

    if (scoreCircle) {
        const radius = scoreCircle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        scoreCircle.style.strokeDasharray = `${circumference} ${circumference}`;

        const offset = circumference - (targetScore / 100) * circumference;
        setTimeout(() => {
            scoreCircle.style.strokeDashoffset = offset;
        }, 100);
    }
}

/* ==========================================
   4. Print Resume / PDF Export
   ========================================== */
function initPrintResume() {
    const printBtn = document.getElementById('print-resume-btn');
    if (!printBtn) return;

    printBtn.addEventListener('click', () => {
        window.print();
    });
}

/* ==========================================
   5. Copy to Clipboard Utility
   ========================================== */
function initCopyToClipboard() {
    document.querySelectorAll('.btn-copy').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSelector = btn.getAttribute('data-copy-target');
            const target = document.querySelector(targetSelector);
            if (!target) return;

            const textToCopy = target.innerText || target.value;
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = btn.innerHTML;
                btn.innerHTML = `<i class="bi bi-check2"></i> Copied!`;
                btn.classList.replace('btn-outline-secondary', 'btn-success');
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.classList.replace('btn-success', 'btn-outline-secondary');
                }, 2000);
            }).catch(err => {
                showToast('Failed to copy text', 'danger');
            });
        });
    });
}

/* ==========================================
   6. Form Helpers & Character Counters
   ========================================== */
function initFormHelpers() {
    // Enable Bootstrap tooltips if any
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
    }

    // Auto add form-control class to standard Django text inputs/textareas if missing
    document.querySelectorAll('form p input[type="text"], form p input[type="email"], form p input[type="password"], form p textarea, form p select').forEach(el => {
        if (!el.classList.contains('form-control') && !el.classList.contains('form-select')) {
            if (el.tagName.toLowerCase() === 'select') {
                el.classList.add('form-select');
            } else {
                el.classList.add('form-control');
            }
        }
    });
}

/* ==========================================
   7. Toast Notification Helper
   ========================================== */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${type} border-0 show mb-2 shadow`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body d-flex align-items-center gap-2">
                <i class="bi ${type === 'danger' ? 'bi-exclamation-octagon-fill' : type === 'success' ? 'bi-check-circle-fill' : 'bi-info-circle-fill'} fs-5"></i>
                <span>${message}</span>
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastEl);

    setTimeout(() => {
        toastEl.classList.remove('show');
        setTimeout(() => toastEl.remove(), 300);
    }, 4000);
}
