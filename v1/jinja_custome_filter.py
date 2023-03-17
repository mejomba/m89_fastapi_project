import routers.posts
import routers.auth
import jalali_date


def to_jalali(date_obj):
    return jalali_date.Gregorian(date_obj).persian_string("{}/{}/{}")


routers.posts.template.env.filters.update({'to_jalali': to_jalali})
routers.auth.template.env.filters.update({'to_jalali': to_jalali})
