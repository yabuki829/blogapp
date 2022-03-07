
from unicodedata import category

from app.models import Category
from sympy import content
def common(request):
    category_data = Category.objects.all
    content = {
        "category_data":category_data
    }
    return content