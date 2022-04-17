from datetime import datetime, timedelta, date
from typing import Optional

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from applications.main.services import generate_request
from applications.locations.models import Location
from applications.schedule.models import Schedule, Schedule_Day

from ..models import Calendar
from .serializers import CalendarSerializer

class HolidayType:
    nombre: Optional[str]
    comentarios: Optional[str]
    fecha: Optional[str]
    irrenunciable: Optional[str]
    tipo: Optional[str]

    def __init__(self, nombre, comentarios, fecha, irrenunciable, tipo):
        self.nombre = nombre
        self.comentarios = comentarios
        self.fecha = fecha
        self.irrenunciable = irrenunciable
        self.tipo = tipo

class CalendarView(APIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = CalendarSerializer

    def post(self,request: Request) -> Response:
        
        if request.data.get('location'):
            id_location = request.data.get('location')

        else:
            return Response(
                {
                    'ok':False,
                    'message':'Location is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('begin_date'):
            begin_date = request.data.get('begin_date')
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Begin Date is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.data.get('end_date'):
            end_date = request.data.get('end_date')
        else:
            return Response(
                {
                    'ok':False,
                    'message':'End Date is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        location: Location = Location.objects.all().filter( id = id_location ).first()
        
        if not location:
            return Response(
                {
                    'ok':False,
                    'message':'Location not found'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        start = datetime.strptime(begin_date,'%Y-%m-%d')
        end = datetime.strptime(end_date,'%Y-%m-%d')
        delta = timedelta(days=1)

        holidays_list = self.get_holidays()

        calendar_all: Calendar = Calendar.objects.all().filter(
            location  = location
        )

        schedule: Schedule = Schedule.objects.all().filter(
            location = location,
            begin_validity__lte = start,
            end_validity__gte = end,
        ).first()

        calendar_insert = list()

        while start <= end:

            for item in calendar_all:
                db_date = item.date.strftime('%Y-%m-%d')
                cur_date = start.strftime('%Y-%m-%d')
                if db_date == cur_date:
                    calendar_insert.append(item)
                    start += delta
                    continue            

            day_week = start.weekday() + 1
            day_type = Schedule_Day.WEEKDAY
            is_holiday = False

            for holiday in holidays_list:
                if holiday['fecha'] == start.strftime('%Y-%m-%d'):
                    is_holiday = True
            
            if day_week >= 1 and day_week <= 5:
                day_type = Schedule_Day.WEEKDAY
            
            if day_week == 6:
                day_type = Schedule_Day.SATURDAY

            if day_week == 7:
                day_type = Schedule_Day.SUNDAY
            
            if is_holiday:
                day_type = Schedule_Day.HOLIDAY

            calendar = Calendar.objects.create(
                location = location,
                schedule = schedule,
                date = start.date(),
                year = start.year,
                month = start.month,
                day = start.day,
                daytype = day_type,
                day_week = day_week,
                day_label = day_week,
                month_label = start.month,
                holiday = is_holiday
            )

            calendar_insert.append(calendar)

            start += delta

        serializer = self.serializer_class(
            calendar_insert,
            many=True
        )

        print(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


    def get_holidays(self, year=None):
                
        if year:
            param = year
        else:
            param = datetime.today().year

        url = 'https://apis.digital.gob.cl/fl/feriados/{0}/'.format(param)

        response = generate_request(url, {})

        holidays_json = response

        holidays_list = list()

        for item in holidays_json:
            holiday = {
                'nombre': item['nombre'],
                'comentarios': item['comentarios'],
                'fecha': item['fecha'],
                'irrenunciable': item['irrenunciable'],
                'tipo': item['tipo']
            }   
            
            holidays_list.append(holiday)

        return holidays_list
        
    
    



