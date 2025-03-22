/**
 * Veterinary Clinic Management Application
 */
document.addEventListener('DOMContentLoaded', () => {
    // Global variables
    let selectedOwnerId = null;
    let selectedPetId = null;
    let configData = {};
    let allSpecies = [];
    let allMedications = [];

    // DOM Elements
    const ownerNameInput = document.getElementById('ownerName');
    const ownerAddressInput = document.getElementById('ownerAddress');
    const ownerPhoneInput = document.getElementById('ownerPhone');
    const ownerSuggestions = document.getElementById('ownerSuggestions');
    
    const petNameInput = document.getElementById('petName');
    const petSpeciesInput = document.getElementById('petSpecies');
    const petBreedInput = document.getElementById('petBreed');
    const petAgeInput = document.getElementById('petAge');
    const petSexInput = document.getElementById('petSex');
    const petSuggestions = document.getElementById('petSuggestions');
    const speciesSuggestions = document.getElementById('speciesSuggestions');
    
    const complaintInput = document.getElementById('complaint');
    const examinationInput = document.getElementById('examination');
    const treatmentInput = document.getElementById('treatment');
    const testsInput = document.getElementById('tests');
    const nextVisitInput = document.getElementById('nextVisit');
    
    const historyList = document.getElementById('historyList');
    
    const btnSave = document.getElementById('btnSave');
    const btnSavePrint = document.getElementById('btnSavePrint');
    const btnReset = document.getElementById('btnReset');
    const btnReset2 = document.getElementById('btnReset2');
    const btnSettings = document.getElementById('btnSettings');
    const btnMedications = document.getElementById('btnMedications');
    
    // Dialogs
    const overlay = document.getElementById('overlay');
    const medicationsDialog = document.getElementById('medicationsDialog');
    const settingsDialog = document.getElementById('settingsDialog');
    const confirmDialog = document.getElementById('confirmDialog');
    const toast = document.getElementById('toast');
    
    const medicationSearch = document.getElementById('medicationSearch');
    const medicationsList = document.getElementById('medicationsList');
    const saveFolderInput = document.getElementById('saveFolder');
    const btnBrowse = document.getElementById('btnBrowse');
    const btnSaveSettings = document.getElementById('btnSaveSettings');
    const btnConfirmYes = document.getElementById('btnConfirmYes');
    const btnConfirmNo = document.getElementById('btnConfirmNo');
    const confirmMessage = document.getElementById('confirmMessage');
    
    // Initialize application
    async function init() {
        // Update loading status
        const loadingOverlay = document.getElementById('loadingOverlay');
        const connectionStatus = document.getElementById('connectionStatus');
        
        if (connectionStatus) {
            connectionStatus.textContent = 'Connecting to server...';
        }
        
        // Try 5 times to connect to the API with increasing delay
        let attempts = 0;
        const maxAttempts = 5;
        
        async function attemptConnection() {
            try {
                console.log(`Connection attempt ${attempts + 1}/${maxAttempts}...`);
                if (connectionStatus) {
                    connectionStatus.textContent = `Connection attempt ${attempts + 1}/${maxAttempts}...`;
                }
                
                // Check if API is alive
                console.log('Checking API health...');
                await apiService.healthCheck();
                console.log('API health check successful');
                
                if (connectionStatus) {
                    connectionStatus.textContent = 'Connected to server successfully!';
                }
                return true;
            } catch (error) {
                console.error(`Connection attempt ${attempts + 1} failed:`, error);
                if (connectionStatus) {
                    connectionStatus.textContent = `Connection attempt ${attempts + 1} failed. Retrying...`;
                }
                return false;
            }
        }
        
        while (attempts < maxAttempts) {
            if (await attemptConnection()) {
                break;
            }
            attempts++;
            
            // Wait a bit longer between attempts (exponential backoff)
            const delay = Math.min(1000 * Math.pow(2, attempts - 1), 10000);
            if (attempts < maxAttempts) {
                console.log(`Waiting ${delay}ms before next attempt...`);
                if (connectionStatus) {
                    connectionStatus.textContent = `Waiting ${delay}ms before next attempt...`;
                }
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
        
        if (attempts >= maxAttempts) {
            console.error('Failed to connect to server after multiple attempts');
            
            // Show error message in the loading overlay
            if (loadingOverlay && connectionStatus) {
                loadingOverlay.style.backgroundColor = 'rgba(255, 200, 200, 0.9)';
                connectionStatus.style.color = 'red';
                connectionStatus.style.fontWeight = 'bold';
                connectionStatus.textContent = 'Failed to connect to server. Please reload the page or check your network connection.';
                
                // Add reload button
                const reloadBtn = document.createElement('button');
                reloadBtn.className = 'primary-button';
                reloadBtn.style.marginTop = '20px';
                reloadBtn.textContent = 'Reload Page';
                reloadBtn.addEventListener('click', () => window.location.reload());
                loadingOverlay.appendChild(reloadBtn);
            } else {
                showToast('Failed to connect to server. Please check if the server is running and reload the page.', 'error');
            }
            return;
        }
        
        try {
            // Load configuration
            if (connectionStatus) {
                connectionStatus.textContent = 'Loading application configuration...';
            }
            console.log('Loading configuration...');
            await loadConfig();
            console.log('Configuration loaded successfully');
            
            // Load species
            if (connectionStatus) {
                connectionStatus.textContent = 'Loading species data...';
            }
            await loadSpeciesList();
            
            // Load medications
            if (connectionStatus) {
                connectionStatus.textContent = 'Loading medications data...';
            }
            await loadMedicationsList();
            
            // Set up event listeners
            if (connectionStatus) {
                connectionStatus.textContent = 'Setting up application...';
            }
            setupEventListeners();
            
            // Reset form
            resetForm();
            
            // Set initial date for next visit to today
            const today = new Date().toISOString().split('T')[0];
            nextVisitInput.value = today;
            
            console.log('App initialization complete');
            
            // Hide loading overlay
            if (loadingOverlay) {
                loadingOverlay.style.display = 'none';
            }
            
        } catch (error) {
            console.error('Error during app initialization:', error);
            
            if (loadingOverlay && connectionStatus) {
                loadingOverlay.style.backgroundColor = 'rgba(255, 200, 200, 0.9)';
                connectionStatus.style.color = 'red';
                connectionStatus.textContent = 'Error initializing application: ' + error.message;
                
                // Add reload button
                const reloadBtn = document.createElement('button');
                reloadBtn.className = 'primary-button';
                reloadBtn.style.marginTop = '20px';
                reloadBtn.textContent = 'Reload Page';
                reloadBtn.addEventListener('click', () => window.location.reload());
                loadingOverlay.appendChild(reloadBtn);
            } else {
                showToast('Error initializing application. Some features may not work properly.', 'error');
            }
        }
    }
    
    // Setup event listeners
    function setupEventListeners() {
        // Owner autocomplete
        ownerNameInput.addEventListener('input', debounce(handleOwnerSearch, 300));
        
        // Pet autocomplete
        petNameInput.addEventListener('input', debounce(handlePetSearch, 300));
        
        // Species autocomplete
        petSpeciesInput.addEventListener('input', debounce(handleSpeciesSearch, 300));
        
        // Medication search
        medicationSearch.addEventListener('input', debounce(handleMedicationSearch, 300));
        
        // Buttons
        btnSave.addEventListener('click', handleSave);
        btnSavePrint.addEventListener('click', handleSaveAndPrint);
        btnReset.addEventListener('click', () => showConfirmDialog('Are you sure you want to reset the form?', resetForm));
        btnReset2.addEventListener('click', () => showConfirmDialog('Are you sure you want to reset the form?', resetForm));
        btnSettings.addEventListener('click', () => {
            settingsDialog.classList.add('show');
            overlay.classList.add('show');
            
            // Make sure we have the latest config
            loadConfig();
        });
        btnMedications.addEventListener('click', showMedicationsDialog);
        
        // Settings dialog
        btnBrowse.addEventListener('click', handleBrowse);
        btnSaveSettings.addEventListener('click', handleSaveSettings);
        
        // Test PDF button
        const btnTestPdf = document.getElementById('btnTestPdf');
        if (btnTestPdf) {
            btnTestPdf.addEventListener('click', handleTestPdf);
        }
        
        // Dialog close buttons
        document.querySelectorAll('.close-button').forEach(button => {
            button.addEventListener('click', closeAllDialogs);
        });
        
        // Confirm dialog
        btnConfirmYes.addEventListener('click', () => {
            if (confirmDialog._callback) {
                confirmDialog._callback();
            }
            closeAllDialogs();
        });
        
        btnConfirmNo.addEventListener('click', closeAllDialogs);
        
        // Close dialogs when clicking overlay
        overlay.addEventListener('click', closeAllDialogs);
    }
    
    // Owner search and suggestions
    async function handleOwnerSearch() {
        const searchTerm = ownerNameInput.value.trim();
        
        if (searchTerm.length < 2) {
            ownerSuggestions.innerHTML = '';
            ownerSuggestions.classList.remove('show');
            return;
        }
        
        try {
            const owners = await apiService.getOwners(searchTerm);
            console.log('Owner search results:', owners);
            
            if (!owners || owners.length === 0) {
                ownerSuggestions.innerHTML = '';
                ownerSuggestions.classList.remove('show');
                return;
            }
            
            ownerSuggestions.innerHTML = '';
            
            owners.forEach(owner => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.textContent = owner.name;
                item.addEventListener('click', () => {
                    ownerNameInput.value = owner.name;
                    ownerAddressInput.value = owner.address || '';
                    ownerPhoneInput.value = owner.phone || '';
                    selectedOwnerId = owner.id;
                    ownerSuggestions.classList.remove('show');
                    
                    // Load pets for this owner
                    apiService.getPets(owner.id)
                        .then(pets => {
                            console.log('Pets for owner:', pets);
                            if (pets && pets.length > 0) {
                                showPetSuggestions(pets);
                            }
                        })
                        .catch(error => {
                            console.error('Error loading pets:', error);
                        });
                });
                
                ownerSuggestions.appendChild(item);
            });
            
            ownerSuggestions.classList.add('show');
        } catch (error) {
            console.error('Error searching owners:', error);
            showToast('Error searching for owners', 'error');
        }
    }
    
    // Pet search and suggestions
    async function handlePetSearch() {
        const searchTerm = petNameInput.value.trim();
        
        if (searchTerm.length < 2) {
            petSuggestions.innerHTML = '';
            petSuggestions.classList.remove('show');
            return;
        }
        
        try {
            // Only search for pets of the selected owner if available
            const pets = await apiService.getPets(selectedOwnerId, searchTerm);
            showPetSuggestions(pets);
        } catch (error) {
            console.error('Error searching pets:', error);
        }
    }
    
    // Show pet suggestions
    function showPetSuggestions(pets) {
        if (pets.length === 0) {
            petSuggestions.innerHTML = '';
            petSuggestions.classList.remove('show');
            return;
        }
        
        petSuggestions.innerHTML = '';
        
        pets.forEach(pet => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = pet.name;
            item.addEventListener('click', () => {
                petNameInput.value = pet.name;
                petSpeciesInput.value = pet.species || '';
                petBreedInput.value = pet.breed || '';
                petAgeInput.value = pet.age || '';
                petSexInput.value = pet.sex || '';
                selectedPetId = pet.id;
                petSuggestions.classList.remove('show');
                
                // Load pet history
                loadPetHistory(pet.id);
            });
            
            petSuggestions.appendChild(item);
        });
        
        petSuggestions.classList.add('show');
    }
    
    // Load pet history
    async function loadPetHistory(petId) {
        try {
            const visits = await apiService.getVisits(petId);
            
            if (visits.length === 0) {
                historyList.innerHTML = '<p class="no-history">No history available for this pet.</p>';
                return;
            }
            
            historyList.innerHTML = '';
            
            visits.forEach(visit => {
                const item = document.createElement('div');
                item.className = 'history-item';
                
                const header = document.createElement('div');
                header.className = 'history-date';
                header.textContent = visit.date;
                
                const content = document.createElement('div');
                content.className = 'history-content';
                
                if (visit.complaint) {
                    content.innerHTML += `<strong>Complaint:</strong> ${visit.complaint.substring(0, 100)}${visit.complaint.length > 100 ? '...' : ''}<br>`;
                }
                
                item.appendChild(header);
                item.appendChild(content);
                
                item.addEventListener('click', () => {
                    // Load visit data into form
                    complaintInput.value = visit.complaint || '';
                    examinationInput.value = visit.examination || '';
                    treatmentInput.value = visit.treatment || '';
                    testsInput.value = visit.tests || '';
                    
                    showToast('Previous visit data loaded');
                });
                
                historyList.appendChild(item);
            });
        } catch (error) {
            console.error('Error loading pet history:', error);
            historyList.innerHTML = '<p class="no-history">Failed to load history.</p>';
        }
    }
    
    // Species handling
    async function loadSpeciesList() {
        try {
            allSpecies = await apiService.getAllSpecies();
            console.log('Loaded species:', allSpecies);
            return allSpecies;
        } catch (error) {
            console.error('Error loading species list:', error);
            showToast('Failed to load species list', 'warning');
            return [];
        }
    }
    
    function handleSpeciesSearch() {
        const searchTerm = petSpeciesInput.value.trim().toLowerCase();
        
        if (searchTerm.length < 1) {
            speciesSuggestions.innerHTML = '';
            speciesSuggestions.classList.remove('show');
            return;
        }
        
        const filteredSpecies = allSpecies.filter(species => 
            species.name.toLowerCase().includes(searchTerm)
        );
        
        if (filteredSpecies.length === 0) {
            speciesSuggestions.innerHTML = '';
            speciesSuggestions.classList.remove('show');
            return;
        }
        
        speciesSuggestions.innerHTML = '';
        
        filteredSpecies.forEach(species => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = species.name;
            item.addEventListener('click', () => {
                petSpeciesInput.value = species.name;
                speciesSuggestions.classList.remove('show');
            });
            
            speciesSuggestions.appendChild(item);
        });
        
        speciesSuggestions.classList.add('show');
    }
    
    // Medications handling
    async function loadMedicationsList() {
        try {
            allMedications = await apiService.getMedications(null, 0, 1000);
            console.log('Loaded medications:', allMedications);
            return allMedications;
        } catch (error) {
            console.error('Error loading medications list:', error);
            showToast('Failed to load medications list', 'warning');
            return [];
        }
    }
    
    function handleMedicationSearch() {
        const searchTerm = medicationSearch.value.trim().toLowerCase();
        
        let filteredMedications = allMedications;
        
        if (searchTerm.length > 0) {
            filteredMedications = allMedications.filter(med => 
                med.name.toLowerCase().includes(searchTerm)
            );
        }
        
        renderMedicationsList(filteredMedications);
    }
    
    function renderMedicationsList(medications) {
        medicationsList.innerHTML = '';
        
        medications.forEach(med => {
            const item = document.createElement('div');
            item.className = 'medication-item';
            
            const nameElem = document.createElement('div');
            nameElem.className = 'medication-name';
            nameElem.textContent = med.name;
            
            const details = document.createElement('div');
            details.className = 'medication-details';
            details.textContent = `${med.description || ''} ${med.dosage ? '- ' + med.dosage : ''}`;
            
            item.appendChild(nameElem);
            item.appendChild(details);
            
            item.addEventListener('click', async () => {
                // Add medication to treatment
                const medicationText = `${med.name} ${med.dosage ? '(' + med.dosage + ')' : ''}`;
                
                if (treatmentInput.value) {
                    treatmentInput.value += '\n' + medicationText;
                } else {
                    treatmentInput.value = medicationText;
                }
                
                // Increment usage count
                try {
                    await apiService.incrementMedicationUsage(med.name);
                    
                    // Update local medication data
                    const medIndex = allMedications.findIndex(m => m.id === med.id);
                    if (medIndex !== -1) {
                        allMedications[medIndex].usage_count++;
                    }
                } catch (error) {
                    console.error('Error incrementing medication usage:', error);
                }
                
                // Close dialog
                closeAllDialogs();
            });
            
            medicationsList.appendChild(item);
        });
    }
    
    // Show medications dialog
    function showMedicationsDialog() {
        // Render all medications initially
        medicationSearch.value = '';
        renderMedicationsList(allMedications);
        
        // Show dialog
        medicationsDialog.classList.add('show');
        overlay.classList.add('show');
    }
    
    // Show settings dialog
    function showSettingsDialog() {
        // Load current settings
        saveFolderInput.value = configData.save_folder || '';
        
        // Show dialog
        settingsDialog.classList.add('show');
        overlay.classList.add('show');
    }
    
    // Show confirm dialog
    function showConfirmDialog(message, callback) {
        confirmMessage.textContent = message;
        confirmDialog._callback = callback;
        
        confirmDialog.classList.add('show');
        overlay.classList.add('show');
    }
    
    // Close all dialogs
    function closeAllDialogs() {
        medicationsDialog.classList.remove('show');
        settingsDialog.classList.remove('show');
        confirmDialog.classList.remove('show');
        overlay.classList.remove('show');
    }
    
    // Show toast notification
    function showToast(message, type = 'success') {
        toast.textContent = message;
        toast.className = 'toast';
        toast.classList.add(type);
        toast.classList.add('show');
        
        console.log(`Toast message (${type}):`, message);
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
    
    // Handle browse button click
    function handleBrowse() {
        // In a real desktop app, this would open a folder picker dialog
        // For now, let's prompt the user to enter a path
        const newPath = prompt("Enter the full path to your save folder:", saveFolderInput.value);
        
        if (newPath) {
            saveFolderInput.value = newPath;
        }
    }
    
    // Handle save settings
    async function handleSaveSettings() {
        const newSaveFolder = saveFolderInput.value.trim();
        
        if (!newSaveFolder) {
            showToast('Save folder cannot be empty', 'error');
            return;
        }
        
        try {
            const result = await apiService.updateConfig({
                save_folder: newSaveFolder
            });
            
            if (result.error) {
                showToast(`Error: ${result.error}`, 'error');
                return;
            }
            
            // Update local config
            configData = result.config;
            console.log('Updated config:', configData);
            
            showToast('Settings saved successfully!');
            closeAllDialogs();
        } catch (error) {
            console.error('Failed to save settings:', error);
            showToast('Failed to save settings', 'error');
        }
    }
    
    // Handle test PDF generation
    async function handleTestPdf() {
        try {
            showToast('Testing PDF generation...', 'info');
            
            const result = await apiService.testPdfGeneration();
            console.log('PDF test result:', result);
            
            if (result.status === 'success') {
                showToast('PDF generated successfully!');
                
                // Open the PDF
                if (result.pdf_path) {
                    let pdfUrl = result.pdf_path;
                    
                    // If the path doesn't start with the origin or a slash, add a slash
                    if (!pdfUrl.startsWith(window.location.origin) && !pdfUrl.startsWith('/')) {
                        pdfUrl = '/' + pdfUrl;
                    }
                    
                    // If the path doesn't include the origin, add it
                    if (!pdfUrl.startsWith(window.location.origin)) {
                        pdfUrl = window.location.origin + pdfUrl;
                    }
                    
                    console.log('Opening test PDF at:', pdfUrl);
                    window.open(pdfUrl, '_blank');
                }
            } else {
                showToast(`PDF generation failed: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Error testing PDF generation:', error);
            showToast('Failed to test PDF generation', 'error');
        }
    }
    
    // Save visit
    async function saveVisit(shouldPrint = false) {
        // Validate required fields
        if (!ownerNameInput.value.trim()) {
            showToast('Owner name is required', 'error');
            return;
        }
        
        if (!petNameInput.value.trim()) {
            showToast('Pet name is required', 'error');
            return;
        }
        
        // Prepare data
        const visitData = {
            owner_name: ownerNameInput.value.trim(),
            owner_address: ownerAddressInput.value.trim(),
            owner_phone: ownerPhoneInput.value.trim(),
            pet_name: petNameInput.value.trim(),
            pet_species: petSpeciesInput.value.trim(),
            pet_breed: petBreedInput.value.trim(),
            pet_age: petAgeInput.value.trim(),
            pet_sex: petSexInput.value,
            complaint: complaintInput.value.trim(),
            examination: examinationInput.value.trim(),
            treatment: treatmentInput.value.trim(),
            tests: testsInput.value.trim(),
            next_visit: nextVisitInput.value
        };
        
        console.log('Saving visit data:', visitData);
        
        try {
            const result = await apiService.saveCompleteVisit(visitData);
            console.log('Save result:', result);
            
            // Update selected IDs
            selectedOwnerId = result.owner_id;
            selectedPetId = result.pet_id;
            
            // Update pet history
            loadPetHistory(selectedPetId);
            
            showToast('Visit saved successfully');
            
            // Print if requested
            if (shouldPrint && result.pdf_path) {
                // Make sure the path is correctly formatted
                let pdfUrl = result.pdf_path;
                
                // If the path doesn't start with the origin or a slash, add a slash
                if (!pdfUrl.startsWith(window.location.origin) && !pdfUrl.startsWith('/')) {
                    pdfUrl = '/' + pdfUrl;
                }
                
                // If the path doesn't include the origin, add it
                if (!pdfUrl.startsWith(window.location.origin)) {
                    pdfUrl = window.location.origin + pdfUrl;
                }
                
                console.log('Opening PDF at:', pdfUrl);
                window.open(pdfUrl, '_blank');
            }
            
        } catch (error) {
            console.error('Error saving visit:', error);
            showToast('Failed to save visit. Please check console for details.', 'error');
        }
    }
    
    // Handle save button click
    function handleSave() {
        saveVisit(false);
    }
    
    // Handle save and print button click
    function handleSaveAndPrint() {
        saveVisit(true);
    }
    
    // Reset form
    function resetForm() {
        // Reset inputs
        ownerNameInput.value = '';
        ownerAddressInput.value = '';
        ownerPhoneInput.value = '';
        petNameInput.value = '';
        petSpeciesInput.value = '';
        petBreedInput.value = '';
        petAgeInput.value = '';
        petSexInput.value = '';
        complaintInput.value = '';
        examinationInput.value = '';
        treatmentInput.value = '';
        testsInput.value = '';
        
        // Set next visit to today
        const today = new Date().toISOString().split('T')[0];
        nextVisitInput.value = today;
        
        // Reset selected IDs
        selectedOwnerId = null;
        selectedPetId = null;
        
        // Reset history
        historyList.innerHTML = '<p class="no-history">No history available for this pet.</p>';
        
        // Hide all suggestions
        ownerSuggestions.innerHTML = '';
        ownerSuggestions.classList.remove('show');
        petSuggestions.innerHTML = '';
        petSuggestions.classList.remove('show');
        speciesSuggestions.innerHTML = '';
        speciesSuggestions.classList.remove('show');
    }
    
    // Utility: Debounce function
    function debounce(func, delay) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }
    
    // Load configuration
    async function loadConfig() {
        try {
            configData = await apiService.getConfig();
            console.log('Loaded config:', configData);
            
            // Update UI with config data
            if (configData.save_folder) {
                saveFolderInput.value = configData.save_folder;
            }
        } catch (error) {
            console.error('Failed to load configuration:', error);
            showToast('Failed to load application configuration', 'error');
        }
    }
    
    // Initialize app
    init();
}); 