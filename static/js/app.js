/* ==========================================================================
   GLOBAL APP INTERACTIONS, THEME ENGINE & FLOATING MEDICAL BACKGROUND
   Clinical Symbol System
   ========================================================================== */

// Theme Engine (Light Pastel Trắng / Dark)
(function initTheme() {
    const isAuthPage = window.location.pathname.includes('/login') || 
                       window.location.pathname.includes('/register');
    
    // Yêu cầu: Các trang khác để màu pastel trắng; Sign in / Sign up để kiểu slidebar glass liquid
    if (isAuthPage) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        const savedTheme = localStorage.getItem('clinical_app_theme');
        // Mặc định các trang khác là pastel trắng (light) trừ khi người dùng chủ động chọn dark
        if (savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
})();

function toggleGlobalTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('clinical_app_theme', newTheme);

    // Update all toggle buttons
    document.querySelectorAll('.btn-theme-toggle').forEach(btn => {
        btn.innerHTML = newTheme === 'dark' ? '🌙' : '☀️';
        btn.title = newTheme === 'dark' ? 'Chuyển sang Giao diện Sáng' : 'Chuyển sang Giao diện Tối';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    document.querySelectorAll('.btn-theme-toggle').forEach(btn => {
        btn.innerHTML = currentTheme === 'dark' ? '🌙' : '☀️';
        btn.addEventListener('click', toggleGlobalTheme);
    });

    // Initialize Sidebar Collapsed State
    const savedCollapsed = localStorage.getItem('clinical_sidebar_collapsed') === 'true';
    const layout = document.querySelector('.app-layout');
    if (layout && savedCollapsed) {
        layout.classList.add('sidebar-collapsed');
    }
    updateSidebarToggleIcons(savedCollapsed);

    document.querySelectorAll('.btn-sidebar-toggle').forEach(btn => {
        btn.addEventListener('click', toggleSidebar);
    });

    // Initialize Floating Medical Background Elements
    initFloatingMedicalBackground();
});

// Sidebar Collapse Toggle Engine
function toggleSidebar() {
    const layout = document.querySelector('.app-layout');
    if (!layout) return;
    const isCollapsed = layout.classList.toggle('sidebar-collapsed');
    localStorage.setItem('clinical_sidebar_collapsed', isCollapsed ? 'true' : 'false');
    updateSidebarToggleIcons(isCollapsed);
}

function updateSidebarToggleIcons(isCollapsed) {
    document.querySelectorAll('.btn-sidebar-toggle').forEach(btn => {
        btn.innerHTML = isCollapsed ? '❯' : '❮';
        btn.title = isCollapsed ? 'Mở rộng thanh điều hướng' : 'Thu gọn thanh điều hướng';
    });
}

// Global Filter for Symbol Catalog Cards
function filterSymbolCatalog(category, buttonEl) {
    if (buttonEl) {
        document.querySelectorAll('.catalog-tab-btn').forEach(btn => btn.classList.remove('active'));
        buttonEl.classList.add('active');
    }

    const cards = document.querySelectorAll('.compact-symbol-card');
    cards.forEach(card => {
        const cardCat = card.dataset.category || '';
        if (category === 'all' || cardCat.toLowerCase().includes(category.toLowerCase())) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

function filterGlobalSymbols(query) {
    const q = (query || '').trim().toLowerCase();
    const cards = document.querySelectorAll('.compact-symbol-card');
    cards.forEach(card => {
        const name = (card.dataset.name || '').toLowerCase();
        const code = (card.dataset.code || '').toLowerCase();
        const cat = (card.dataset.category || '').toLowerCase();
        if (!q || name.includes(q) || code.includes(q) || cat.includes(q)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Modal Helpers
function openModalById(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('open');
}

function closeModalById(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('open');
}

// Global Sidebar Modals
function openAIBrainModal() {
    openModalById('aiBrainModal');
}

function openUserProfileModal() {
    openModalById('userProfileModal');
}

/* ==========================================================================
   FLOATING MEDICAL PARTICLES (PILLS, SYRINGES, STETHOSCOPES, CROSSES)
   ========================================================================== */

function getMedicalSvg(type, id) {
    switch (type) {
        case 'capsule':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="capB_${id}" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#38bdf8"/>
                  <stop offset="100%" stop-color="#2563eb"/>
                </linearGradient>
                <linearGradient id="capR_${id}" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#f43f5e"/>
                  <stop offset="100%" stop-color="#fb7185"/>
                </linearGradient>
              </defs>
              <g transform="rotate(-35 32 32)">
                <path d="M22 32 V46 A10 10 0 0 0 42 46 V32 Z" fill="url(#capB_${id})"/>
                <path d="M22 32 V18 A10 10 0 0 1 42 18 V32 Z" fill="url(#capR_${id})"/>
                <line x1="22" y1="32" x2="42" y2="32" stroke="#ffffff" stroke-width="1.5" stroke-opacity="0.8"/>
                <path d="M25 18 A7 7 0 0 1 31 13" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-opacity="0.7"/>
                <line x1="25" y1="22" x2="25" y2="44" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-opacity="0.5"/>
              </g>
            </svg>`;
        case 'roundPill':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="roundGrad_${id}" cx="35%" cy="35%" r="65%">
                  <stop offset="0%" stop-color="#ffffff"/>
                  <stop offset="60%" stop-color="#e0e7ff"/>
                  <stop offset="100%" stop-color="#818cf8"/>
                </radialGradient>
              </defs>
              <circle cx="32" cy="32" r="22" fill="url(#roundGrad_${id})" stroke="#a5b4fc" stroke-width="2"/>
              <line x1="16" y1="32" x2="48" y2="32" stroke="#6366f1" stroke-width="2.2" stroke-linecap="round" stroke-opacity="0.7"/>
              <path d="M20 20 A16 16 0 0 1 44 20" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-opacity="0.85"/>
            </svg>`;
        case 'syringe':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g transform="rotate(-40 32 32)">
                <line x1="32" y1="4" x2="32" y2="15" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
                <rect x="29" y="15" width="6" height="4" rx="1" fill="#64748b"/>
                <rect x="25" y="19" width="14" height="28" rx="2" fill="rgba(186, 230, 253, 0.45)" stroke="#38bdf8" stroke-width="2"/>
                <rect x="26.5" y="27" width="11" height="19" fill="#0ea5e9" fill-opacity="0.7"/>
                <line x1="28" y1="23" x2="31" y2="23" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="28" y1="27" x2="34" y2="27" stroke="#ffffff" stroke-width="1.5"/>
                <line x1="28" y1="31" x2="31" y2="31" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="28" y1="35" x2="34" y2="35" stroke="#ffffff" stroke-width="1.5"/>
                <line x1="28" y1="39" x2="31" y2="39" stroke="#38bdf8" stroke-width="1.5"/>
                <rect x="21" y="47" width="22" height="3" rx="1.5" fill="#2563eb"/>
                <rect x="30" y="47" width="4" height="10" fill="#94a3b8"/>
                <rect x="25" y="57" width="14" height="3" rx="1.5" fill="#2563eb"/>
              </g>
            </svg>`;
        case 'stethoscope':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="20" cy="14" r="3.2" fill="#38bdf8"/>
              <circle cx="44" cy="14" r="3.2" fill="#38bdf8"/>
              <path d="M20 16 V23 C20 31 28 35 32 37 C36 35 44 31 44 23 V16" stroke="#94a3b8" stroke-width="3" stroke-linecap="round" fill="none"/>
              <path d="M32 37 V43 C32 50 23 52 23 46 C23 39 41 39 43 47 C44 51 41 55 36 55" stroke="#818cf8" stroke-width="3.5" stroke-linecap="round" fill="none"/>
              <circle cx="36" cy="55" r="6" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
              <circle cx="36" cy="55" r="2.5" fill="#ffffff"/>
            </svg>`;
        case 'cross':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="crossGrad_${id}" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#34d399"/>
                  <stop offset="100%" stop-color="#059669"/>
                </linearGradient>
              </defs>
              <path d="M26 12 C26 9.8 27.8 8 30 8 H34 C36.2 8 38 9.8 38 12 V26 H52 C54.2 26 56 27.8 56 30 V34 C56 36.2 54.2 38 52 38 H38 V52 C38 54.2 36.2 56 34 56 H30 C27.8 56 26 54.2 26 52 V38 H12 C9.8 38 8 36.2 8 34 V30 C8 27.8 9.8 26 12 26 H26 V12 Z" fill="url(#crossGrad_${id})"/>
              <rect x="29" y="12" width="6" height="40" rx="3" fill="#ffffff" fill-opacity="0.35"/>
              <rect x="12" y="29" width="40" height="6" rx="3" fill="#ffffff" fill-opacity="0.35"/>
            </svg>`;
        case 'bandaid':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g transform="rotate(30 32 32)">
                <rect x="10" y="22" width="44" height="20" rx="10" fill="#fcd34d" stroke="#f59e0b" stroke-width="1.5"/>
                <rect x="24" y="22" width="16" height="20" fill="#fef3c7" stroke="#fbbf24" stroke-width="1"/>
                <circle cx="16" cy="28" r="1.3" fill="#d97706"/>
                <circle cx="16" cy="36" r="1.3" fill="#d97706"/>
                <circle cx="20" cy="32" r="1.3" fill="#d97706"/>
                <circle cx="44" cy="32" r="1.3" fill="#d97706"/>
                <circle cx="48" cy="28" r="1.3" fill="#d97706"/>
                <circle cx="48" cy="36" r="1.3" fill="#d97706"/>
              </g>
            </svg>`;
        case 'testTube':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g transform="rotate(-20 32 32)">
                <rect x="25" y="8" width="14" height="3" rx="1.5" fill="#a78bfa"/>
                <path d="M27 11 V46 A5 5 0 0 0 37 46 V11 Z" fill="rgba(196, 181, 253, 0.25)" stroke="#8b5cf6" stroke-width="2"/>
                <path d="M28 28 V46 A4 4 0 0 0 36 46 V28 Z" fill="#8b5cf6" fill-opacity="0.65"/>
                <circle cx="31" cy="37" r="1.5" fill="#ffffff" fill-opacity="0.8"/>
                <circle cx="33" cy="32" r="1" fill="#ffffff" fill-opacity="0.8"/>
                <circle cx="32" cy="42" r="1.2" fill="#ffffff" fill-opacity="0.8"/>
                <line x1="28.5" y1="13" x2="28.5" y2="44" stroke="#ffffff" stroke-width="1.2" stroke-linecap="round" stroke-opacity="0.7"/>
              </g>
            </svg>`;
        case 'ecgHeart':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="ecgGrad_${id}" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#f43f5e"/>
                  <stop offset="100%" stop-color="#fb7185"/>
                </linearGradient>
              </defs>
              <path d="M32 54 S10 40 10 24 A12 12 0 0 1 32 18 A12 12 0 0 1 54 24 C54 40 32 54 32 54 Z" fill="url(#ecgGrad_${id})" fill-opacity="0.3" stroke="#f43f5e" stroke-width="2"/>
              <path d="M14 30 H23 L26 23 L30 38 L34 20 L38 34 L41 30 H50" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>`;
        case 'thermometer':
            return `
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g transform="rotate(25 32 32)">
                <rect x="30" y="8" width="4" height="34" rx="2" fill="rgba(255,255,255,0.4)" stroke="#94a3b8" stroke-width="1.5"/>
                <circle cx="32" cy="46" r="7" fill="#ef4444" stroke="#94a3b8" stroke-width="1.5"/>
                <rect x="31" y="22" width="2" height="20" fill="#ef4444"/>
                <line x1="27" y1="16" x2="29" y2="16" stroke="#64748b" stroke-width="1.5"/>
                <line x1="27" y1="22" x2="29" y2="22" stroke="#64748b" stroke-width="1.5"/>
                <line x1="27" y1="28" x2="29" y2="28" stroke="#64748b" stroke-width="1.5"/>
                <line x1="27" y1="34" x2="29" y2="34" stroke="#64748b" stroke-width="1.5"/>
              </g>
            </svg>`;
        case 'sparkle':
            return `
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 2 C16 9.5 22.5 16 30 16 C22.5 16 16 22.5 16 30 C16 22.5 9.5 16 2 16 C9.5 16 16 9.5 16 2 Z" fill="#67e8f9" fill-opacity="0.85"/>
            </svg>`;
        default:
            return '';
    }
}

function initFloatingMedicalBackground() {
    // Yêu cầu: "cái thuốc chạy qua chạy lại chỉ áp dụng cho sign in sign up thôi các trang khác để màu pastel trắng"
    const isAuthPage = document.querySelector('.sliding-auth-wrapper') !== null ||
                       window.location.pathname.includes('/login') ||
                       window.location.pathname.includes('/register');

    let layer = document.getElementById('medicalFloatingLayer');
    if (!isAuthPage) {
        if (layer) {
            layer.remove();
        }
        return;
    }

    if (!layer) {
        layer = document.createElement('div');
        layer.id = 'medicalFloatingLayer';
        layer.className = 'medical-floating-layer';
        document.body.prepend(layer);
    } else {
        layer.innerHTML = '';
    }

    // Configured list of floating items across different depths, speeds, paths & positions
    const itemsConfig = [
        // Left-to-right drifters
        { type: 'capsule', motion: 'drift-right', top: 8, size: 52, duration: 24, delay: -6, opacity: 0.65, depth: 0.12 },
        { type: 'syringe', motion: 'drift-right', top: 28, size: 58, duration: 32, delay: -18, opacity: 0.58, depth: 0.08 },
        { type: 'cross', motion: 'drift-right', top: 48, size: 44, duration: 28, delay: -10, opacity: 0.62, depth: 0.15 },
        { type: 'roundPill', motion: 'drift-right', top: 68, size: 40, duration: 26, delay: -14, opacity: 0.7, depth: 0.10 },
        { type: 'ecgHeart', motion: 'drift-right', top: 86, size: 54, duration: 30, delay: -22, opacity: 0.65, depth: 0.14 },

        // Right-to-left drifters
        { type: 'testTube', motion: 'drift-left', top: 14, size: 50, duration: 27, delay: -8, opacity: 0.6, depth: 0.11 },
        { type: 'stethoscope', motion: 'drift-left', top: 36, size: 62, duration: 35, delay: -16, opacity: 0.55, depth: 0.07 },
        { type: 'bandaid', motion: 'drift-left', top: 58, size: 48, duration: 29, delay: -12, opacity: 0.68, depth: 0.13 },
        { type: 'capsule', motion: 'drift-left', top: 76, size: 46, duration: 25, delay: -20, opacity: 0.65, depth: 0.10 },
        { type: 'thermometer', motion: 'drift-left', top: 92, size: 48, duration: 33, delay: -5, opacity: 0.55, depth: 0.09 },

        // Wandering / Orbiting in corners & peripheral zones
        { type: 'roundPill', motion: 'drift-wander', top: 18, left: 12, size: 38, duration: 16, delay: -3, opacity: 0.6, depth: 0.06 },
        { type: 'cross', motion: 'drift-wander', top: 72, left: 8, size: 42, duration: 18, delay: -9, opacity: 0.65, depth: 0.08 },
        { type: 'capsule', motion: 'drift-wander', top: 22, left: 82, size: 44, duration: 15, delay: -7, opacity: 0.6, depth: 0.07 },
        { type: 'testTube', motion: 'drift-wander', top: 82, left: 86, size: 42, duration: 17, delay: -11, opacity: 0.58, depth: 0.08 },

        // Sparkle and pulse stars
        { type: 'sparkle', motion: 'sparkle-pulse', top: 12, left: 24, size: 26, duration: 4.5, delay: -1, opacity: 0.8, depth: 0.05 },
        { type: 'sparkle', motion: 'sparkle-pulse', top: 42, left: 16, size: 22, duration: 5.2, delay: -2.5, opacity: 0.75, depth: 0.05 },
        { type: 'sparkle', motion: 'sparkle-pulse', top: 62, left: 78, size: 28, duration: 4.8, delay: -3.2, opacity: 0.85, depth: 0.05 },
        { type: 'sparkle', motion: 'sparkle-pulse', top: 88, left: 38, size: 24, duration: 5.5, delay: -1.8, opacity: 0.8, depth: 0.05 },
        { type: 'sparkle', motion: 'sparkle-pulse', top: 30, left: 88, size: 22, duration: 4.2, delay: -0.5, opacity: 0.75, depth: 0.05 }
    ];

    itemsConfig.forEach((cfg, idx) => {
        const item = document.createElement('div');
        item.className = `floating-med-item ${cfg.motion}`;
        item.dataset.depth = cfg.depth || 0.1;

        item.style.top = `${cfg.top}%`;
        if (cfg.left !== undefined) {
            item.style.left = `${cfg.left}%`;
        }
        item.style.width = `${cfg.size}px`;
        item.style.height = `${cfg.size}px`;
        item.style.animationDuration = `${cfg.duration}s`;
        item.style.animationDelay = `${cfg.delay}s`;
        item.style.setProperty('--med-opacity', cfg.opacity);

        const parallaxWrapper = document.createElement('div');
        parallaxWrapper.className = 'med-item-parallax';

        const inner = document.createElement('div');
        inner.className = 'med-item-inner';
        inner.innerHTML = getMedicalSvg(cfg.type, idx);

        parallaxWrapper.appendChild(inner);
        item.appendChild(parallaxWrapper);
        layer.appendChild(item);
    });

    // Mouse Parallax Effect for immersive 3D clinical ambiance
    let ticking = false;
    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;

    window.addEventListener('mousemove', (e) => {
        targetX = (e.clientX / window.innerWidth - 0.5) * 45;
        targetY = (e.clientY / window.innerHeight - 0.5) * 45;

        if (!ticking) {
            ticking = true;
            requestAnimationFrame(updateParallax);
        }
    }, { passive: true });

    function updateParallax() {
        currentX += (targetX - currentX) * 0.08;
        currentY += (targetY - currentY) * 0.08;

        const items = layer.querySelectorAll('.floating-med-item');
        items.forEach(el => {
            const depth = parseFloat(el.dataset.depth) || 0.1;
            const shiftX = (currentX * depth).toFixed(2);
            const shiftY = (currentY * depth).toFixed(2);
            const pWrapper = el.querySelector('.med-item-parallax');
            if (pWrapper) {
                pWrapper.style.transform = `translate3d(${shiftX}px, ${shiftY}px, 0)`;
            }
        });

        if (Math.abs(targetX - currentX) > 0.1 || Math.abs(targetY - currentY) > 0.1) {
            requestAnimationFrame(updateParallax);
        } else {
            ticking = false;
        }
    }
}

