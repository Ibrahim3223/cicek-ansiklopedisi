// Çiçek Ansiklopedisi - Ana JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Search functionality
  initSearch();

  // Mobile menu
  initMobileMenu();

  // Scroll to top
  initScrollToTop();

  // FAQ accordions
  initFAQ();

  // Filter buttons
  initFilters();
});

// ========================================
// Search Functionality
// ========================================
let searchIndex = [];
let searchTimeout = null;

async function initSearch() {
  // Load search index
  try {
    const response = await fetch('/index.json');
    searchIndex = await response.json();
  } catch (error) {
    console.log('Search index not available yet');
  }

  // Header search
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (searchInput && searchResults) {
    searchInput.addEventListener('input', (e) => handleSearch(e, searchResults));
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.length >= 2) {
        searchResults.classList.add('active');
      }
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-box')) {
        searchResults.classList.remove('active');
      }
    });
  }

  // Hero search
  const heroSearchInput = document.getElementById('hero-search-input');
  if (heroSearchInput) {
    heroSearchInput.addEventListener('input', (e) => {
      // Redirect to header search on mobile or show inline results
      const query = e.target.value;
      if (query.length >= 2 && searchInput) {
        searchInput.value = query;
        searchInput.focus();
        handleSearch({ target: searchInput }, searchResults);
      }
    });
  }

  // Mobile search
  const mobileSearchInput = document.getElementById('mobile-search-input');
  if (mobileSearchInput) {
    mobileSearchInput.addEventListener('input', (e) => {
      if (searchInput) {
        searchInput.value = e.target.value;
        handleSearch({ target: searchInput }, searchResults);
      }
    });
  }
}

function handleSearch(e, resultsContainer) {
  const query = e.target.value.toLowerCase().trim();

  // Clear previous timeout
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  // Debounce search
  searchTimeout = setTimeout(() => {
    if (query.length < 2) {
      resultsContainer.classList.remove('active');
      return;
    }

    // Normalize Turkish characters
    const normalizedQuery = normalizeText(query);

    // Search
    const results = searchIndex.filter(item => {
      const title = normalizeText(item.title.toLowerCase());
      const latince = normalizeText((item.latince || '').toLowerCase());
      const description = normalizeText((item.description || '').toLowerCase());

      return title.includes(normalizedQuery) ||
             latince.includes(normalizedQuery) ||
             description.includes(normalizedQuery);
    }).slice(0, 8);

    // Render results
    renderSearchResults(results, resultsContainer);
  }, 200);
}

function renderSearchResults(results, container) {
  if (results.length === 0) {
    container.innerHTML = `
      <div style="padding: 1rem; text-align: center; color: #6b7280;">
        Sonuç bulunamadı
      </div>
    `;
    container.classList.add('active');
    return;
  }

  container.innerHTML = results.map(item => `
    <a href="${item.url}" class="search-result-item">
      ${item.image ?
        `<img src="${item.image}" alt="${item.title}">` :
        `<div class="no-image" style="width: 48px; height: 48px; font-size: 1.5rem; border-radius: 0.375rem;">🌱</div>`
      }
      <div class="search-result-info">
        <h4>${item.title}</h4>
        <p>${item.latince || item.tur || 'Bitki'}</p>
      </div>
    </a>
  `).join('');

  container.classList.add('active');
}

// Normalize Turkish characters
function normalizeText(text) {
  return text
    .replace(/ı/g, 'i')
    .replace(/İ/g, 'i')
    .replace(/ğ/g, 'g')
    .replace(/Ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/Ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/Ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/Ö/g, 'o')
    .replace(/ç/g, 'c')
    .replace(/Ç/g, 'c');
}

// ========================================
// Mobile Menu
// ========================================
function initMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileNav = document.getElementById('mobile-nav');

  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', () => {
      mobileNav.classList.toggle('active');

      // Update icon
      const isActive = mobileNav.classList.contains('active');
      menuBtn.innerHTML = isActive ?
        `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>` :
        `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>`;
    });

    // Close on link click
    const mobileLinks = mobileNav.querySelectorAll('.mobile-nav-link');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('active');
      });
    });
  }
}

// ========================================
// Scroll to Top
// ========================================
function initScrollToTop() {
  const scrollBtn = document.getElementById('scroll-to-top');

  if (scrollBtn) {
    let lastScrollTop = 0;
    let ticking = false;

    // Throttled scroll handler to prevent forced reflow
    function handleScroll() {
      lastScrollTop = window.scrollY;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (lastScrollTop > 300) {
            scrollBtn.classList.add('visible');
          } else {
            scrollBtn.classList.remove('visible');
          }
          ticking = false;
        });

        ticking = true;
      }
    }

    // Show/hide based on scroll position
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Scroll to top on click
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

// ========================================
// FAQ Accordions
// ========================================
function initFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', () => {
        // Close other items
        faqItems.forEach(other => {
          if (other !== item) {
            other.classList.remove('active');
          }
        });

        // Toggle current item
        item.classList.toggle('active');
      });
    }
  });
}

// ========================================
// Filter Buttons
// ========================================
function initFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
  const plantCards = document.querySelectorAll('.plant-card[data-bakim]');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter cards - Use class toggle instead of direct style to prevent layout thrashing
      window.requestAnimationFrame(() => {
        plantCards.forEach(card => {
          const bakim = card.dataset.bakim;
          let shouldShow = false;

          if (filter === 'all') {
            shouldShow = true;
          } else if (filter === 'kolay' && bakim === 'kolay') {
            shouldShow = true;
          } else if (filter === 'orta' && bakim === 'orta') {
            shouldShow = true;
          } else if (filter === 'az-isik' || filter === 'cok-isik') {
            // This would need light data
            shouldShow = true;
          }

          card.style.display = shouldShow ? '' : 'none';
        });
      });
    });
  });
}

// ========================================
// Smooth Scroll for Anchor Links
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});
