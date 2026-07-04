/**
 * CTS site scripts.
 * Requires jQuery, AOS, Slick Carousel and Bootstrap 5 (loaded in base.html).
 */

(function($) {
    'use strict';

    // ==========================================
    // Configuration & Constants
    // ==========================================
    const CONFIG = {
        slider: {
            autoPlayDelay: 5000,
            carouselSpeed: 2000
        },
        animation: {
            duration: 800,
            counterDuration: 2000,
            scrollOffset: 80
        },
        scroll: {
            navbarThreshold: 50,
            backToTopThreshold: 300
        }
    };

    // ==========================================
    // CSRF Token Handler (Django)
    // ==========================================
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    function ajaxSetup() {
        $.ajaxSetup({
            headers: { 'X-CSRFToken': csrfToken },
            error: function(xhr) {
                console.error('AJAX Error:', xhr.status, xhr.statusText);
            }
        });
    }

    // ==========================================
    // Preloader
    // ==========================================
    function initPreloader() {
        $(window).on('load', function() {
            $('#preloader').fadeOut('slow', function() {
                $(this).remove();
            });
        });
    }

    // ==========================================
    // AOS Animations
    // ==========================================
    function initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: CONFIG.animation.duration,
                easing: 'ease-in-out',
                once: true,
                offset: 100
            });
        }
    }

    // ==========================================
    // Navbar Scroll Effect
    // ==========================================
    function initNavbarScroll() {
        const $window = $(window);
        const $navbar = $('#main-navbar');

        $window.on('scroll', function() {
            $navbar.toggleClass('scrolled', $window.scrollTop() > CONFIG.scroll.navbarThreshold);
        });
    }

    // ==========================================
    // Smooth Scroll
    // ==========================================
    function initSmoothScroll() {
        $('a[href^="#"]').on('click', function(e) {
            const $target = $($(this).attr('href'));
            if ($target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: $target.offset().top - CONFIG.animation.scrollOffset
                }, CONFIG.animation.duration);
            }
        });
    }

    // ==========================================
    // Back to Top Button
    // ==========================================
    function initBackToTop() {
        const $window = $(window);
        const $btn = $('#back-to-top');

        $window.on('scroll', function() {
            $btn.toggleClass('show', $window.scrollTop() > CONFIG.scroll.backToTopThreshold);
        });

        $btn.on('click', function(e) {
            e.preventDefault();
            $('html, body').animate({ scrollTop: 0 }, CONFIG.animation.duration);
        });
    }

    // ==========================================
    // Hero Slider
    // ==========================================
    function initHeroSlider() {
        const $slider = $('.hero-slider');
        if (!$slider.length) return;

        const $slides = $slider.find('.hero-slide');
        const $nav = $slider.find('.hero-nav');
        let currentSlide = 0;
        let slideInterval;

        function showSlide(index) {
            $slides.removeClass('active').fadeOut(0);
            $nav.find('.hero-dot').removeClass('active');

            currentSlide = ((index % $slides.length) + $slides.length) % $slides.length;
            $slides.eq(currentSlide).addClass('active').fadeIn(500);
            $nav.find('.hero-dot').eq(currentSlide).addClass('active');
        }

        function startSlider() {
            slideInterval = setInterval(() => showSlide(currentSlide + 1), CONFIG.slider.autoPlayDelay);
        }

        function stopSlider() {
            clearInterval(slideInterval);
        }

        // Create navigation dots
        $slides.each(function(i) {
            $nav.append(`<span class="hero-dot${i === 0 ? ' active' : ''}" data-slide="${i}"></span>`);
        });

        $nav.on('click', '.hero-dot', function() {
            stopSlider();
            showSlide($(this).data('slide'));
            startSlider();
        });

        $slider.on('mouseenter', stopSlider).on('mouseleave', startSlider);

        showSlide(0);
        startSlider();
    }

    // ==========================================
    // Slick Carousels
    // ==========================================
    function initCarousels() {
        const slickDefaults = {
            autoplay: true,
            pauseOnHover: true,
            responsive: [
                { breakpoint: 992, settings: { slidesToShow: 4 } },
                { breakpoint: 768, settings: { slidesToShow: 3 } },
                { breakpoint: 576, settings: { slidesToShow: 2 } }
            ]
        };

        if ($('.clients-carousel').length) {
            $('.clients-carousel').slick($.extend({}, slickDefaults, {
                slidesToShow: 5,
                slidesToScroll: 1,
                autoplaySpeed: CONFIG.slider.carouselSpeed,
                arrows: false,
                dots: false
            }));
        }

        if ($('.testimonial-slider').length) {
            $('.testimonial-slider').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: CONFIG.slider.autoPlayDelay,
                arrows: true,
                dots: true,
                prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-arrow-left"></i></button>',
                nextArrow: '<button type="button" class="slick-next"><i class="fas fa-arrow-right"></i></button>'
            });
        }
    }

    // ==========================================
    // Counter Animation
    // ==========================================
    function initCounters() {
        if (!('IntersectionObserver' in window)) return;

        function animateCounter($counter) {
            const target = parseInt($counter.data('target'), 10);
            const duration = CONFIG.animation.counterDuration;
            const step = target / (duration / 16);
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    $counter.text(target);
                    clearInterval(timer);
                } else {
                    $counter.text(Math.floor(current));
                }
            }, 16);
        }

        $('.counter').each(function() {
            const $counter = $(this);
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter($counter);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(this);
        });
    }

    // ==========================================
    // Form Validation (Bootstrap 5)
    // ==========================================
    function initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');

        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // ==========================================
    // Contact Form Handler
    // ==========================================
    function initContactForm() {
        $('#contactForm, #inquiryForm').on('submit', function(e) {
            e.preventDefault();

            const $form = $(this);
            const $btn = $form.find('button[type="submit"]');
            const originalText = $btn.html();

            $btn.prop('disabled', true).html(
                '<span class="spinner-border spinner-border-sm me-2"></span>Sending...'
            );

            $.ajax({
                url: $form.attr('action'),
                method: 'POST',
                data: $form.serialize(),
                success: function() {
                    $form[0].reset();
                    showAlert($form, 'success', 
                        '<i class="fas fa-check-circle me-2"></i>Thank you! Your message has been sent successfully.'
                    );
                },
                error: function() {
                    showAlert($form, 'danger',
                        '<i class="fas fa-exclamation-circle me-2"></i>Sorry, there was an error. Please try again later.'
                    );
                },
                complete: function() {
                    $btn.html(originalText).prop('disabled', false);
                }
            });
        });
    }

    // ==========================================
    // Newsletter Form Handler
    // ==========================================
    function initNewsletterForm() {
        $('#newsletterForm').on('submit', function(e) {
            e.preventDefault();

            const $form = $(this);
            const $email = $form.find('input[type="email"]');
            const email = $email.val().trim();

            if (!isValidEmail(email)) {
                alert('Please enter a valid email address.');
                return;
            }

            $.ajax({
                url: $form.attr('action'),
                method: 'POST',
                data: { email: email },
                success: function() {
                    $email.val('');
                    alert('Thank you for subscribing!');
                },
                error: function() {
                    alert('Please enter a valid email address.');
                }
            });
        });
    }

    // ==========================================
    // Lazy Load Images
    // ==========================================
    function initLazyLoad() {
        if (!('IntersectionObserver' in window)) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
    }

    // ==========================================
    // Active Nav Link
    // ==========================================
    function initActiveNav() {
        const currentPath = window.location.pathname;

        $('.navbar-nav .nav-link').each(function() {
            const href = $(this).attr('href');
            if (currentPath === href || (href !== '#' && currentPath.includes(href))) {
                $(this).addClass('active');
            }
        });
    }

    // ==========================================
    // Mobile Menu Close
    // ==========================================
    function initMobileMenu() {
        $('.navbar-nav .nav-link').on('click', function() {
            const $collapse = $('.navbar-collapse');
            if ($collapse.hasClass('show')) {
                $('.navbar-toggler').trigger('click');
            }
        });
    }

    // ==========================================
    // Utility Functions
    // ==========================================
    function showAlert($form, type, message) {
        $form.find('.alert').remove();
        $form.prepend(
            `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`
        );
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // ==========================================
    // Initialize All Modules
    // ==========================================
    $(document).ready(function() {
        ajaxSetup();
        initPreloader();
        initAOS();
        initNavbarScroll();
        initSmoothScroll();
        initBackToTop();
        initHeroSlider();
        initCarousels();
        initCounters();
        initFormValidation();
        initContactForm();
        initNewsletterForm();
        initLazyLoad();
        initActiveNav();
        initMobileMenu();
    });

})(jQuery);