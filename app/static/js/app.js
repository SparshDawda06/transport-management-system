window.TMS = window.TMS || {};

TMS.fetchJSON = async function(url, options={}){
  const res = await fetch(url, Object.assign({headers: {"X-Requested-With":"XMLHttpRequest"}}, options));
  if(!res.ok){
    const text = await res.text();
    throw new Error(text || ("HTTP " + res.status));
  }
  const ct = res.headers.get("content-type") || "";
  if(ct.includes("application/json")) return res.json();
  return res.text();
};

TMS.toggleSidebar = function(){
  var sidebar = document.getElementById('sidebar');
  if(!sidebar) return;
  
  sidebar.classList.toggle('open');
};

// Navigation scroll behavior (InquisiCon style)
TMS.initNavbar = function() {
  let lastScrollTop = 0;
  let scrollTimeout;
  const navbar = document.getElementById('navbar');
  let ticking = false;

  function updateNavbar() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Add scrolled class for background change
    if (scrollTop > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Hide/Show logic
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      navbar.classList.add('hidden');
      navbar.classList.remove('visible');
    } else {
      // Scrolling up
      navbar.classList.remove('hidden');
      navbar.classList.add('visible');
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }

  function handleScroll() {
    if (!ticking) {
      requestAnimationFrame(updateNavbar);
      ticking = true;
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });

  // Mobile menu functionality
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navMenu = document.querySelector('.nav-menu');

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      mobileMenuBtn.classList.toggle('active');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!mobileMenuBtn.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
      }
    });

    // Close mobile menu when clicking on a link
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
      });
    });
  }
};

// Inline panel stack
TMS._inline = { open: false, panels: [] };

TMS._ensureModal = function(){
  let modal = document.getElementById('inline-modal');
  if(!modal){
    const m = document.createElement('div');
    m.id = 'inline-modal';
    m.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);align-items:center;justify-content:center;';
    const wrap = document.createElement('div');
    wrap.id = 'inline-wrap';
    wrap.style.cssText = 'background:#fff;padding:16px;border-radius:10px;max-width:95vw;max-height:90vh;overflow:auto;display:flex;gap:12px;';
    m.appendChild(wrap);
    document.body.appendChild(m);
  }
  return document.getElementById('inline-modal');
};

TMS.closeInline = function(){
  const modal = document.getElementById('inline-modal');
  if(modal){ modal.style.display = 'none'; }
  TMS._inline.open = false;
  TMS._inline.panels = [];
  const wrap = document.getElementById('inline-wrap');
  if(wrap){ wrap.innerHTML = ''; }
};

TMS.openInline = async function(entity, ctx={}){
  // Close all open dropdowns before opening new modal
  document.querySelectorAll('.cs-menu').forEach(menu => {
    menu.style.display = 'none';
  });
  
  const modal = TMS._ensureModal();
  const wrap = document.getElementById('inline-wrap');
  modal.style.display = 'flex';
  TMS._inline.open = true;

  const params = new URLSearchParams();
  Object.entries(ctx || {}).forEach(([k,v])=>{ if(v!=null && v!==''){ params.set(k, v); } });
  const url = `/api/${entity}/new` + (params.toString() ? `?${params}` : '');
  const html = await TMS.fetchJSON(url);

  const panel = document.createElement('div');
  panel.className = 'inline-panel';
  panel.style.cssText = 'min-width:320px;max-width:420px;border:1px solid #e5e7eb;border-radius:10px;padding:12px;flex:0 0 auto;';
  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      <strong style="font-size:14px;">Add ${entity.replace('_',' ').replace(/\b\w/g, c=>c.toUpperCase())}</strong>
      <div style="display:flex;gap:6px;align-items:center;">
        <button class="btn small secondary" type="button">Close</button>
      </div>
    </div>
    <div class="inline-body">${html}</div>
  `;
  panel.querySelector('button').addEventListener('click', ()=>{
    wrap.removeChild(panel);
    TMS._inline.panels.pop();
    if(TMS._inline.panels.length === 0){ TMS.closeInline(); }
  });
  wrap.appendChild(panel);
  TMS._inline.panels.push(panel);

  const form = panel.querySelector('form');
  if(form){
    // populate dynamic selects from data-populate-source (for nested quick adds)
    form.querySelectorAll('select[data-populate-source]').forEach(async (sel)=>{
      const src = sel.getAttribute('data-populate-source');
      const url = new URL(src, window.location.origin);
      const stateEl = form.querySelector('[name="state"]');
      if(entity === 'stations' && stateEl && stateEl.value){
        url.searchParams.set('state', stateEl.value);
      }
      const items = await TMS.fetchJSON(url.pathname + url.search);
      sel.innerHTML = '<option value="">Select...</option>';
      items.forEach(o=>{ const opt=document.createElement('option'); opt.value=o.id; opt.textContent=o.label; sel.appendChild(opt); });
    });

    form.addEventListener('submit', async function(ev){
      ev.preventDefault();
      const fd = new FormData(form);
      try{
        const res = await fetch(`/api/${entity}`, { method: 'POST', body: fd });
        if(!res.ok){ throw new Error(await res.text()); }
        const data = await res.json();
        
        // Update parent form's dropdown if this was a nested add
        if(entity === 'stations'){
          // Find all station selects in parent forms and refresh them
          document.querySelectorAll('select[data-populate-source="/api/stations"]').forEach(sel => {
            const form = sel.closest('form');
            const stateEl = form && form.querySelector('[name="state"]');
            if(stateEl && stateEl.value){
              const url = new URL('/api/stations', window.location.origin);
              url.searchParams.set('state', stateEl.value);
              TMS.fetchJSON(url.pathname + url.search).then(items => {
                const currentVal = sel.value;
                sel.innerHTML = '<option value="">Select...</option>';
                items.forEach(o=>{ 
                  const opt=document.createElement('option'); 
                  opt.value=o.id; 
                  opt.textContent=o.label; 
                  if(o.id == data.id) opt.selected = true;
                  sel.appendChild(opt); 
                });
                if(currentVal) sel.value = currentVal;
              });
            }
          });
        }
        
        if(typeof TMS.inlineSaved === 'function'){
          TMS.inlineSaved(entity, data.id, data.label);
        }
        wrap.removeChild(panel);
        TMS._inline.panels.pop();
        if(TMS._inline.panels.length === 0){ TMS.closeInline(); }
      }catch(e){ alert(e.message || 'Failed to save'); }
    });

    form.querySelectorAll('[data-quick-add]').forEach(btn => {
      btn.addEventListener('click', function(){
        const target = btn.getAttribute('data-quick-add');
        const stateEl = form.querySelector('[name="state"]');
        const ctx2 = {};
        if(stateEl && stateEl.value){ ctx2.state = stateEl.value; }
        TMS.openInline(target, ctx2);
      });
    });

    // Handle state change to refresh station dropdown
    const stateEl = form.querySelector('[name="state"]');
    if(stateEl){
      stateEl.addEventListener('change', function(){
        const stationSelect = form.querySelector('select[data-populate-source="/api/stations"]');
        if(stationSelect){
          const url = new URL('/api/stations', window.location.origin);
          url.searchParams.set('state', this.value);
          TMS.fetchJSON(url.pathname + url.search).then(items => {
            stationSelect.innerHTML = '<option value="">Select...</option>';
            items.forEach(o=>{ 
              const opt=document.createElement('option'); 
              opt.value=o.id; 
              opt.textContent=o.label; 
              stationSelect.appendChild(opt); 
            });
          });
        }
      });
    }
  }
};

// Custom searchable dropdown
TMS.CustomSelect = function(config){
  const { mount, source, placeholder, value, onChange, extraParams } = config;
  const root = document.createElement('div');
  root.className = 'custom-select';
  root.innerHTML = `
    <div class="cs-control"><span class="cs-label">${placeholder||'Select'}</span><span class="cs-value"></span><span class="cs-chevron">▾</span></div>
    <div class="cs-menu" style="display:none;">
      <div class="cs-search"><input type="text" placeholder="Search..." /></div>
      <div class="cs-list"></div>
    </div>`;
  mount.innerHTML = '';
  mount.appendChild(root);
  const control = root.querySelector('.cs-control');
  const menu = root.querySelector('.cs-menu');
  const list = root.querySelector('.cs-list');
  const search = root.querySelector('input');
  const valSpan = root.querySelector('.cs-value');

  let current = null;
  function setValue(item){
    current = item;
    valSpan.textContent = item ? item.label : '';
    if(onChange) onChange(item);
  }

  async function load(q){
    const url = new URL(source, window.location.origin);
    if(q) url.searchParams.set('q', q);
    if(extraParams){ Object.entries(extraParams).forEach(([k,v])=>{ if(v) url.searchParams.set(k, v); }); }
    const items = await TMS.fetchJSON(url.pathname + url.search);
    list.innerHTML = '';
    items.forEach(it => {
      const opt = document.createElement('div');
      opt.className = 'cs-option';
      opt.textContent = it.label;
      opt.dataset.id = it.id;
      opt.addEventListener('click', ()=>{ setValue(it); menu.style.display='none'; });
      list.appendChild(opt);
    });
  }

  control.addEventListener('click', async ()=>{
    // Close other dropdowns first
    document.querySelectorAll('.cs-menu').forEach(otherMenu => {
      if(otherMenu !== menu) otherMenu.style.display = 'none';
    });
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    if(menu.style.display === 'block') await load('');
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!root.contains(e.target)) {
      menu.style.display = 'none';
    }
  });
  
  search.addEventListener('input', ()=>{ load(search.value); });

  return { setExtraParams(p){ if(p) config.extraParams = p; }, get value(){ return current; }, set value(v){ setValue(v); } };
};

// Open select-only panel via Search button
TMS.openSearchPanel = async function(entity, ctx={}){
  const modal = TMS._ensureModal();
  const wrap = document.getElementById('inline-wrap');
  modal.style.display = 'flex';
  const panel = document.createElement('div');
  panel.className = 'inline-panel';
  panel.style.cssText = 'min-width:320px;max-width:420px;border:1px solid #e5e7eb;border-radius:10px;padding:12px;flex:0 0 auto;';
  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      <strong style="font-size:14px;">Search ${entity}</strong>
      <button class="btn small secondary" type="button">Close</button>
    </div>
    <div>
      <div id="cs-mount"></div>
      <div style="margin-top:10px;display:flex;gap:8px;">
        <button class="btn" type="button" id="use-selected">Use Selected</button>
        <button class="btn secondary" type="button" id="add-new">Add New</button>
      </div>
    </div>`;
  panel.querySelector('button').addEventListener('click', ()=>{
    wrap.removeChild(panel);
    if(wrap.children.length === 0) TMS.closeInline();
  });
  wrap.appendChild(panel);

  const mount = panel.querySelector('#cs-mount');
  const cs = TMS.CustomSelect({ mount, source: `/api/${entity}`, placeholder: 'Search...', extraParams: ctx });
  panel.querySelector('#use-selected').addEventListener('click', ()=>{
    const sel = cs.value;
    if(sel && typeof TMS.inlineSaved === 'function'){
      TMS.inlineSaved(entity, sel.id, sel.label);
      wrap.removeChild(panel);
      if(wrap.children.length === 0) TMS.closeInline();
    }
  });
  panel.querySelector('#add-new').addEventListener('click', ()=>{
    TMS.openInline(entity, ctx);
  });
};

// Standard navigation handling (PJAX removed)
TMS.pjax = function(){
  // PJAX functionality removed - using standard navigation
  console.log('PJAX disabled - using standard navigation');
};

TMS.enhanceSelects = function(context){
  const root = context || document;
  root.querySelectorAll('select[data-entity]').forEach(sel => {
    // hide native select and mount custom
    if(sel.dataset.enhanced === '1') return;
    const entity = sel.getAttribute('data-entity');
    sel.style.display = 'none';
    sel.dataset.enhanced = '1';
    const mount = document.createElement('div');
    sel.parentNode.insertBefore(mount, sel.nextSibling);
    const getExtra = ()=>{
      // if entity is stations, try to pick state from sibling input/select named 'state'
      const form = sel.closest('form');
      const stateEl = form && form.querySelector('[name="state"]');
      return entity === 'stations' && stateEl && stateEl.value ? { state: stateEl.value } : {};
    };
    const cs = TMS.CustomSelect({ mount, source: `/api/${entity}`, placeholder: sel.getAttribute('data-placeholder')||'Select', extraParams: getExtra(), onChange: (item)=>{ sel.value = item ? item.id : ''; } });
    // keep station list filtered when state changes
    const form = sel.closest('form');
    if(form){
      form.querySelectorAll('[name="state"]').forEach(s => s.addEventListener('change', ()=>{ cs.setExtraParams(getExtra()); }));
    }
  });

  // attach search buttons
  root.querySelectorAll('button[data-search-entity]').forEach(btn => {
    if(btn.dataset.bound==='1') return;
    btn.dataset.bound='1';
    btn.addEventListener('click', ()=>{
      const entity = btn.getAttribute('data-search-entity');
      const form = btn.closest('form');
      const ctx = {};
      const stateEl = form && form.querySelector('[name="state"]');
      if(stateEl && stateEl.value) ctx.state = stateEl.value;
      TMS.openSearchPanel(entity, ctx);
    });
  });
};

// Auto-populate pin codes when station is selected
TMS.enhanceStationFields = function(context){
  const root = context || document;
  root.querySelectorAll('select[name="station_id"]').forEach(stationSelect => {
    if(stationSelect.dataset.enhanced === '1') return;
    stationSelect.dataset.enhanced = '1';
    
    stationSelect.addEventListener('change', function(){
      const form = this.closest('form');
      if(!form) return;
      
      const pinCodeSelect = form.querySelector('select[name="pin_code_id"]');
      
      if(!pinCodeSelect) return;
      
      const stationId = this.value;
      if(!stationId || stationId === '0') {
        // Clear pin code options if no station selected
        pinCodeSelect.innerHTML = '<option value="">Select Pin Code</option>';
        return;
      }
      
      // Fetch pin codes for the selected station
      fetch(`/api/pin_codes?station_id=${stationId}`)
        .then(response => response.json())
        .then(data => {
          pinCodeSelect.innerHTML = '<option value="">Select Pin Code</option>';
          data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.label;
            pinCodeSelect.appendChild(option);
          });
        })
        .catch(error => console.log('Error fetching pin codes:', error));
    });
  });
};

// Form validation helper
TMS.validateForm = function(form) {
  const errors = [];
  const requiredFields = form.querySelectorAll('[required]');
  
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      errors.push(`${field.labels[0]?.textContent || field.name} is required`);
      field.classList.add('error');
    } else {
      field.classList.remove('error');
    }
  });
  
  // Email validation
  const emailFields = form.querySelectorAll('input[type="email"]');
  emailFields.forEach(field => {
    if (field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
      errors.push(`${field.labels[0]?.textContent || field.name} must be a valid email`);
      field.classList.add('error');
    }
  });
  
  // Phone validation
  const phoneFields = form.querySelectorAll('input[type="tel"], input[name*="phone"]');
  phoneFields.forEach(field => {
    if (field.value && !/^[\d\s\-\+\(\)]+$/.test(field.value)) {
      errors.push(`${field.labels[0]?.textContent || field.name} must be a valid phone number`);
      field.classList.add('error');
    }
  });
  
  // Number validation
  const numberFields = form.querySelectorAll('input[type="number"]');
  numberFields.forEach(field => {
    if (field.value && isNaN(field.value)) {
      errors.push(`${field.labels[0]?.textContent || field.name} must be a valid number`);
      field.classList.add('error');
    }
  });
  
  return errors;
};

// Enhanced form submission handling with AJAX support
TMS.handleFormSubmission = function(form) {
  if (!form) return;
  
  // Check if form already has event listener attached
  if (form.getAttribute('data-tms-processed')) return;
  form.setAttribute('data-tms-processed', 'true');
  
  // Store original button text
  const submitBtn = form.querySelector('button[type="submit"]');
  if (submitBtn && !submitBtn.getAttribute('data-original-text')) {
    submitBtn.setAttribute('data-original-text', submitBtn.textContent);
  }
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Prevent double submission
    if (form.getAttribute('data-submitting') === 'true') {
      return;
    }
    
    // Client-side validation
    const validationErrors = TMS.validateForm(form);
    if (validationErrors.length > 0) {
      TMS.showNotification(validationErrors.join('<br>'), 'error', 8000);
      return;
    }
    
    form.setAttribute('data-submitting', 'true');
    
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Saving...';
    }
    
    try {
      const formData = new FormData(form);
      const response = await fetch(form.action || window.location.pathname, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (response.ok) {
        // Check if response is JSON (success response)
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          if (data.success && data.redirect_url) {
            // Show success message and redirect
            if (data.message) {
              // Show success notification
              TMS.showNotification(data.message, 'success');
            }
            window.location.href = data.redirect_url;
            return;
          } else if (data.success === false && data.message) {
            // Show error message
            TMS.showNotification(data.message, 'error');
            // Re-enable button and reset submission flag
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = submitBtn.getAttribute('data-original-text') || 'Save';
            }
            form.removeAttribute('data-submitting');
            return;
          }
        }
        
        // Check if it's a redirect response (status 200 but URL changed)
        if (response.redirected || response.status === 302) {
          // Standard navigation
          window.location.href = response.url;
        } else {
          // Check if response contains a redirect URL in the response
          const responseText = await response.text();
          
          // Check if the response is a redirect (contains location header or redirect URL)
          if (responseText.includes('redirect') || responseText.includes('location')) {
            // Extract redirect URL if present
            const urlMatch = responseText.match(/window\.location\.href\s*=\s*['"]([^'"]+)['"]/);
            if (urlMatch) {
              window.location.href = urlMatch[1];
              return;
            }
          }
          
          // Parse response as HTML and update content
          const parser = new DOMParser();
          const doc = parser.parseFromString(responseText, 'text/html');
          const main = doc.querySelector('main.container') || doc.querySelector('main.content');
          const target = document.querySelector('main.container, main.content');
          
          if (main && target) {
            target.innerHTML = main.innerHTML;
            
            // Reinitialize functionality
            setTimeout(() => {
              if (typeof TMS !== 'undefined') {
                TMS.enhanceSelects();
                TMS.enhanceStationFields();
              }
            }, 100);
          } else {
            // If no content to update, redirect to list page
            window.location.href = '/orders/' || '/builty/';
          }
        }
      } else {
        // Handle validation errors
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const main = doc.querySelector('main.container') || doc.querySelector('main.content');
        const target = document.querySelector('main.container, main.content');
        
        if (main && target) {
          target.innerHTML = main.innerHTML;
          
          // Reinitialize functionality
          setTimeout(() => {
            if (typeof TMS !== 'undefined') {
              TMS.enhanceSelects();
              TMS.enhanceStationFields();
            }
          }, 100);
        }
        
        // Re-enable button and reset submission flag
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = submitBtn.getAttribute('data-original-text') || 'Save';
        }
        form.removeAttribute('data-submitting');
      }
    } catch (error) {
      console.error('Form submission error:', error);
      
      // Show error notification
      TMS.showNotification('An error occurred while saving. Please try again.', 'error');
      
      // Fallback to normal form submission
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = submitBtn.getAttribute('data-original-text') || 'Save';
      }
      
      // Reset submission flag
      form.removeAttribute('data-submitting');
      
      // Submit normally
      form.submit();
    }
  });
};

// Notification System
TMS.showNotification = function(message, type = 'info', duration = 5000) {
  // Remove existing notifications
  const existingNotifications = document.querySelectorAll('.tms-notification');
  existingNotifications.forEach(notification => notification.remove());
  
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `tms-notification tms-notification-${type}`;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : type === 'warning' ? '#fff3cd' : '#d1ecf1'};
    color: ${type === 'success' ? '#155724' : type === 'error' ? '#721c24' : type === 'warning' ? '#856404' : '#0c5460'};
    border: 1px solid ${type === 'success' ? '#c3e6cb' : type === 'error' ? '#f5c6cb' : type === 'warning' ? '#ffeaa7' : '#bee5eb'};
    border-radius: 6px;
    padding: 12px 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 10000;
    max-width: 400px;
    font-size: 14px;
    line-height: 1.4;
    animation: slideInRight 0.3s ease-out;
  `;
  
  notification.innerHTML = `
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="font-weight: 600;">${message}</span>
      <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 18px; line-height: 1; padding: 0; margin-left: auto;">&times;</button>
    </div>
  `;
  
  // Add CSS animation
  if (!document.querySelector('#tms-notification-styles')) {
    const style = document.createElement('style');
    style.id = 'tms-notification-styles';
    style.textContent = `
      @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
  
  document.body.appendChild(notification);
  
  // Auto remove after duration
  setTimeout(() => {
    if (notification.parentElement) {
      notification.style.animation = 'slideOutRight 0.3s ease-in';
      setTimeout(() => notification.remove(), 300);
    }
  }, duration);
};

// Enhanced initialization
document.addEventListener('DOMContentLoaded', function() {
  TMS.pjax();
  TMS.enhanceSelects();
  TMS.enhanceStationFields();
  TMS.initNavbar(); // Initialize navbar with scroll behavior

  // Handle all form submissions (only once)
  document.querySelectorAll('form').forEach(form => {
    TMS.handleFormSubmission(form);
  });
});
