# from typing import Union

# Number = Union[int, float]  # تعریف یک تایپ برای اعداد

def divide(a: int, b: int) -> float:
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("ورودی‌ها باید عدد باشند")
    if b == 0:
        raise ValueError("تقسیم بر صفر ممکن نیست")
    return a / b

def calculate_discount(price: int, discount_percent: int) -> float:
    if not isinstance(price, (int, float)) or not isinstance(discount_percent, (int, float)):
        raise TypeError("قیمت و درصد تخفیف باید عدد باشند")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("درصد تخفیف باید بین 0 تا 100 باشد")
    return price * (1 - discount_percent / 100)

# تست‌های مختلف
print(divide(10, 2))  # درست: 5.0
print(calculate_discount(1000, 20))  # درست: 800.0

# این‌ها خطا میدن
divide("10", 2)  # TypeError
calculate_discount(1000, 150)  # ValueError
