document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Client-Side Search Filtering Logic ---
    const searchInput = document.getElementById('scheme-search');
    const allSchemeCards = document.querySelectorAll('article.scheme-card');
    const noResultsMsg = document.getElementById('no-results-msg');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();
            let visibleCount = 0;

            allSchemeCards.forEach(card => {
                // Get text from card title, description, and marathi name
                const titleEng = card.querySelector('h3')?.textContent.toLowerCase() || '';
                const titleMar = card.querySelector('.scheme-marathi-name')?.textContent.toLowerCase() || '';
                const desc = card.querySelector('.scheme-desc')?.textContent.toLowerCase() || '';
                // Also search the English keyword bank (farmer, kisan, mudra, agri, etc.)
                const keywords = (card.getAttribute('data-keywords') || '').toLowerCase();
                const tags = (card.getAttribute('data-tags') || '').toLowerCase();
                
                if (titleEng.includes(searchTerm) || titleMar.includes(searchTerm) || desc.includes(searchTerm) || keywords.includes(searchTerm) || tags.includes(searchTerm)) {
                    card.classList.remove('hidden');
                    // Add quick subtle animation for feedback
                    card.style.animation = 'fadeUp 0.3s ease-out forwards';
                    visibleCount++;
                } else {
                    card.classList.add('hidden');
                    card.style.animation = 'none';
                }
            });

            // Toggle No Results Message display based on visibleCount
            if (noResultsMsg) {
                if (visibleCount === 0 && searchTerm !== "") {
                    noResultsMsg.classList.remove('hidden');
                } else {
                    noResultsMsg.classList.add('hidden');
                }
            }
        });
    }

    // --- 2. Scroll Animations Setup ---
    const scrollElements = document.querySelectorAll('.animate-on-scroll');
    
    // Create intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // If the element is visible
            if (entry.isIntersecting) {
                // Add the animating class
                entry.target.classList.add('visible');
                // Unobserve after animating once
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1, // Trigger when 10% of element is visible
        rootMargin: "0px 0px -50px 0px"
    });
    
    // Observe all scroll elements
    scrollElements.forEach(el => observer.observe(el));

    // --- 3. FAQ Accordion Setup (for other pages) ---
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Check if this item is currently active
            const isActive = item.classList.contains('active');
            
            // First, close all other FAQ items (optional, but good for UX)
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
                const otherAnswer = otherItem.querySelector('.faq-answer');
                if(otherAnswer) otherAnswer.style.maxHeight = null;
            });
            
            // If it wasn't active, open it
            if (!isActive) {
                item.classList.add('active');
                const answer = item.querySelector('.faq-answer');
                // Handled gracefully via CSS classes
            }
        });
    });
    

    // --- 5. Advanced Scheme Finder Tool ---
    const runFinderBtn = document.getElementById('run-finder-btn');
    const finderResults = document.getElementById('finder-results');
    const finderCategory = document.getElementById('finder-category');
    
    if (runFinderBtn && finderResults && finderCategory) {
        runFinderBtn.addEventListener('click', () => {
            const category = finderCategory.value;
            // Clear previous results
            finderResults.innerHTML = '';
            finderResults.style.display = 'block';
            
            let matchCount = 0;
            const resultGrid = document.createElement('div');
            resultGrid.style.display = 'grid';
            resultGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
            resultGrid.style.gap = '1.5rem';
            
            allSchemeCards.forEach(card => {
                const tags = card.getAttribute('data-tags') || '';
                
                // Extremely simple filter (in a real app, income/age would be stored as data-* attributes and checked)
                if (category === 'all' || tags.includes(category) || (category === 'student' && tags.includes('students'))) {
                    // Clone the card for the results area
                    const clonedCard = card.cloneNode(true);
                    clonedCard.classList.remove('hidden', 'animate-on-scroll', 'visible');
                    clonedCard.style.opacity = '1';
                    clonedCard.style.transform = 'none';
                    resultGrid.appendChild(clonedCard);
                    matchCount++;
                }
            });
            
            if (matchCount > 0) {
                const header = document.createElement('h3');
                header.style.marginBottom = '1.5rem';
                header.style.color = 'var(--text-dark)';
                header.innerHTML = `🎉 तुमच्यासाठी <strong>${matchCount}</strong> संबंधित योजना सापडल्या:`;
                finderResults.appendChild(header);
                finderResults.appendChild(resultGrid);
            } else {
                finderResults.innerHTML = '<p style="text-align:center; color: var(--text-muted); padding: 2rem;"><i class="fa-solid fa-search-minus" style="font-size: 2rem; margin-bottom: 1rem; display: block; opacity: 0.5;"></i>तुमच्या निकषांनुसार कोणतीही योजना सापडली नाही.</p>';
            }
        });
    }

    // --- 6. Header Actions ---
    const headerSearchBtn = document.getElementById('header-search-trigger');
    const mainSearchInput = document.getElementById('scheme-search');
    
    if (headerSearchBtn) {
        headerSearchBtn.addEventListener('click', () => {
            if (mainSearchInput) {
                mainSearchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                setTimeout(() => mainSearchInput.focus(), 600);
            } else {
                window.location.href = '/?search=true';
            }
        });
    }

    // Auto-focus search if URL param exists
    if (window.location.search.includes('search=true') && mainSearchInput) {
        setTimeout(() => {
            mainSearchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            mainSearchInput.focus();
        }, 500);
    }

    const mobileMenuBtn = document.getElementById('mobile-menu-trigger');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            alert('मोबाइल मेनू लवकरच येत आहे! (Mobile menu coming soon!)');
        });
    }

});

