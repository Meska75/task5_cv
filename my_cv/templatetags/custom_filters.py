# در پوشه templatetags یک فایل به نام custom_filters.py بسازید
# مسیر: your_app/templatetags/custom_filters.py

from django import template
from datetime import date

register = template.Library()

@register.filter
def calculate_age(birth_date):
    """
    محاسبه سن از روی تاریخ تولد
    """
    if not birth_date:
        return 0
    
    today = date.today()
    age = today.year - birth_date.year
    
    # بررسی اینکه آیا تولد امسال گذشته یا نه
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


@register.filter
def to_persian_numbers(number):
    """
    تبدیل اعداد انگلیسی به فارسی
    """
    persian_digits = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    
    return ''.join(persian_digits.get(char, char) for char in str(number))

@register.inclusion_tag("certificates.html")
def show_certificates(certificates):
    return {"certificates": certificates}
