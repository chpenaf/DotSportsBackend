from django.urls import path

from .views import CalendarView, SlotView

urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('<int:id_location>/calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='calendar-month'),
    path('<int:id_location>/calendar/<int:year>/<int:month>/<int:day>/<int:all>/', SlotView.as_view(), name='slots_all'),
    path('<int:id_location>/calendar/<int:year>/<int:month>/<int:day>/slots/', SlotView.as_view(), name='slots')
]
