document.addEventListener('astro:page-load', () => {

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

    // --- 2. Scroll Animations Setup (GSAP) ---
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
        const scrollElements = document.querySelectorAll('.animate-on-scroll');
        
        scrollElements.forEach(el => {
            // Remove CSS transition to let GSAP handle it smoothly
            el.style.transition = 'none';
            gsap.fromTo(el, 
                { y: 40, opacity: 0 }, 
                { 
                    y: 0, 
                    opacity: 1, 
                    duration: 0.8,
                    ease: 'power2.out',
                    scrollTrigger: {
                        trigger: el,
                        start: "top 90%",
                        toggleActions: "play none none none"
                    }
                }
            );
        });

        // Hover animations for scheme cards (GSAP)
        const schemeCards = document.querySelectorAll('.scheme-card');
        schemeCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    gsap.to(card, { scale: 1.03, duration: 0.3, ease: 'power1.out' });
                }
            });
            card.addEventListener('mouseleave', () => {
                gsap.to(card, { scale: 1, duration: 0.3, ease: 'power1.out' });
            });
        });
    }

    // --- 3. FAQ Accordion Setup (for other pages) ---
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        if (question) {
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
        }
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

});
