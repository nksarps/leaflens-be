from django.contrib import admin
from predict.models import DiseasePrediction


class DiseasePredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'prediction', 'timestamp')
    readonly_fields = ('timestamp',)


admin.site.register(DiseasePrediction, DiseasePredictionAdmin)