from django.contrib import admin

# Register your models here.
from filterbank.models import Filter, ParsingRequest, Representation, NpArray, AImage, DiCom

admin.site.register(Filter)
admin.site.register(ParsingRequest)
admin.site.register(Representation)
admin.site.register(NpArray)
admin.site.register(AImage)
admin.site.register(DiCom)