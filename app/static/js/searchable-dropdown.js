// Searchable Dropdown Component
class SearchableDropdown {
  constructor(selectElement, options = {}) {
    this.originalSelect = selectElement;
    this.options = {
      placeholder: '',
      noResultsText: 'No results found',
      searchThreshold: 1,
      ...options
    };
    
    this.init();
  }
  
  init() {
    // Create wrapper
    this.wrapper = document.createElement('div');
    this.wrapper.className = 'searchable-dropdown-wrapper';
    this.wrapper.style.position = 'relative';
    this.wrapper.style.display = 'inline-block';
    this.wrapper.style.width = '100%';
    
    // Create search input (styled like a select)
    this.searchInput = document.createElement('input');
    this.searchInput.type = 'text';
    this.searchInput.className = 'searchable-dropdown-input';
    this.searchInput.style.cssText = `
      width: 100%;
      padding: 8px 32px 8px 12px;
      border: 1px solid var(--border, #ddd);
      border-radius: 6px;
      font-size: 14px;
      background: white;
      box-sizing: border-box;
      cursor: pointer;
      color: #333;
    `;
    
    // Add dropdown arrow
    const arrow = document.createElement('div');
    arrow.innerHTML = '▼';
    arrow.style.cssText = `
      position: absolute;
      right: 8px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      color: #666;
      font-size: 12px;
    `;
    this.wrapper.appendChild(arrow);
    
    // Create dropdown
    this.dropdown = document.createElement('div');
    this.dropdown.className = 'searchable-dropdown-list';
    this.dropdown.style.cssText = `
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      border: 1px solid var(--border, #ddd);
      border-top: none;
      border-radius: 0 0 6px 6px;
      max-height: 200px;
      overflow-y: auto;
      z-index: 1000;
      display: none;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    
    // Create hidden input for form submission
    this.hiddenInput = document.createElement('input');
    this.hiddenInput.type = 'hidden';
    this.hiddenInput.name = this.originalSelect.name;
    this.hiddenInput.value = this.originalSelect.value;
    
    // Insert wrapper before original select
    this.originalSelect.parentNode.insertBefore(this.wrapper, this.originalSelect);
    this.originalSelect.style.display = 'none';
    
    // Add elements to wrapper
    this.wrapper.appendChild(this.searchInput);
    this.wrapper.appendChild(this.dropdown);
    this.wrapper.appendChild(this.hiddenInput);
    
    // Load initial options
    this.loadOptions();
    
    // Add event listeners
    this.addEventListeners();
    
    // Set initial value
    this.setInitialValue();
  }
  
  loadOptions() {
    this.optionsList = [];
    Array.from(this.originalSelect.options).forEach(option => {
      if (option.value !== '') {
        this.optionsList.push({
          value: option.value,
          text: option.textContent,
          element: option
        });
      }
    });
  }
  
  addEventListeners() {
    let isSearching = false;
    let originalValue = '';
    
    // Click to show all options (browse mode)
    this.searchInput.addEventListener('click', (e) => {
      e.preventDefault();
      if (!isSearching) {
        this.showAllOptions();
      }
    });
    
    // Focus to show all options
    this.searchInput.addEventListener('focus', () => {
      originalValue = this.searchInput.value;
      if (!isSearching) {
        this.showAllOptions();
      }
    });
    
    // Search input events - only when actively typing
    this.searchInput.addEventListener('input', (e) => {
      const query = e.target.value;
      
      if (query.length > 0 && query !== originalValue) {
        isSearching = true;
        this.handleSearch(query);
      } else if (query.length === 0) {
        isSearching = false;
        this.showAllOptions();
      }
    });
    
    // Handle keyboard navigation
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.hideDropdown();
        this.searchInput.blur();
        this.searchInput.value = originalValue;
        isSearching = false;
      }
    });
    
    // Handle blur - restore original value if no selection made
    this.searchInput.addEventListener('blur', (e) => {
      setTimeout(() => {
        if (!this.dropdown.contains(document.activeElement)) {
          this.hideDropdown();
          // If no option was selected and we were searching, restore original value
          if (isSearching && this.searchInput.value !== this.hiddenInput.value) {
            this.restoreOriginalValue();
          }
          isSearching = false;
        }
      }, 150);
    });
    
    // Click outside to close
    document.addEventListener('click', (e) => {
      if (!this.wrapper.contains(e.target)) {
        this.hideDropdown();
        if (isSearching) {
          this.restoreOriginalValue();
        }
        isSearching = false;
      }
    });
  }
  
  showAllOptions() {
    // Clear dropdown
    this.dropdown.innerHTML = '';
    
    // Show all options
    this.optionsList.forEach(option => {
      const item = document.createElement('div');
      item.className = 'searchable-dropdown-item';
      item.textContent = option.text;
      item.style.cssText = `
        padding: 8px 12px;
        cursor: pointer;
        border-bottom: 1px solid #f0f0f0;
      `;
      
      // Hover effects
      item.addEventListener('mouseenter', () => {
        item.style.backgroundColor = '#f5f5f5';
      });
      
      item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = 'white';
      });
      
      // Click handler
      item.addEventListener('mousedown', (e) => {
        e.preventDefault();
        this.selectOption(option);
      });
      
      this.dropdown.appendChild(item);
    });
    
    this.showDropdown();
  }
  
  handleSearch(query) {
    const searchTerm = query.toLowerCase().trim();
    
    // Clear dropdown
    this.dropdown.innerHTML = '';
    
    if (searchTerm.length < this.options.searchThreshold) {
      this.showAllOptions();
      return;
    }
    
    // Filter options
    const filteredOptions = this.optionsList.filter(option =>
      option.text.toLowerCase().includes(searchTerm)
    );
    
    if (filteredOptions.length === 0) {
      const noResults = document.createElement('div');
      noResults.className = 'searchable-dropdown-no-results';
      noResults.textContent = this.options.noResultsText;
      noResults.style.cssText = `
        padding: 8px 12px;
        color: #666;
        font-style: italic;
      `;
      this.dropdown.appendChild(noResults);
    } else {
      filteredOptions.forEach(option => {
        const item = document.createElement('div');
        item.className = 'searchable-dropdown-item';
        item.textContent = option.text;
        item.style.cssText = `
          padding: 8px 12px;
          cursor: pointer;
          border-bottom: 1px solid #f0f0f0;
        `;
        
        // Hover effects
        item.addEventListener('mouseenter', () => {
          item.style.backgroundColor = '#f5f5f5';
        });
        
        item.addEventListener('mouseleave', () => {
          item.style.backgroundColor = 'white';
        });
        
        // Click handler
        item.addEventListener('mousedown', (e) => {
          e.preventDefault();
          this.selectOption(option);
        });
        
        this.dropdown.appendChild(item);
      });
    }
    
    this.showDropdown();
  }
  
  selectOption(option) {
    // Update hidden input
    this.hiddenInput.value = option.value;
    
    // Update original select
    this.originalSelect.value = option.value;
    
    // Update search input
    this.searchInput.value = option.text;
    
    // Hide dropdown
    this.hideDropdown();
    
    // Trigger change event to maintain automatic filtering
    const changeEvent = new Event('change', { bubbles: true });
    this.originalSelect.dispatchEvent(changeEvent);
    
    // Also trigger input event to maintain any input-based filtering
    const inputEvent = new Event('input', { bubbles: true });
    this.originalSelect.dispatchEvent(inputEvent);
  }
  
  restoreOriginalValue() {
    const selectedOption = this.originalSelect.options[this.originalSelect.selectedIndex];
    if (selectedOption && selectedOption.value !== '') {
      this.searchInput.value = selectedOption.textContent;
    } else {
      this.searchInput.value = '';
    }
  }
  
  showDropdown() {
    this.dropdown.style.display = 'block';
  }
  
  hideDropdown() {
    this.dropdown.style.display = 'none';
  }
  
  setInitialValue() {
    const selectedOption = this.originalSelect.options[this.originalSelect.selectedIndex];
    if (selectedOption && selectedOption.value !== '') {
      this.searchInput.value = selectedOption.textContent;
      this.hiddenInput.value = selectedOption.value;
    } else {
      // Set placeholder text only when no value is selected
      this.searchInput.placeholder = 'Select...';
    }
  }
  
  getValue() {
    return this.hiddenInput.value;
  }
  
  setValue(value) {
    const option = this.optionsList.find(opt => opt.value === value);
    if (option) {
      this.selectOption(option);
    }
  }
}

// Initialize all searchable dropdowns
function initializeSearchableDropdowns() {
  // Temporarily disable searchable dropdowns to preserve automatic filtering
  // Only apply to firm dropdown which doesn't have automatic filtering
  const searchableSelects = document.querySelectorAll('select[id="firm"]');
  
  searchableSelects.forEach(select => {
    if (!select.hasAttribute('data-searchable-initialized')) {
      new SearchableDropdown(select);
      select.setAttribute('data-searchable-initialized', 'true');
    }
  });
}

// Make it available globally
window.SearchableDropdown = SearchableDropdown;
window.initializeSearchableDropdowns = initializeSearchableDropdowns;
