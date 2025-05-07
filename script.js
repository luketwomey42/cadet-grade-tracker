/**
 * Cadet Academic Tracker - Custom JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Apply grade coloring to table cells
    applyGradeColoring();
    
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    // Setup form validation
    setupFormValidation();
    
    // Setup flash message auto-dismissal
    setupFlashMessages();
});

/**
 * Apply enhanced color-coding to grade elements with visual effects and better user experience
 */
function applyGradeColoring() {
    // Static grade displays
    document.querySelectorAll('.grade-display').forEach(function(element) {
        const grade = element.textContent.trim();
        if (grade) {
            element.classList.add(`grade-${grade}`);
        }
    });
    
    // Enhanced grade select dropdowns
    document.querySelectorAll('select[name^="grade_"]').forEach(function(select) {
        const currentGrade = select.value;
        const slotId = select.name.split('_')[1];
        const classSelect = document.getElementById(`class_${slotId}`);
        
        // Apply initial styling
        if (currentGrade) {
            select.classList.add(`grade-${currentGrade}`);
            
            // Highlight the row to show classes with grades
            if (classSelect) {
                classSelect.style.fontWeight = 'bold';
                classSelect.parentElement.style.backgroundColor = 'rgba(13, 110, 253, 0.05)';
            }
        }
        
        // Add change event with enhanced visual feedback
        select.addEventListener('change', function() {
            // Remove all existing grade classes
            ['A', 'B', 'C', 'D', 'F'].forEach(grade => {
                select.classList.remove(`grade-${grade}`);
            });
            
            // Add new grade class with animation effect
            if (this.value) {
                // Apply the grade class
                select.classList.add(`grade-${this.value}`);
                
                // Add visual feedback with animation
                select.style.transition = 'all 0.3s ease';
                select.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    select.style.transform = 'scale(1)';
                }, 300);
                
                // Highlight the row to show it has a grade
                if (classSelect) {
                    classSelect.style.fontWeight = 'bold';
                    classSelect.parentElement.style.backgroundColor = 'rgba(13, 110, 253, 0.05)';
                }
            } else {
                // Remove highlighting if no grade
                if (classSelect) {
                    classSelect.style.fontWeight = 'normal';
                    classSelect.parentElement.style.backgroundColor = '';
                }
            }
        });
        
        // Add focus effects for better UX
        select.addEventListener('focus', function() {
            if (!this.disabled) {
                this.style.boxShadow = '0 0 0 0.25rem rgba(13, 110, 253, 0.25)';
            }
        });
        
        select.addEventListener('blur', function() {
            this.style.boxShadow = '';
        });
    });
    
    // Make class selects interact with grade selects
    document.querySelectorAll('select[id^="class_"]').forEach(function(select) {
        select.addEventListener('change', function() {
            const slotId = this.id.split('_')[1];
            const gradeSelect = document.querySelector(`select[name="grade_${slotId}"]`);
            
            if (gradeSelect) {
                if (this.value && this.value !== 'custom') {
                    // Enable grade selection when a class is selected
                    gradeSelect.disabled = false;
                    gradeSelect.focus(); // Auto-focus on grade after selecting class
                } else if (this.value === 'custom') {
                    // Don't enable grade yet for custom classes until text is entered
                    gradeSelect.disabled = true;
                } else {
                    // Disable and clear grade when no class is selected
                    gradeSelect.disabled = true;
                    gradeSelect.value = '';
                    // Remove grade coloring
                    ['A', 'B', 'C', 'D', 'F'].forEach(grade => {
                        gradeSelect.classList.remove(`grade-${grade}`);
                    });
                    // Remove row highlighting
                    this.style.fontWeight = 'normal';
                    this.parentElement.style.backgroundColor = '';
                }
            }
        });
    });
    
    // Handle custom class inputs
    document.querySelectorAll('.custom-class-input').forEach(function(input) {
        input.addEventListener('input', function() {
            const slotId = this.id.split('_')[2]; // Extract the slot number
            const gradeSelect = document.querySelector(`select[name="grade_${slotId}"]`);
            
            if (gradeSelect) {
                if (this.value.trim()) {
                    // Enable grade selection when custom class has text
                    gradeSelect.disabled = false;
                } else {
                    // Disable grade when custom class is empty
                    gradeSelect.disabled = true;
                }
            }
        });
    });
}

/**
 * Initialize Bootstrap components like tooltips and popovers
 */
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Setup client-side form validation
 */
function setupFormValidation() {
    // Add custom validation styles
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Setup auto-dismissal of flash messages after 5 seconds
 */
function setupFlashMessages() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}