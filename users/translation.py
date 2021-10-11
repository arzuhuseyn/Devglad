from modeltranslation.translator import register, TranslationOptions

from users.models import UserProfile


@register(UserProfile)
class UserProfileTranslation(TranslationOptions):
    fields = ('bio',)