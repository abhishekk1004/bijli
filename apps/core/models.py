from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.common.models import ActiveModel, SlugModel, SEOModel, OrderableModel
from apps.common.managers import ActiveManager
from apps.common.utils import upload_to, generate_unique_slug
from apps.common.choices import SocialPlatform


class CompanyInfo(ActiveModel):
    """Company information model."""

    company_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to=upload_to)
    favicon = models.ImageField(upload_to=upload_to, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    secondary_phone = models.CharField(max_length=30, blank=True)
    address = models.TextField()
    google_map = models.URLField(blank=True)
    copyright = models.CharField(max_length=255)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.company_name


class SocialMedia(ActiveModel):
    """Social media links model."""

    platform = models.CharField(max_length=30, choices=SocialPlatform.choices)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["order", "platform"]
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"

    def __str__(self):
        return self.get_platform_display()


class NavbarLink(ActiveModel, SlugModel, OrderableModel):
    """Navigation bar links."""

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    is_footer = models.BooleanField(default=False, help_text="Show in footer as well")

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["order"]
        verbose_name = "Navbar Link"
        verbose_name_plural = "Navbar Links"

    def __str__(self):
        return self.title


class FooterSection(OrderableModel):
    """Footer sections with links."""

    title = models.CharField(max_length=100)
    column = models.PositiveIntegerField(
        default=1,
        help_text="Footer column (1-4)",
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    links = models.ManyToManyField(NavbarLink, blank=True, related_name='footer_sections')

    class Meta:
        ordering = ["column", "order"]
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Sections"

    def __str__(self):
        return self.title


class HeroSlider(ActiveModel, OrderableModel):
    """Hero slider for homepage."""

    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_to)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=255, blank=True)
    is_fullscreen = models.BooleanField(default=False)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["order"]
        verbose_name = "Hero Slider"
        verbose_name_plural = "Hero Sliders"

    def __str__(self):
        return self.title


class Client(ActiveModel, OrderableModel):
    """Client/Partner logos."""

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=upload_to)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["order"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name


class Testimonial(ActiveModel):
    """Client testimonials."""

    client_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(
        default=5,
        help_text="Rating out of 5",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.company}"


class SEOSetting(SlugModel):
    """SEO settings for pages."""

    page_name = models.CharField(max_length=100, unique=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "SEO Setting"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return self.page_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'slug')
        super().save(*args, **kwargs)