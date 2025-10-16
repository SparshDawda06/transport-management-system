/**
 * Unified Relationship Logic for TMS Forms
 * Handles station-entity relationships with symbol-based filtering
 */

class TMSRelationshipManager {
  constructor() {
    this.consignorStationMap = {};
    this.consigneeStationMap = {};
    this.agentStationMap = {};
    this.vehicleData = {};
    this.relationshipsLoaded = false;
    this.manualStationSet = {
      from: false,
      to: false
    };
  }

  /**
   * Initialize relationship logic for a form
   * @param {Object} config - Configuration object
   * @param {string} config.formType - Type of form ('order', 'builty', 'entity')
   * @param {Object} config.selectors - DOM selectors for form elements
   */
  async initialize(config) {
    console.log(`Initializing relationship logic for ${config.formType} form`);
    
    // Load relationship data
    await this.loadRelationshipData();
    
    // Initialize based on form type
    switch (config.formType) {
      case 'order':
        this.initializeOrderForm(config.selectors);
        break;
      case 'builty':
        this.initializeBuiltyForm(config.selectors);
        break;
      case 'entity':
        this.initializeEntityForm(config.selectors);
        break;
      case 'fleet':
        this.initializeFleetForm(config.selectors);
        break;
    }
  }

  /**
   * Load all relationship data from API
   */
  async loadRelationshipData() {
    if (this.relationshipsLoaded) return;

    try {
      const [consignorsResponse, consigneesResponse, agentsResponse, vehiclesResponse] = await Promise.all([
        fetch('/api/consignors').then(r => r.json()),
        fetch('/api/consignees').then(r => r.json()),
        fetch('/api/booking_agents').then(r => r.json()),
        fetch('/api/vehicles').then(r => r.json())
      ]);

      // Populate station maps
      consignorsResponse.forEach(c => {
        this.consignorStationMap[c.id] = c.station_id;
      });

      consigneesResponse.forEach(c => {
        this.consigneeStationMap[c.id] = c.station_id;
      });

      agentsResponse.forEach(a => {
        this.agentStationMap[a.id] = a.station_id;
      });

      // Populate vehicle data
      vehiclesResponse.forEach(v => {
        this.vehicleData[v.id] = {
          owner_id: v.owner_id,
          driver_id: v.driver_id
        };
      });

      this.relationshipsLoaded = true;
      console.log('Relationship data loaded successfully:', {
        consignors: Object.keys(this.consignorStationMap).length,
        consignees: Object.keys(this.consigneeStationMap).length,
        agents: Object.keys(this.agentStationMap).length,
        vehicles: Object.keys(this.vehicleData).length
      });
    } catch (error) {
      console.error('Failed to load relationship data:', error);
    }
  }

  /**
   * Initialize order form relationships
   */
  initializeOrderForm(selectors) {
    const {
      fromStationSelect,
      toStationSelect,
      consignorSelect,
      consigneeSelect,
      agentSelect,
      fromStationAgentSelect,
      toStationAgentSelect
    } = selectors;

    // Consignor -> From Station relationship
    if (consignorSelect && fromStationSelect) {
      consignorSelect.addEventListener('change', () => {
        if (!this.manualStationSet.from && consignorSelect.value && consignorSelect.value !== '0') {
          const stationId = this.consignorStationMap[consignorSelect.value];
          if (stationId) {
            fromStationSelect.value = stationId;
            fromStationSelect.dispatchEvent(new Event('change'));
          }
        }
      });
    }

    // Consignee -> To Station relationship
    if (consigneeSelect && toStationSelect) {
      consigneeSelect.addEventListener('change', () => {
        if (!this.manualStationSet.to && consigneeSelect.value && consigneeSelect.value !== '0') {
          const stationId = this.consigneeStationMap[consigneeSelect.value];
          if (stationId) {
            toStationSelect.value = stationId;
            toStationSelect.dispatchEvent(new Event('change'));
          }
        }
      });
    }

    // Agent -> From Station relationship
    if (agentSelect && fromStationAgentSelect) {
      agentSelect.addEventListener('change', () => {
        if (!this.manualStationSet.from && agentSelect.value && agentSelect.value !== '0') {
          const stationId = this.agentStationMap[agentSelect.value];
          if (stationId) {
            fromStationAgentSelect.value = stationId;
            fromStationAgentSelect.dispatchEvent(new Event('change'));
          }
        }
      });
    }

    // Station change handlers
    if (fromStationSelect) {
      fromStationSelect.addEventListener('change', () => {
        this.manualStationSet.from = true;
        if (fromStationSelect.value && fromStationSelect.value !== '0') {
          this.sortOptionsByStation(consignorSelect, fromStationSelect.value, this.consignorStationMap);
          this.sortOptionsByStation(agentSelect, fromStationSelect.value, this.agentStationMap);
          
          // Sync with agent mode
          if (fromStationAgentSelect) {
            fromStationAgentSelect.value = fromStationSelect.value;
          }
        }
      });
    }

    if (toStationSelect) {
      toStationSelect.addEventListener('change', () => {
        this.manualStationSet.to = true;
        if (toStationSelect.value && toStationSelect.value !== '0') {
          this.sortOptionsByStation(consigneeSelect, toStationSelect.value, this.consigneeStationMap);
          
          // Sync with agent mode
          if (toStationAgentSelect) {
            toStationAgentSelect.value = toStationSelect.value;
          }
        }
      });
    }
  }

  /**
   * Initialize builty form relationships
   */
  initializeBuiltyForm(selectors) {
    const {
      fromStationSelect,
      toStationSelect,
      consignorSelect,
      consigneeSelect,
      agentSelect,
      vehicleSelect,
      driverSelect,
      ownerSelect
    } = selectors;

    // Station-entity relationships
    if (consignorSelect && fromStationSelect) {
      consignorSelect.addEventListener('change', () => {
        if (consignorSelect.value && consignorSelect.value !== '0') {
          const stationId = this.consignorStationMap[consignorSelect.value];
          if (stationId) {
            fromStationSelect.value = stationId;
            this.sortOptionsByStation(consignorSelect, stationId, this.consignorStationMap);
          }
        }
      });
    }

    if (consigneeSelect && toStationSelect) {
      consigneeSelect.addEventListener('change', () => {
        if (consigneeSelect.value && consigneeSelect.value !== '0') {
          const stationId = this.consigneeStationMap[consigneeSelect.value];
          if (stationId) {
            toStationSelect.value = stationId;
            this.sortOptionsByStation(consigneeSelect, stationId, this.consigneeStationMap);
          }
        }
      });
    }

    if (agentSelect && fromStationSelect) {
      agentSelect.addEventListener('change', () => {
        if (agentSelect.value && agentSelect.value !== '0') {
          const stationId = this.agentStationMap[agentSelect.value];
          if (stationId) {
            fromStationSelect.value = stationId;
            this.sortOptionsByStation(agentSelect, stationId, this.agentStationMap);
          }
        }
      });
    }

    // Vehicle-driver-owner relationships
    if (vehicleSelect && driverSelect && ownerSelect) {
      // Vehicle change handler
      vehicleSelect.addEventListener('change', () => {
        const vehicleId = vehicleSelect.value;
        if (vehicleId && vehicleId !== '0') {
          const vehicleData = this.vehicleData[vehicleId];
          if (vehicleData) {
            if (vehicleData.owner_id && !this.manualStationSet.owner) {
              ownerSelect.value = vehicleData.owner_id;
            }
            if (vehicleData.driver_id && !this.manualStationSet.driver) {
              driverSelect.value = vehicleData.driver_id;
            }
          }
        }
      });

      // Owner change handler
      ownerSelect.addEventListener('change', () => {
        this.manualStationSet.owner = true;
        if (ownerSelect.value && ownerSelect.value !== '0') {
          this.sortOptionsByOwner(vehicleSelect, ownerSelect.value);
        }
      });

      // Driver change handler
      driverSelect.addEventListener('change', () => {
        this.manualStationSet.driver = true;
        if (driverSelect.value && driverSelect.value !== '0') {
          this.sortOptionsByDriver(vehicleSelect, driverSelect.value);
        }
      });
    }
  }

  /**
   * Initialize entity form relationships
   */
  initializeEntityForm(selectors) {
    const { stationSelect, pinCodeSelect } = selectors;

    if (stationSelect && pinCodeSelect) {
      stationSelect.addEventListener('change', () => {
        if (stationSelect.value && stationSelect.value !== '0') {
          this.sortOptionsByStation(pinCodeSelect, stationSelect.value, this.pinCodeStationMap);
        }
      });
    }
  }

  /**
   * Initialize fleet form relationships
   */
  initializeFleetForm(selectors) {
    const { vehicleSelect, driverSelect, ownerSelect } = selectors;

    if (vehicleSelect && driverSelect && ownerSelect) {
      // Vehicle change handler
      vehicleSelect.addEventListener('change', () => {
        const vehicleId = vehicleSelect.value;
        if (vehicleId && vehicleId !== '0') {
          const vehicleData = this.vehicleData[vehicleId];
          if (vehicleData) {
            if (vehicleData.owner_id) {
              ownerSelect.value = vehicleData.owner_id;
            }
            if (vehicleData.driver_id) {
              driverSelect.value = vehicleData.driver_id;
            }
          }
        }
      });
    }
  }

  /**
   * Sort options by station with symbol highlighting
   */
  sortOptionsByStation(select, stationId, stationMap) {
    if (!select || !stationId || !this.relationshipsLoaded) return;

    const currentValue = select.value;
    const options = Array.from(select.options);
    const firstOption = options.shift();

    let matchingCount = 0;
    let nonMatchingCount = 0;

    // Sort options
    options.sort((a, b) => {
      const aStation = stationMap[a.value];
      const bStation = stationMap[b.value];

      const aMatches = aStation == stationId;
      const bMatches = bStation == stationId;

      if (aMatches) matchingCount++;
      else nonMatchingCount++;

      if (aMatches && !bMatches) return -1;
      if (!aMatches && bMatches) return 1;
      return a.text.replace('★ ', '').localeCompare(b.text.replace('★ ', ''));
    });

    // Clear and rebuild select
    select.innerHTML = '';
    select.appendChild(firstOption);

    options.forEach(opt => {
      const optStation = stationMap[opt.value];
      const matches = optStation == stationId;

      if (matches) {
        opt.text = '★ ' + opt.text.replace('★ ', '');
        opt.style.backgroundColor = '#fef3c7';
        opt.title = `Matches station ${stationId}`;
      } else {
        opt.text = opt.text.replace('★ ', '');
        opt.style.backgroundColor = '';
        opt.title = `Station: ${optStation || 'Unknown'}`;
      }

      select.appendChild(opt);
    });

    if (currentValue) select.value = currentValue;
  }

  /**
   * Sort options by owner with symbol highlighting
   */
  sortOptionsByOwner(select, ownerId) {
    if (!select || !ownerId) return;

    const currentValue = select.value;
    const options = Array.from(select.options);
    const firstOption = options.shift();

    options.forEach(opt => {
      if (opt.value === '0') return;
      const vehicleData = this.vehicleData[opt.value];
      if (vehicleData && vehicleData.owner_id == ownerId) {
        opt.text = '★ ' + opt.text.replace('★ ', '');
        opt.style.backgroundColor = '#fef3c7';
      } else {
        opt.text = opt.text.replace('★ ', '');
        opt.style.backgroundColor = '';
      }
    });

    // Re-sort options
    const sortedOptions = options.sort((a, b) => {
      const aMatch = a.text.startsWith('★');
      const bMatch = b.text.startsWith('★');
      if (aMatch && !bMatch) return -1;
      if (!aMatch && bMatch) return 1;
      return a.text.localeCompare(b.text);
    });

    select.innerHTML = '';
    select.appendChild(firstOption);
    sortedOptions.forEach(opt => select.appendChild(opt));

    if (currentValue) select.value = currentValue;
  }

  /**
   * Sort options by driver with symbol highlighting
   */
  sortOptionsByDriver(select, driverId) {
    if (!select || !driverId) return;

    const currentValue = select.value;
    const options = Array.from(select.options);
    const firstOption = options.shift();

    options.forEach(opt => {
      if (opt.value === '0') return;
      const vehicleData = this.vehicleData[opt.value];
      if (vehicleData && vehicleData.driver_id == driverId) {
        opt.text = '★ ' + opt.text.replace('★ ', '');
        opt.style.backgroundColor = '#fef3c7';
      } else {
        opt.text = opt.text.replace('★ ', '');
        opt.style.backgroundColor = '';
      }
    });

    // Re-sort options
    const sortedOptions = options.sort((a, b) => {
      const aMatch = a.text.startsWith('★');
      const bMatch = b.text.startsWith('★');
      if (aMatch && !bMatch) return -1;
      if (!aMatch && bMatch) return 1;
      return a.text.localeCompare(b.text);
    });

    select.innerHTML = '';
    select.appendChild(firstOption);
    sortedOptions.forEach(opt => select.appendChild(opt));

    if (currentValue) select.value = currentValue;
  }

  /**
   * Reset manual station flags
   */
  resetManualFlags() {
    this.manualStationSet.from = false;
    this.manualStationSet.to = false;
    this.manualStationSet.owner = false;
    this.manualStationSet.driver = false;
  }
}

// Global instance
window.TMSRelationshipManager = new TMSRelationshipManager();

// Auto-initialize for common forms
document.addEventListener('DOMContentLoaded', function() {
  // Auto-detect form type and initialize
  const form = document.querySelector('form');
  if (!form) return;

  const formId = form.id;
  let config = null;

  if (formId === 'orderForm') {
    config = {
      formType: 'order',
      selectors: {
        fromStationSelect: document.getElementById('from_station_id'),
        toStationSelect: document.getElementById('to_station_id'),
        consignorSelect: document.getElementById('consignor_id'),
        consigneeSelect: document.getElementById('consignee_id'),
        agentSelect: document.getElementById('booking_agent_id'),
        fromStationAgentSelect: document.getElementById('from_station_id_agent'),
        toStationAgentSelect: document.getElementById('to_station_id_agent')
      }
    };
  } else if (formId === 'builtyForm') {
    config = {
      formType: 'builty',
      selectors: {
        fromStationSelect: document.getElementById('from_station_id'),
        toStationSelect: document.getElementById('to_station_id'),
        consignorSelect: document.getElementById('builty_consignor_id'),
        consigneeSelect: document.getElementById('builty_consignee_id'),
        agentSelect: document.getElementById('builty_booking_agent_id'),
        vehicleSelect: document.getElementById('vehicle_id'),
        driverSelect: document.getElementById('driver_id'),
        ownerSelect: document.getElementById('owner_id')
      }
    };
  }

  if (config) {
    window.TMSRelationshipManager.initialize(config);
  }
});
