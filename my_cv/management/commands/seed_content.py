"""Seed the database with Mohammad's real portfolio content.

Idempotent: safe to run multiple times (uses update_or_create on natural keys).
Run with:  python manage.py seed_content
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from my_cv.models import (
    Certificate,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    SocialLink,
)

ABOUT = (
    "مسیر من از دنیای فروش و مدیریت دفتر شروع شد، اما در هر نقش، چیزی که همیشه جذبم "
    "می‌کرد «داده» بود — ساخت سیستم‌های اطلاعاتی، داشبوردهای مدیریتی و گزارش‌های "
    "تحلیلی. همین علاقه من را به علم داده، یادگیری ماشین و در نهایت مهندسی نرم‌افزار "
    "کشاند. امروز همان کاری را که سال‌ها به‌صورت دستی در کسب‌وکار انجام می‌دادم، با "
    "Python، Django و هوش مصنوعی، خودکار و مقیاس‌پذیر می‌سازم."
)

# (category_name, icon, order, [(skill, level, featured), ...])
SKILLS = [
    ("بک‌اند", "fas fa-server", 1, [
        ("Python", 5, True),
        ("Django", 5, True),
        ("PostgreSQL", 4, True),
        ("SQL Server", 3, True),
        ("اصول پایگاه داده", 4, True),
        ("REST API", 4, True),
    ]),
    ("هوش مصنوعی و داده", "fas fa-brain", 2, [
        ("LangChain", 4, True),
        ("RAG", 4, True),
        ("OpenAI API", 4, True),
        ("ChromaDB", 4, True),
        ("سیستم توصیه‌گر", 3, True),
        ("تحلیل داده", 4, True),
        ("Power BI", 3, True),
    ]),
    ("DevOps و ابزارها", "fas fa-cubes", 3, [
        ("Docker", 4, True),
        ("Git", 4, True),
        ("Liara", 4, True),
        ("n8n", 3, True),
        ("مبانی شبکه", 3, True),
    ]),
    ("وب‌اسکرپینگ", "fas fa-spider", 4, [
        ("BeautifulSoup", 4, True),
        ("Camoufox", 4, True),
        ("یکپارچه‌سازی API", 4, True),
    ]),
    ("مهارت‌های پایه", "fas fa-lightbulb", 5, [
        ("الگوریتم", 3, True),
        ("حل مسئله", 5, True),
        ("کار تیمی", 5, True),
        ("ارتباط مؤثر", 5, True),
    ]),
]

EXPERIENCES = [
    {
        "role": "مدیر داخلی انتشارات",
        "organization": "پژوهشکده مطالعات و تحقیقات بین‌الملل ابرار معاصر تهران",
        "location": "تهران",
        "period": "خرداد ۱۴۰۲ – اکنون",
        "is_current": True,
        "order": 1,
        "description": (
            "به‌عنوان کارشناس مالی، با تسلط بر اصول انبارداری و انبارگردانی یک سیستم "
            "ساختارمند ایجاد کردم که به جلوگیری از فساد در فروش و کاهش هزینه‌های "
            "انبارداری و تولید کمک کرد. مسئول ارائه‌ی گزارش‌های فروش به سطوح بالای "
            "مدیریتی بودم و با ساخت یک سیستم داده‌ی محصولات، تولید و فروش، اطلاعات دقیقی "
            "برای تصمیم‌گیری‌های استراتژیک فراهم کردم."
        ),
    },
    {
        "role": "منشی دفتر قاضی و مسئول دبیرخانه",
        "organization": "دادسرای نظامی جنوب‌غرب استان تهران",
        "location": "تهران",
        "period": "دی ۱۳۹۹ – آذر ۱۴۰۱",
        "is_current": False,
        "order": 2,
        "description": (
            "همزمان با دوران خدمت سربازی، درک عمیق‌تری از محیط‌های کاری اداری بزرگ و "
            "مسئولیت‌های حساس به دست آوردم که به دریافت تقدیرنامه از این سازمان منجر شد."
        ),
    },
    {
        "role": "دستیار داخلی حوزه‌ی افغانستان (بخش بین‌الملل)",
        "organization": "دفتر خبری ایران",
        "location": "تهران",
        "period": "اردیبهشت ۱۳۹۸ – آبان ۱۳۹۹",
        "is_current": False,
        "order": 3,
        "description": (
            "وظیفه‌ی نظارت و هماهنگی میان بخش‌های مختلف حوزه را بر عهده داشتم. در این "
            "دوره با داده و تحلیل داده‌ها و تهیه‌ی داشبوردهای مدیریتی برای گزارش به "
            "مدیران آشنا شدم — همین نقطه‌ی آغاز علاقه‌ام به علم داده و یادگیری ماشین بود."
        ),
    },
    {
        "role": "مسئول دفتر",
        "organization": "انجمن علوم سیاسی ایران",
        "location": "تهران",
        "period": "مهر ۱۳۹۷ – مرداد ۱۳۹۸",
        "is_current": False,
        "order": 4,
        "description": (
            "مدیریت برنامه‌ی ملاقات‌ها، برگزاری جلسات و همایش‌های داخلی و بین‌المللی و "
            "تنظیم مستندات اداری. این تجربه مهارت‌های سازماندهی و ارتباطی‌ام را تقویت کرد."
        ),
    },
]

# title -> dict (skills referenced by name; created above)
PROJECTS = [
    {
        "title": "دستیار دانش هوشمند (RAG)",
        "summary": "چت‌بات هوشمند روی کتاب‌های PDF دوزبانه (فارسی/انگلیسی) با خط‌لوله‌ی کامل RAG.",
        "category": Project.Category.AI,
        "status": Project.Status.COMPLETED,
        "problem": "پاسخ‌گویی دقیق به پرسش‌ها از روی محتوای تخصصیِ کتاب‌ها، نه دانش عمومی مدل.",
        "solution": (
            "یک خط‌لوله‌ی RAG ساختم: استخراج و قطعه‌بندی متن از PDF، تولید embedding با "
            "مدل text-embedding-3-large، ذخیره در پایگاه برداری ChromaDB و بازیابی متنی "
            "برای پاسخ‌گویی با GPT-4o-mini از طریق LangChain."
        ),
        "outcome": "پاسخ‌های متکی بر منبع و دوزبانه، با امکان گسترش به هر مجموعه‌سند دیگری.",
        "github_url": "https://github.com/Meska75/quera-LLM-project-2",
        "is_featured": True,
        "is_private": False,
        "order": 1,
        "skills": ["LangChain", "RAG", "OpenAI API", "ChromaDB", "Python"],
    },
    {
        "title": "سامانه‌ی تجمیع چند-فروشگاهی",
        "summary": "دسترسی بلادرنگ کاربران یک فروشگاه به کالای ۱۰ فروشگاه معتبر دیگر.",
        "category": Project.Category.BACKEND,
        "status": Project.Status.COMPLETED,
        "problem": (
            "یک فروشگاه می‌خواست کاربرانش در لحظه به کالای چندین فروشگاه معتبر دسترسی "
            "داشته باشند."
        ),
        "solution": (
            "دو مسیر تأمین داده طراحی کردم: برای فروشگاه‌های دارای API رسمی (باسلام و "
            "دیجی‌کالا) اتصال مستقیم API، و برای ۸ فروشگاه دیگر وب‌اسکرپینگ منظم. داده‌ها "
            "در PostgreSQL روی هاست Liara ذخیره می‌شدند تا سریع در دسترس کاربران باشند."
        ),
        "outcome": "تجمیع ۱۰ منبع فروشگاهی (۲ API رسمی + ۸ اسکرپینگ) با دسترسی بلادرنگ.",
        "is_featured": True,
        "is_private": True,
        "order": 2,
        "skills": ["Django", "PostgreSQL", "Camoufox", "یکپارچه‌سازی API", "Liara"],
    },
    {
        "title": "پلتفرم جمع‌آوری داده‌ی تیمی",
        "summary": "موتور Core سمت سرور + داشبورد تعریف تسک برای کارمندان یک شرکت.",
        "category": Project.Category.BACKEND,
        "status": Project.Status.COMPLETED,
        "problem": "نیاز یک شرکت به جمع‌آوری خودکار داده از سامانه‌های مختلف بر اساس تسک‌های تعریف‌شده.",
        "solution": (
            "به‌صورت تیمی یک موتور Core روی سرور و یک داشبورد وب ساختیم که کارمندان از "
            "طریق آن تسک تعریف می‌کردند؛ Core با ترکیب ۱ API رسمی و ۲ منبع وب‌اسکرپینگ "
            "(BeautifulSoup و Camoufox) داده را جمع‌آوری و ذخیره می‌کرد. چون هاست اجازه‌ی "
            "اجرای Camoufox را نمی‌داد، کل سرویس را Dockerize کردم."
        ),
        "outcome": "خودکارسازی جمع‌آوری داده با معماری Core + داشبورد و استقرار داکرایزشده.",
        "is_featured": False,
        "is_private": True,
        "order": 3,
        "skills": ["Python", "BeautifulSoup", "Camoufox", "Docker"],
    },
    {
        "title": "نرم‌افزار تحلیل داده‌ی فروش و توصیه‌گر هوشمند",
        "summary": "آنالیز داده‌های فروش با Python و نمایش در داشبورد همراه پیشنهادهای مبتنی بر AI.",
        "category": Project.Category.DATA,
        "status": Project.Status.COMPLETED,
        "problem": "تبدیل داده‌های خام فروش به بینش قابل‌اقدام و پیشنهادهای خرید برای کاربر.",
        "solution": (
            "داده‌های جمع‌آوری‌شده را با Python تحلیل می‌کردم، نتایج را در داشبورد به "
            "کاربر نشان می‌دادم و همان داده‌ها را برای تولید پیشنهاد به هوش مصنوعی "
            "می‌فرستادم (تحلیل رفتار کاربر برای راهنمایی خرید)."
        ),
        "outcome": "نرم‌افزار تحلیل فروش با لایه‌ی توصیه‌گر هوشمند.",
        "is_featured": False,
        "is_private": True,
        "order": 4,
        "skills": ["Python", "تحلیل داده", "سیستم توصیه‌گر"],
    },
    {
        "title": "وب‌سایت مطب دکتر وحید عبدالرحیمی",
        "summary": "وب‌سایت کامل و سه‌زبانه‌ی یک پزشک با Django، مستقرشده روی Liara.",
        "category": Project.Category.WEB,
        "status": Project.Status.IN_PROGRESS,
        "problem": "نیاز یک پزشک به وب‌سایت حرفه‌ای و چندزبانه برای معرفی خدمات و ارتباط با بیماران.",
        "solution": (
            "یک سایت کامل با Django شامل سیستم حساب کاربری، بلاگ، گالری، صفحات خدمات و تیم "
            "طراحی و توسعه دادم و آن را روی Liara مستقر کردم. سایت سه‌زبانه است. فاز بعدی، "
            "افزودن یک دستیار هوش مصنوعی برای راهنمایی بیماران، کمک به تعیین وقت و کمک به "
            "ادمین‌ها در تولید محتوای چندزبانه است."
        ),
        "outcome": "سایت سه‌زبانه‌ی مستقرشده؛ دستیار هوش مصنوعی در دست توسعه.",
        "github_url": "https://github.com/Meska75/drvahidabdolrahimi",
        "is_featured": False,
        "is_private": False,
        "order": 5,
        "skills": ["Django", "Liara"],
    },
]

# (title, issuer, instructor, year, hours, category)
CERTIFICATES = [
    ("آموزش Docker برای برنامه‌نویس‌ها و مهندسین DevOps", "", "", "", None, Certificate.Category.BACKEND),
    ("آموزش جنگو Django", "", "", "", None, Certificate.Category.BACKEND),
    ("آموزش اصول پایگاه داده و SQL Server", "", "", "", None, Certificate.Category.BACKEND),
    ("آموزش درک برنامه‌نویسی", "مکتب‌خونه", "جادی میرمیرانی", "۱۴۰۲", 17, Certificate.Category.BACKEND),
    ("آموزش پایتون مقدماتی", "مکتب‌خونه", "جادی میرمیرانی", "۱۴۰۲", 57, Certificate.Category.BACKEND),
    ("مقدمه‌ای بر الگوریتم و برنامه‌نویسی", "مجتمع فنی تهران", "", "۱۴۰۱", 38, Certificate.Category.BACKEND),
    ("آموزش درک مقدماتی شبکه", "", "", "", None, Certificate.Category.BACKEND),
    ("ساخت اپلیکیشن‌های LLM", "", "", "", None, Certificate.Category.AI_DATA),
    ("دوره‌ی یک‌ساله‌ی طراحی و نمونه‌سازی محصولات هوش مصنوعی و اینترنت اشیا (AIoT)",
     "مرکز تحقیقاتی چیتا، دانشگاه تهران", "", "۱۴۰۲", None, Certificate.Category.AI_DATA),
    ("طراحی داشبوردهای هوش تجاری با Power BI", "مجتمع فنی تهران", "", "۱۴۰۲", 24, Certificate.Category.AI_DATA),
    ("آموزش اتوماسیون با n8n", "", "", "", None, Certificate.Category.AI_DATA),
    ("آموزش اکسل کاربردی", "مکتب‌خونه", "سجاد شکوهیار", "۱۴۰۱", 20, Certificate.Category.AI_DATA),
    ("ICDL Level 2", "مجتمع فنی تهران", "", "۱۴۰۱", 63, Certificate.Category.OTHER),
    ("آموزش عملی کار با آردوینو (برنامه‌نویسی میکروکنترلرها)", "", "", "", None, Certificate.Category.OTHER),
]

SOCIAL_LINKS = [
    ("GitHub", "https://github.com/Meska75", "fab fa-github", 1),
    ("LinkedIn", "https://www.linkedin.com/", "fab fa-linkedin", 2),
    ("Email", "mailto:mohammad.eska34@gmail.com", "fas fa-envelope", 3),
]


class Command(BaseCommand):
    help = "Seed the database with the real portfolio content (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        Profile.objects.update_or_create(
            full_name="محمد اسکندرلو",
            defaults={
                "headline": "مهندس بک‌اند پایتون/جنگو و هوش مصنوعی",
                "tagline": "ساخت پلتفرم‌های داده‌محور و هوشمند — از جمع‌آوری داده تا لایه‌ی هوش مصنوعی.",
                "about": ABOUT,
                "location": "تهران",
                "email": "mohammad.eska34@gmail.com",
                "phone": "09198298159",
                "show_phone": False,
                "available_for_work": True,
            },
        )

        for label, url, icon, order in SOCIAL_LINKS:
            SocialLink.objects.update_or_create(
                label=label, defaults={"url": url, "icon": icon, "order": order})

        skill_by_name = {}
        for cat_name, icon, order, skills in SKILLS:
            category, _ = SkillCategory.objects.update_or_create(
                name=cat_name, defaults={"icon": icon, "order": order})
            for s_order, (s_name, level, featured) in enumerate(skills, start=1):
                skill, _ = Skill.objects.update_or_create(
                    category=category, name=s_name,
                    defaults={"level": level, "featured": featured, "order": s_order})
                skill_by_name[s_name] = skill

        for exp in EXPERIENCES:
            Experience.objects.update_or_create(
                role=exp["role"], organization=exp["organization"],
                defaults={k: v for k, v in exp.items() if k not in ("role", "organization")})

        for p in PROJECTS:
            skills = p.pop("skills", [])
            project, _ = Project.objects.update_or_create(
                title=p["title"],
                defaults={k: v for k, v in p.items() if k != "title"})
            resolved = [skill_by_name[name] for name in skills if name in skill_by_name]
            project.skills.set(resolved)

        for order, (title, issuer, instructor, year, hours, category) in enumerate(CERTIFICATES, start=1):
            Certificate.objects.update_or_create(
                title=title,
                defaults={"issuer": issuer, "instructor": instructor, "year": year,
                          "hours": hours, "category": category, "order": order})

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {Profile.objects.count()} profile, {Skill.objects.count()} skills, "
            f"{Experience.objects.count()} experiences, {Project.objects.count()} projects, "
            f"{Certificate.objects.count()} certificates, {SocialLink.objects.count()} social links."
        ))
