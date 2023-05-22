from product.models import Category


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
