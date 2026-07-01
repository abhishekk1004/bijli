/**
 * CTS - Celltronic Tele Solutions
 * Main JavaScript File
 */

(function($) {
    'use strict';

    // ==========================================
    // 1. Preloader
    // ==========================================
    $(window).on('load', function() {
        $('#preloader').fadeOut('slow', function() {
            $(this).remove();
        });
    });

    // ==========================================
    // 2. Initialize AOS Animation
    // ==========================================
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        offset: 100
    });

    // ==========================================
    // 3. Navbar Scroll Effect
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('#main-navbar').addClass('scrolled');
        } else {
            $('#main-navbar').removeClass('scrolled');
        }
    });

    // ==========================================
    // 4. Smooth Scroll
    // ==========================================
    $('a[href^="#"]').on('click', function(e) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            var offset = 80; // Account for fixed navbar
            $('html, body').stop().animate({
                scrollTop: target.offset().top - offset
            }, 800, 'swing');
        }
    });

    // ==========================================
    // 5. Back to Top Button
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').addClass('show');
        } else {
            $('#back-to-top').removeClass('show');
        }
    });

    $('#back-to-top').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 800);
        return false;
    });

    // ==========================================
    // 6. Hero Slider
    // ==========================================
    if ($('.hero-slider').length) {
        var $slider = $('.hero-slider');
        var $slides = $slider.find('.hero-slide');
        var $nav = $slider.find('.hero-nav');
        var currentSlide = 0;
        var slideInterval;

        function showSlide(index) {
            $slides.removeClass('active').fadeOut(0);
            $nav.find('.hero-dot').removeClass('active');
            
            currentSlide = index;
            if (currentSlide >= $slides.length) currentSlide = 0;
            if (currentSlide < 0) currentSlide = $slides.length - 1;
            
            $($slides[currentSlide]).addClass('active').fadeIn(500);
            $($nav.find('.hero-dot')[currentSlide]).addClass('active');
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function startSlider() {
            slideInterval = setInterval(nextSlide, 5000);
        }

        function stopSlider() {
            clearInterval(slideInterval);
        }

        // Create navigation dots
        $slides.each(function(index) {
            $nav.append('<span class="hero-dot' + (index === 0 ? ' active' : '') + '" data-slide="' + index + '"></span>');
        });

        // Dot click handler
        $nav.on('click', '.hero-dot', function() {
            stopSlider();
            showSlide($(this).data('slide'));
            startSlider();
        });

        // Start slider
        showSlide(0);
        startSlider();

        // Pause on hover
        $slider.on('mouseenter', stopSlider);
        $slider.on('mouseleave', startSlider);
    }

    // ==========================================
    // 7. Client Logo Carousel
    // ==========================================
    if ($('.clients-carousel').length) {
        $('.clients-carousel').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 2000,
            arrows: false,
            dots: false,
            pauseOnHover: true,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 4
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 576,
                    settings: {
                        slidesToShow: 2
                    }
                }
            ]
        });
    }

    // ==========================================
    // 8. Testimonial Slider
    // ==========================================
    if ($('.testimonial-slider').length) {
        $('.testimonial-slider').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 5000,
            arrows: true,
            dots: true,
            prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-arrow-left"></i></button>',
            nextArrow: '<button type="button" class="slick-next"><i class="fas fa-arrow-right"></i></button>'
        });
    }

    // ==========================================
    // 9. Counter Animation
    // ==========================================
    function animateCounter($counter) {
        var target = parseInt($counter.data('target'));
        var duration = 2000;
        var step = target / (duration / 16);
        var current = 0;
        
        var timer = setInterval(function() {
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
        var $counter = $(this);
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter($counter);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(this);
    });

    // ==========================================
    // 10. Form Validation
    // ==========================================
    (function() {
        'use strict';
        
        var forms = document.querySelectorAll('.needs-validation');
        
        Array.prototype.slice.call(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

    // ==========================================
    // 11. Contact Form Submission
    // ==========================================
    $('#contactForm, #inquiryForm').on('submit', function(e) {
        e.preventDefault();
        
        var $form = $(this);
        var $submitBtn = $form.find('button[type="submit"]');
        var originalText = $submitBtn.html();
        
        // Show loading state
        $submitBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Sending...').prop('disabled', true);
        
        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            data: $form.serialize(),
            success: function(response) {
                $form[0].reset();
                $form.find('.alert').remove();
                $form.prepend('<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                    '<i class="fas fa-check-circle me-2"></i>' +
                    'Thank you! Your message has been sent successfully.' +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                    '</div>');
            },
            error: function() {
                $form.find('.alert').remove();
                $form.prepend('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                    '<i class="fas fa-exclamation-circle me-2"></i>' +
                    'Sorry, there was an error. Please try again later.' +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                    '</div>');
            },
            complete: function() {
                $submitBtn.html(originalText).prop('disabled', false);
            }
        });
    });

    // ==========================================
    // 12. Lazy Load Images
    // ==========================================
    if ('IntersectionObserver' in window) {
        var lazyImages = document.querySelectorAll('img[data-src]');
        
        var imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }

    // ==========================================
    // 13. Active Nav Link
    // ==========================================
    var currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        var $link = $(this);
        var href = $link.attr('href');
        
        if (currentPath === href || currentPath.indexOf(href) !== -1) {
            $link.addClass('active');
        }
    });

    // ==========================================
    // 14. Close Mobile Menu on Click
    // ==========================================
    $('.navbar-nav .nav-link').on('click', function() {
        if ($('.navbar-collapse').hasClass('show')) {
            $('.navbar-toggler').trigger('click');
        }
    });

    // ==========================================
    // 15. Newsletter Form
    // ==========================================
    $('#newsletterForm').on('submit', function(e) {
        e.preventDefault();
        
        var $form = $(this);
        var $email = $form.find('input[type="email"]');
        
        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            data: { email: $email.val() },
            success: function() {
                $email.val('');
                alert('Thank you for subscribing!');
            },
            error: function() {
                alert('Please enter a valid email address.');
            }
        });
    });

})(jQuery);