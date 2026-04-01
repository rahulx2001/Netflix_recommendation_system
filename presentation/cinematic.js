// Netflix Cinematic Presentation - Heavy Animations
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initProgressBar();
    initHeroAnimations();
    initScrollAnimations();
    initCounters();
    initDemo();
    initNavHighlight();
    initImageLightbox();
    initFloatingDemoCTA();
});

// ===== FLOATING DEMO CTA =====
function initFloatingDemoCTA() {
    const floatingCTA = document.getElementById('floatingDemo');
    const demoSection = document.getElementById('demo');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const demoRect = demoSection.getBoundingClientRect();

        // Show floating CTA after scrolling past hero, hide when demo is visible
        if (scrollY > 500 && demoRect.top > window.innerHeight) {
            floatingCTA.classList.add('visible');
        } else {
            floatingCTA.classList.remove('visible');
        }
    });

    // Smooth scroll to demo
    floatingCTA.querySelector('a').addEventListener('click', (e) => {
        e.preventDefault();
        demoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
}

// ===== IMAGE LIGHTBOX =====
function initImageLightbox() {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalClose = document.getElementById('modalClose');

    // Add click listeners to all chart images
    const chartImages = document.querySelectorAll('.chart-card img, .cluster-main-viz, .wordcloud-img, .chart-image img');

    chartImages.forEach(img => {
        img.addEventListener('click', () => {
            modalImage.src = img.src;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // --- Simple firework burst on close ---
    const burstCanvas = document.createElement('canvas');
    burstCanvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:10001;';
    document.body.appendChild(burstCanvas);
    const bCtx = burstCanvas.getContext('2d');
    burstCanvas.width = window.innerWidth;
    burstCanvas.height = window.innerHeight;
    window.addEventListener('resize', () => { burstCanvas.width = window.innerWidth; burstCanvas.height = window.innerHeight; });

    let sparks = [];
    let burstRunning = false;

    function fireworkBurst(x, y) {
        const colors = ['#e50914', '#ff4444', '#ff6b6b', '#00d4ff', '#ffffff', '#f59e0b'];
        for (let i = 0; i < 30; i++) {
            const angle = (i / 30) * Math.PI * 2 + (Math.random() - 0.5) * 0.3;
            const speed = 3 + Math.random() * 5;
            sparks.push({
                x, y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size: Math.random() * 3 + 1.5,
                color: colors[Math.floor(Math.random() * colors.length)],
                life: 1
            });
        }
        if (!burstRunning) { burstRunning = true; animateBurst(); }
    }

    function animateBurst() {
        bCtx.clearRect(0, 0, burstCanvas.width, burstCanvas.height);
        sparks = sparks.filter(s => s.life > 0);
        sparks.forEach(s => {
            s.x += s.vx;
            s.y += s.vy;
            s.vy += 0.12;          // gravity
            s.vx *= 0.97;
            s.vy *= 0.97;
            s.life -= 0.025;
            s.size *= 0.985;
            bCtx.globalAlpha = s.life;
            bCtx.beginPath();
            bCtx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            bCtx.fillStyle = s.color;
            bCtx.fill();
        });
        bCtx.globalAlpha = 1;
        if (sparks.length > 0) {
            requestAnimationFrame(animateBurst);
        } else {
            burstRunning = false;
        }
    }

    modalClose.addEventListener('click', () => {
        const rect = modalClose.getBoundingClientRect();
        fireworkBurst(rect.left + rect.width / 2, rect.top + rect.height / 2);
        setTimeout(closeModal, 120);
    });
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            fireworkBurst(e.clientX, e.clientY);
            setTimeout(closeModal, 120);
        }
    });
}
// ===== END IMAGE LIGHTBOX (simplified) =====


// ===== PARTICLE BACKGROUND =====
function initParticles() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    let particles = [];

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.5 + 0.1;
            this.color = Math.random() > 0.5 ? '#e50914' : '#00d4ff';
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
                this.reset();
            }
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity;
            ctx.fill();
            ctx.globalAlpha = 1;
        }
    }

    for (let i = 0; i < 100; i++) {
        particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });

        // Connect nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(255,255,255,${0.1 * (1 - dist / 100)})`;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

// ===== PROGRESS BAR =====
function initProgressBar() {
    const progressFill = document.querySelector('.progress-fill');
    window.addEventListener('scroll', () => {
        const scrollTop = document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / scrollHeight) * 100;
        progressFill.style.width = `${progress}%`;
    });
}

// ===== HERO ANIMATIONS =====
function initHeroAnimations() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    // Fade in navigation
    tl.from('.nav', { y: -100, opacity: 0, duration: 0.8 });

    // Hero content staggered entrance
    tl.from('.hero-badge', { y: 50, opacity: 0, duration: 0.6 }, '-=0.3');
    tl.from('.hero-title .line', { y: 80, opacity: 0, stagger: 0.15, duration: 0.8 }, '-=0.4');
    tl.from('.hero-desc', { y: 40, opacity: 0, duration: 0.6 }, '-=0.4');
    tl.from('.hero-stats .stat', { y: 40, opacity: 0, stagger: 0.1, duration: 0.5 }, '-=0.3');
    tl.from('.hero-cta button', { y: 30, opacity: 0, stagger: 0.1, duration: 0.5 }, '-=0.3');

    // Hero visual
    tl.from('.orbit-container', { scale: 0.5, opacity: 0, rotation: -180, duration: 1.2 }, '-=0.8');

    // Scroll indicator
    tl.from('.scroll-indicator', { y: 30, opacity: 0, duration: 0.5 }, '-=0.3');
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    // Section headers
    gsap.utils.toArray('.section-header').forEach(header => {
        gsap.from(header, {
            scrollTrigger: {
                trigger: header,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            y: 60,
            opacity: 0,
            duration: 0.8
        });
    });

    // Problem cards
    gsap.utils.toArray('.insight-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                toggleActions: 'play none none reverse'
            },
            y: 80,
            opacity: 0,
            duration: 0.6,
            delay: i * 0.1
        });
    });

    // Solution box
    gsap.from('.solution-box', {
        scrollTrigger: {
            trigger: '.solution-box',
            start: 'top 80%'
        },
        y: 60,
        opacity: 0,
        duration: 0.8
    });

    // Solution steps
    gsap.utils.toArray('.step').forEach((step, i) => {
        gsap.from(step, {
            scrollTrigger: {
                trigger: step,
                start: 'top 85%'
            },
            y: 40,
            opacity: 0,
            scale: 0.9,
            duration: 0.5,
            delay: i * 0.1
        });
    });

    // Chart blocks
    gsap.utils.toArray('.chart-block').forEach(block => {
        const image = block.querySelector('.chart-image');
        const desc = block.querySelector('.chart-desc');
        const isReverse = block.classList.contains('reverse');

        gsap.from(image, {
            scrollTrigger: {
                trigger: block,
                start: 'top 75%',
                toggleActions: 'play none none reverse'
            },
            x: isReverse ? 100 : -100,
            opacity: 0,
            duration: 0.8
        });

        gsap.from(desc, {
            scrollTrigger: {
                trigger: block,
                start: 'top 75%',
                toggleActions: 'play none none reverse'
            },
            x: isReverse ? -100 : 100,
            opacity: 0,
            duration: 0.8,
            delay: 0.2
        });
    });

    // Chart annotations float in
    gsap.utils.toArray('.chart-annotation').forEach((ann, i) => {
        gsap.from(ann, {
            scrollTrigger: {
                trigger: ann,
                start: 'top 85%'
            },
            scale: 0,
            opacity: 0,
            duration: 0.5,
            delay: 0.3 + i * 0.1
        });
    });

    // Pipeline stages
    gsap.utils.toArray('.pipeline-stage').forEach((stage, i) => {
        gsap.from(stage, {
            scrollTrigger: {
                trigger: '.pipeline-visual',
                start: 'top 75%'
            },
            y: 50,
            opacity: 0,
            scale: 0.8,
            duration: 0.5,
            delay: i * 0.1
        });
    });

    // Chart cards
    gsap.utils.toArray('.chart-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 85%'
            },
            y: 60,
            opacity: 0,
            duration: 0.6,
            delay: i * 0.1
        });
    });

    // Cluster hero
    gsap.from('.cluster-main-viz', {
        scrollTrigger: {
            trigger: '.cluster-hero',
            start: 'top 75%'
        },
        scale: 0.9,
        opacity: 0,
        duration: 1
    });

    // Cluster annotations
    gsap.utils.toArray('.annotation').forEach((ann, i) => {
        gsap.from(ann, {
            scrollTrigger: {
                trigger: '.cluster-hero',
                start: 'top 60%'
            },
            scale: 0,
            opacity: 0,
            duration: 0.5,
            delay: 0.5 + i * 0.15
        });
    });

    // Cluster summary cards
    gsap.utils.toArray('.cluster-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: '.clusters-summary',
                start: 'top 80%'
            },
            y: 50,
            opacity: 0,
            scale: 0.9,
            duration: 0.5,
            delay: i * 0.1
        });
    });

    // Demo container
    gsap.from('.demo-container', {
        scrollTrigger: {
            trigger: '.demo-container',
            start: 'top 75%'
        },
        y: 80,
        opacity: 0,
        duration: 0.8
    });

    // Insights
    gsap.utils.toArray('.insight-big').forEach((insight, i) => {
        gsap.from(insight, {
            scrollTrigger: {
                trigger: insight,
                start: 'top 85%'
            },
            y: 60,
            opacity: 0,
            scale: 0.9,
            duration: 0.6,
            delay: i * 0.15
        });
    });

    // Final CTA
    gsap.from('.final-cta', {
        scrollTrigger: {
            trigger: '.final-cta',
            start: 'top 85%'
        },
        y: 50,
        opacity: 0,
        scale: 0.95,
        duration: 0.7
    });
}

// ===== COUNTERS =====
function initCounters() {
    const counters = document.querySelectorAll('[data-count]');

    counters.forEach(counter => {
        const target = parseInt(counter.dataset.count);
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                animateCounter(counter, target);
                observer.disconnect();
            }
        }, { threshold: 0.5 });
        observer.observe(counter);
    });
}

function animateCounter(el, target) {
    gsap.to(el, {
        innerHTML: target,
        duration: 2,
        snap: { innerHTML: 1 },
        ease: 'power2.out'
    });
}

// ===== SMOOTH SCROLL =====
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// ===== NAVIGATION HIGHLIGHT =====
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

console.log('🎬 Netflix Cinematic Presentation Loaded');

// ===== HOVER TEXT FOOTER EFFECT =====
function initHoverTextEffect() {
    const svg = document.querySelector('.hover-text-svg');
    if (!svg) return;

    const maskCircle = svg.querySelector('.mask-circle');
    if (!maskCircle) return;

    let isHovered = false;

    svg.addEventListener('mouseenter', () => {
        isHovered = true;
    });

    svg.addEventListener('mouseleave', () => {
        isHovered = false;
        // Reset circle position smoothly
        gsap.to(maskCircle, {
            attr: { r: 0, cx: 200, cy: 50 },
            duration: 0.3,
            ease: 'power2.out'
        });
    });

    svg.addEventListener('mousemove', (e) => {
        if (!isHovered) return;

        const rect = svg.getBoundingClientRect();
        const viewBox = svg.viewBox.baseVal;
        
        // Calculate position relative to SVG viewBox
        const x = ((e.clientX - rect.left) / rect.width) * viewBox.width;
        const y = ((e.clientY - rect.top) / rect.height) * viewBox.height;

        // Animate mask circle to follow cursor
        gsap.to(maskCircle, {
            attr: { cx: x, cy: y, r: 120 },
            duration: 0.15,
            ease: 'power2.out'
        });
    });
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHoverTextEffect);
} else {
    initHoverTextEffect();
}

// ===== THREE.JS SHADER ANIMATION BACKGROUND =====
function initShaderBackground() {
    const container = document.getElementById('shaderBackground');
    if (!container || typeof THREE === 'undefined') return;

    // Vertex shader
    const vertexShader = `
        void main() {
            gl_Position = vec4(position, 1.0);
        }
    `;

    // Fragment shader - Netflix-themed colors
    const fragmentShader = `
        #define TWO_PI 6.2831853072
        #define PI 3.14159265359

        precision highp float;
        uniform vec2 resolution;
        uniform float time;

        void main(void) {
            vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / min(resolution.x, resolution.y);
            float t = time * 0.05;
            float lineWidth = 0.002;

            vec3 color = vec3(0.0);
            
            // Netflix red, orange, and dark tones
            for(int j = 0; j < 3; j++){
                for(int i = 0; i < 5; i++){
                    float intensity = lineWidth * float(i * i) / abs(fract(t - 0.01 * float(j) + float(i) * 0.01) * 5.0 - length(uv) + mod(uv.x + uv.y, 0.2));
                    if(j == 0) color.r += intensity * 1.2; // Red channel boosted
                    else if(j == 1) color.g += intensity * 0.3; // Less green
                    else color.b += intensity * 0.2; // Even less blue
                }
            }
            
            gl_FragColor = vec4(color, 1.0);
        }
    `;

    // Initialize Three.js
    const camera = new THREE.Camera();
    camera.position.z = 1;

    const scene = new THREE.Scene();
    const geometry = new THREE.PlaneGeometry(2, 2);

    const uniforms = {
        time: { type: 'f', value: 1.0 },
        resolution: { type: 'v2', value: new THREE.Vector2() }
    };

    const material = new THREE.ShaderMaterial({
        uniforms: uniforms,
        vertexShader: vertexShader,
        fragmentShader: fragmentShader
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Handle resize
    function onResize() {
        const width = container.clientWidth || window.innerWidth;
        const height = container.clientHeight || window.innerHeight;
        renderer.setSize(width, height);
        uniforms.resolution.value.x = renderer.domElement.width;
        uniforms.resolution.value.y = renderer.domElement.height;
    }

    onResize();
    window.addEventListener('resize', onResize);

    // Animation loop
    let animationId;
    function animate() {
        animationId = requestAnimationFrame(animate);
        uniforms.time.value += 0.05;
        renderer.render(scene, camera);
    }

    animate();

    // Fade in effect
    gsap.fromTo(container, 
        { opacity: 0 }, 
        { opacity: 1, duration: 2, ease: 'power2.out' }
    );

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        cancelAnimationFrame(animationId);
        renderer.dispose();
        geometry.dispose();
        material.dispose();
    });
}

// Initialize shader on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initShaderBackground);
} else {
    initShaderBackground();
}
