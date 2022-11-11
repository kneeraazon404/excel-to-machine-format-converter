from django.contrib import admin

from course.models import Store, Profile, StoreNumber, MarketId, TerminalId

# Register your models here.
# admin.site.register(Test)
admin.site.register(Store)
admin.site.register(Profile)
admin.site.register(StoreNumber)
admin.site.register(MarketId)
admin.site.register(TerminalId)
