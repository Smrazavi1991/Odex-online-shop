from product.models import Category
from django.contrib.auth.models import Group
import jwt
from config.secrets import SECRET_KEY


def categories_cascade_deactivation_check():
    all_categories = Category.objects.all()
    for category1 in all_categories:
        if category1.sub:
            category2_id = category1.sub.id
            category2 = Category.objects.get(id=category2_id)
            if category2.sub:
                category3_id = category2.sub.id
                category3 = Category.objects.get(id=category3_id)
                if category3.is_deleted is True or category3.is_active is False:
                    category2.is_active = False
                    category2.save()
            if category2.is_deleted is True or category2.is_active is False:
                category1.is_active = False
                category1.save()


def identify_user_role(user_id: int):
    list_of_roles = []
    user_roles = Group.objects.filter(user__id=user_id)
    if not user_roles:
        list_of_roles = None
    else:
        for user_role in user_roles:
            list_of_roles.append(user_role.name)
    return list_of_roles


def create_jwt_token(payload: dict):
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return {'token': token.decode('utf-8')}
