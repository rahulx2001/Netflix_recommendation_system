// Netflix × Raycast - Clean, Minimal Animations
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initProgressBar();
    initScrollAnimations();
    initCounters();
    initDemo();
    initNavHighlight();
    initImageLightbox();
    initFloatingDemoCTA();
});

// ===== PARTICLES - More subtle =====
function initParticles() {
    const canvas = document.getElementById('particles');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    function createParticle() {
        return {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 1.5 + 0.5,
            speedX: (Math.random() - 0.5) * 0.3,
            speedY: (Math.random() - 0.5) * 0.3,
            opacity: Math.random() * 0.3 + 0.1
        };
    }
    
    function initParticlesArray() {
        particles = [];
        const particleCount = Math.floor((canvas.width * canvas.height) / 20000);
        for (let i = 0; i < Math.min(particleCount, 80); i++) {
            particles.push(createParticle());
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            
            if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
            if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(229, 9, 20, ${p.opacity})`;
            ctx.fill();
        });
        
        animationId = requestAnimationFrame(animate);
    }
    
    resize();
    initParticlesArray();
    animate();
    
    window.addEventListener('resize', () => {
        resize();
        initParticlesArray();
    });
}

// ===== PROGRESS BAR =====
function initProgressBar() {
    const progressFill = document.querySelector('.progress-fill');
    if (!progressFill) return;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressFill.style.width = scrollPercent + '%';
    });
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || 0;
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, delay * 1000);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => observer.observe(el));
}

// ===== COUNTERS =====
function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.count);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target) {
    const duration = 2000;
    const steps = 60;
    const stepTime = duration / steps;
    let current = 0;
    
    const increment = target / steps;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, stepTime);
}

// ===== DEMO FUNCTIONALITY =====
function initDemo() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const quickPicks = document.querySelectorAll('.quick-picks button');
    
    if (!searchInput || !searchBtn) return;
    
    searchBtn.addEventListener('click', () => {
        performSearch(searchInput.value);
    });
    
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch(searchInput.value);
        }
    });
    
    quickPicks.forEach(btn => {
        btn.addEventListener('click', () => {
            const title = btn.dataset.title;
            searchInput.value = title;
            performSearch(title);
        });
    });
}

function performSearch(query) {
    if (!query.trim()) return;
    
    const resultsContainer = document.getElementById('demoResults');
    if (!resultsContainer) return;
    
    // Show loading state
    resultsContainer.innerHTML = `
        <div class="placeholder">
            <div class="placeholder-icon">⏳</div>
            <h3>Searching for "${query}"...</h3>
            <p>Finding similar content based on our clustering model</p>
        </div>
    `;
    
    // Simulate search delay then call demo.js function if available
    setTimeout(() => {
        if (typeof searchNetflix === 'function') {
            searchNetflix(query);
        } else {
            resultsContainer.innerHTML = `
                <div class="placeholder">
                    <div class="placeholder-icon">📊</div>
                    <h3>Demo data loading...</h3>
                    <p>Please wait for the Netflix data to load</p>
                </div>
            `;
        }
    }, 500);
}

// ===== NAV HIGHLIGHT =====
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    window.addEventListener('scroll', () => {
        let current = '';
        const scrollY = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            
            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// ===== IMAGE LIGHTBOX =====
function initImageLightbox() {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalClose = document.getElementById('modalClose');
    
    if (!modal || !modalImage || !modalClose) return;
    
    const chartImages = document.querySelectorAll('.chart-card img, .cluster-main-viz, .wordcloud-img, .chart-image img');
    
    chartImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', () => {
            modalImage.src = img.src;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

// ===== FLOATING DEMO CTA =====
function initFloatingDemoCTA() {
    const floatingCTA = document.getElementById('floatingDemo');
    const demoSection = document.getElementById('demo');
    
    if (!floatingCTA || !demoSection) return;
    
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const demoRect = demoSection.getBoundingClientRect();
        
        if (scrollY > 500 && demoRect.top > window.innerHeight) {
            floatingCTA.classList.add('visible');
        } else {
            floatingCTA.classList.remove('visible');
        }
    });
    
    const ctaLink = floatingCTA.querySelector('a');
    if (ctaLink) {
        ctaLink.addEventListener('click', (e) => {
            e.preventDefault();
            demoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
}

// ===== SMOOTH SCROLL UTILITY =====
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Make smoothScroll available globally
window.smoothScroll = smoothScroll;
