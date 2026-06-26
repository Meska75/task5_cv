from django.db import models
from django.utils.text import slugify


def _unicode_slug(value):
    """Slugify keeping Persian characters readable in URLs."""
    return slugify(value, allow_unicode=True)


class Profile(models.Model):
    """Single-row site identity / hero content."""

    full_name = models.CharField('نام کامل', max_length=120)
    headline = models.CharField('عنوان شغلی', max_length=160,
                                help_text='مثلاً: مهندس بک‌اند پایتون و هوش مصنوعی')
    tagline = models.CharField('شعار کوتاه', max_length=255, blank=True)
    about = models.TextField('درباره‌ی من', blank=True)
    location = models.CharField('محل سکونت', max_length=120, blank=True)
    email = models.EmailField('ایمیل', blank=True)
    phone = models.CharField('تلفن', max_length=40, blank=True)
    show_phone = models.BooleanField('نمایش عمومی تلفن', default=False)
    photo = models.ImageField('عکس', upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField('فایل رزومه', upload_to='resume/', blank=True, null=True)
    available_for_work = models.BooleanField('آماده‌ی همکاری', default=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'

    def __str__(self):
        return self.full_name


class SocialLink(models.Model):
    """Social / contact links shown in the contact section and footer."""

    label = models.CharField('عنوان', max_length=60)
    url = models.URLField('لینک')
    icon = models.CharField('کلاس آیکن', max_length=60, blank=True,
                            help_text='مثلاً: fab fa-github')
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'لینک اجتماعی'
        verbose_name_plural = 'لینک‌های اجتماعی'

    def __str__(self):
        return self.label


class SkillCategory(models.Model):
    name = models.CharField('نام دسته', max_length=80)
    slug = models.SlugField('اسلاگ', max_length=90, unique=True, blank=True, allow_unicode=True)
    icon = models.CharField('کلاس آیکن', max_length=60, blank=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'دسته‌ی مهارت'
        verbose_name_plural = 'دسته‌های مهارت'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unicode_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE,
                                 related_name='skills', verbose_name='دسته')
    name = models.CharField('نام مهارت', max_length=80)
    # 1..5 self-assessed proficiency; optional.
    level = models.PositiveSmallIntegerField('سطح (۱ تا ۵)', default=3)
    featured = models.BooleanField('نمایش در بخش مهارت‌ها', default=True,
                                   help_text='اگر خاموش باشد فقط به‌عنوان تگ پروژه استفاده می‌شود.')
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return self.name


class Experience(models.Model):
    role = models.CharField('عنوان شغلی', max_length=160)
    organization = models.CharField('سازمان', max_length=160)
    location = models.CharField('مکان', max_length=120, blank=True)
    period = models.CharField('بازه‌ی زمانی', max_length=120,
                              help_text='متن نمایشی، مثلاً: خرداد ۱۴۰۲ – اکنون')
    start_date = models.DateField('تاریخ شروع (برای مرتب‌سازی)', null=True, blank=True)
    is_current = models.BooleanField('شغل فعلی', default=False)
    description = models.TextField('توضیحات', blank=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'تجربه‌ی کاری'
        verbose_name_plural = 'تجربه‌های کاری'

    def __str__(self):
        return f'{self.role} — {self.organization}'


class Project(models.Model):
    class Category(models.TextChoices):
        AI = 'ai', 'هوش مصنوعی'
        BACKEND = 'backend', 'بک‌اند'
        DATA = 'data', 'داده'
        WEB = 'web', 'وب'

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'تکمیل‌شده'
        IN_PROGRESS = 'in_progress', 'در حال توسعه'

    title = models.CharField('عنوان', max_length=160)
    slug = models.SlugField('اسلاگ', max_length=180, unique=True, blank=True, allow_unicode=True)
    summary = models.CharField('خلاصه‌ی یک‌خطی', max_length=255)
    # Case-study structure.
    problem = models.TextField('مشکل', blank=True)
    solution = models.TextField('راه‌حل', blank=True)
    outcome = models.TextField('نتیجه', blank=True)
    category = models.CharField('دسته', max_length=20, choices=Category.choices, default=Category.BACKEND)
    status = models.CharField('وضعیت', max_length=20, choices=Status.choices, default=Status.COMPLETED)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True, verbose_name='تک‌استک')
    cover_image = models.ImageField('تصویر کاور', upload_to='projects/', blank=True, null=True)
    github_url = models.URLField('لینک گیت‌هاب', blank=True)
    live_url = models.URLField('لینک زنده', blank=True)
    is_private = models.BooleanField('پروژه‌ی خصوصی (بدون افشای کد)', default=False)
    is_featured = models.BooleanField('شاخص', default=False)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', '-is_featured']
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unicode_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    class Category(models.TextChoices):
        BACKEND = 'backend', 'بک‌اند'
        AI_DATA = 'ai_data', 'هوش مصنوعی و داده'
        OTHER = 'other', 'سایر'

    title = models.CharField('عنوان دوره', max_length=200)
    issuer = models.CharField('برگزارکننده', max_length=160, blank=True)
    instructor = models.CharField('مدرس', max_length=120, blank=True)
    year = models.CharField('سال', max_length=20, blank=True)
    hours = models.PositiveIntegerField('ساعت', null=True, blank=True)
    category = models.CharField('دسته', max_length=20, choices=Category.choices, default=Category.OTHER)
    url = models.URLField('لینک مدرک', blank=True)
    image = models.ImageField('تصویر مدرک', upload_to='certificates/', blank=True, null=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'گواهینامه'
        verbose_name_plural = 'گواهینامه‌ها'

    def __str__(self):
        return self.title
