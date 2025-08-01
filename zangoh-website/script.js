document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Smooth scrolling for navigation links
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

    // Navbar background change on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.service-card, .innovation-card, .about-text, .contact-info, .contact-form');
    animateElements.forEach(el => observer.observe(el));

    // Contact form handling
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const formObject = {};
            formData.forEach((value, key) => {
                formObject[key] = value;
            });

            // Simple form validation
            const name = this.querySelector('input[type="text"]').value;
            const email = this.querySelector('input[type="email"]').value;
            const subject = this.querySelector('input[type="text"]:nth-of-type(2)').value;
            const message = this.querySelector('textarea').value;

            if (!name || !email || !subject || !message) {
                showNotification('Please fill in all fields', 'error');
                return;
            }

            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address', 'error');
                return;
            }

            // Simulate form submission
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            setTimeout(() => {
                showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }

    // Enhanced neural network animation
    function enhanceNeuralNetwork() {
        const neuralNetwork = document.querySelector('.neural-network');
        if (!neuralNetwork) return;

        // Add more dynamic connections
        const connections = neuralNetwork.querySelectorAll('.connection');
        connections.forEach((connection, index) => {
            connection.style.animationDelay = `${index * 0.5}s`;
            connection.style.animationDuration = `${3 + Math.random() * 2}s`;
        });

        // Add pulsing effect to nodes
        const nodes = neuralNetwork.querySelectorAll('.node');
        nodes.forEach((node, index) => {
            node.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.2)';
                this.style.boxShadow = '0 0 30px rgba(102, 126, 234, 0.6)';
            });
            
            node.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
            });
        });
    }

    // Counter animation for stats
    function animateCounters() {
        const counters = document.querySelectorAll('.stat h3');
        const speed = 200;

        counters.forEach(counter => {
            const target = parseInt(counter.textContent);
            const increment = target / speed;
            let current = 0;

            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.ceil(current) + (counter.textContent.includes('+') ? '+' : '') + (counter.textContent.includes('%') ? '%' : '');
                    setTimeout(updateCounter, 10);
                } else {
                    counter.textContent = counter.textContent;
                }
            };

            // Trigger animation when element is visible
            const counterObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        counter.textContent = '0';
                        updateCounter();
                        counterObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            counterObserver.observe(counter);
        });
    }

    // Particle effect for hero section
    function createParticleEffect() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '2px';
            particle.style.height = '2px';
            particle.style.background = 'rgba(102, 126, 234, 0.3)';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            
            const startX = Math.random() * window.innerWidth;
            const startY = Math.random() * window.innerHeight;
            const duration = 10 + Math.random() * 20;
            
            particle.style.left = startX + 'px';
            particle.style.top = startY + 'px';
            
            particle.animate([
                { transform: 'translateY(0px)', opacity: 0 },
                { transform: 'translateY(-100px)', opacity: 1 },
                { transform: 'translateY(-200px)', opacity: 0 }
            ], {
                duration: duration * 1000,
                iterations: Infinity,
                delay: Math.random() * 5000
            });
            
            hero.appendChild(particle);
        }
    }

    // Tech stack hover effects
    function addTechStackEffects() {
        const techItems = document.querySelectorAll('.tech-item');
        techItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                this.style.color = 'white';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.background = '#ffffff';
                this.style.color = '#667eea';
            });
        });
    }

    // Utility functions
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showNotification(message, type) {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 2rem;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            background: ${type === 'success' ? '#48bb78' : '#f56565'};
        `;

        // Add slide in animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => {
                notification.remove();
                style.remove();
            }, 300);
        }, 4000);
    }

    // Innovation cards interactive effects
    function addInnovationEffects() {
        const innovationCards = document.querySelectorAll('.innovation-card');
        
        innovationCards.forEach(card => {
            // Add glow effect on hover
            card.addEventListener('mouseenter', function() {
                this.style.boxShadow = '0 25px 50px -12px rgba(102, 126, 234, 0.3), 0 0 0 1px rgba(102, 126, 234, 0.1)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.boxShadow = '';
            });
            
            // Add click animation
            card.addEventListener('click', function() {
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
        
        // Animate tech tags
        const techTags = document.querySelectorAll('.tech-tag');
        techTags.forEach((tag, index) => {
            tag.style.animationDelay = `${index * 0.1}s`;
            tag.classList.add('fade-in-up');
        });
    }
    
    // AI metrics counter with enhanced animation
    function animateInnovationMetrics() {
        const metrics = document.querySelectorAll('.metric-value');
        
        metrics.forEach(metric => {
            const targetText = metric.textContent;
            const targetNumber = parseInt(targetText.replace(/[^\d]/g, ''));
            const suffix = targetText.replace(/[\d]/g, '');
            
            if (targetNumber > 0) {
                const duration = 2000;
                const increment = targetNumber / (duration / 16);
                let current = 0;
                
                const updateMetric = () => {
                    if (current < targetNumber) {
                        current += increment;
                        metric.textContent = Math.ceil(current) + suffix;
                        requestAnimationFrame(updateMetric);
                    } else {
                        metric.textContent = targetText;
                    }
                };
                
                // Trigger animation when element is visible
                const metricObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            metric.textContent = '0' + suffix;
                            updateMetric();
                            metricObserver.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.5 });
                
                metricObserver.observe(metric);
            }
        });
    }
    
    // AI-themed cursor effect for innovation section
    function addAICursorEffect() {
        const innovationsSection = document.querySelector('.innovations');
        if (!innovationsSection) return;
        
        let mouseX = 0;
        let mouseY = 0;
        
        innovationsSection.addEventListener('mousemove', (e) => {
            mouseX = e.clientX - innovationsSection.offsetLeft;
            mouseY = e.clientY - innovationsSection.offsetTop;
            
            // Create glowing cursor trail
            const trail = document.createElement('div');
            trail.style.cssText = `
                position: absolute;
                left: ${mouseX}px;
                top: ${mouseY}px;
                width: 4px;
                height: 4px;
                background: rgba(240, 147, 251, 0.6);
                border-radius: 50%;
                pointer-events: none;
                z-index: 10;
                animation: cursorTrail 1s ease-out forwards;
            `;
            
            innovationsSection.appendChild(trail);
            
            setTimeout(() => {
                trail.remove();
            }, 1000);
        });
        
        // Add cursor trail animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes cursorTrail {
                from {
                    opacity: 1;
                    transform: scale(1);
                }
                to {
                    opacity: 0;
                    transform: scale(3);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Enhanced neural network with more interactive features
    function enhanceNeuralNetworkAdvanced() {
        const neuralNetwork = document.querySelector('.neural-network');
        if (!neuralNetwork) return;
        
        // Add data flow animation
        const connections = neuralNetwork.querySelectorAll('.connection');
        connections.forEach((connection, index) => {
            // Create flowing data particles
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: linear-gradient(45deg, #f093fb, #f5576c);
                border-radius: 50%;
                box-shadow: 0 0 10px rgba(240, 147, 251, 0.8);
            `;
            
            connection.appendChild(particle);
            
            // Animate particle along connection
            particle.animate([
                { left: '0%', opacity: 0 },
                { left: '50%', opacity: 1 },
                { left: '100%', opacity: 0 }
            ], {
                duration: 3000 + Math.random() * 2000,
                iterations: Infinity,
                delay: Math.random() * 2000
            });
        });
    }

    // Initialize all enhancements
    enhanceNeuralNetwork();
    enhanceNeuralNetworkAdvanced();
    animateCounters();
    animateInnovationMetrics();
    createParticleEffect();
    addTechStackEffects();
    addInnovationEffects();
    addAICursorEffect();

    // Handle window resize
    window.addEventListener('resize', function() {
        // Close mobile menu on resize
        if (window.innerWidth > 768) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });

    // Preload images for better performance
    const images = [
        // Add any image URLs here if you add images later
    ];
    
    images.forEach(src => {
        const img = new Image();
        img.src = src;
    });

    console.log('Zangoh website loaded successfully! 🚀');
});