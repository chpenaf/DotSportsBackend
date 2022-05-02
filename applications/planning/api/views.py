from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from applications.main.services import generate_request
from applications.locations.models import Location
from applications.schedule.models import Schedule, Schedule_Day, Schedule_Slot

from ..models import Calendar, Slot
from .serializers import CalendarSerializer, SlotSerializer


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

        return self.fill_calendar(location, begin_date=begin_date, end_date=end_date)

    def get(self, request: Request, id_location: int = None, year: int = None, month: int = None) -> Response:
        
        calendar_month = Calendar.objects.all().filter(
            location = Location.objects.all().filter( id = id_location ).first(),
            year = year,
            month = month
        )

        serializer = self.serializer_class(
            calendar_month,
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )
        
    def fill_calendar(self, location: Location, begin_date, end_date) -> Response:

        start = datetime.strptime(begin_date,'%Y-%m-%d')
        end = datetime.strptime(end_date,'%Y-%m-%d')
        delta = timedelta(days=1)

        holidays_list = self.get_holidays()

        calendar_all: Calendar = Calendar.objects.all().filter(
            location  = location
        )

        calendar_insert = list()

        while start <= end:

            for item in calendar_all:
                db_date = item.date.strftime('%Y-%m-%d')
                cur_date = start.strftime('%Y-%m-%d')
                if db_date == cur_date:
                    calendar_insert.append(item)
                    start += delta
                    continue

            schedule: Schedule = Schedule.objects.all().filter(
                location = location,
                begin_validity__lte = start,
                end_validity__gte = start,
            ).first()

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

            if schedule:
                schedule_day: Schedule_Day = Schedule_Day.objects.all().filter(
                    schedule = schedule,
                    daytype = day_type
                ).first()
                if schedule_day:
                    schedule_slots: list = Schedule_Slot.objects.all().filter(
                        schedule_day=schedule_day
                    )

                    for item in schedule_slots:
                        slot: Slot = Slot.objects.create(
                            calendar = calendar,
                            slot = item.slot,
                            starttime = item.starttime,
                            endtime = item.endtime
                        )
                        slot.save()

            start += delta

        serializer = self.serializer_class(
            calendar_insert,
            many=True
        )

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

class SlotView(APIView):

    def get(self, request, id_location=None, year=None, month=None, day=None, all=None):
        
        if id_location:
            location: Location = Location.objects.all().filter( id = id_location ).first()
        else:
            return Response(
                {
                    'ok':True,
                    'message':'Date'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if year and month and day:
            date = datetime(year,month,day)
        else:
            date = datetime.today().date()

        calendar: Calendar = Calendar.objects.all().filter(
            location=location,
            date=date
        ).first()

        if all == 1:
            slots = Slot.objects.all().filter(
                        calendar=calendar
                    )

        else:
            if date.date() == datetime.now().date():
                slots = Slot.objects.all().filter(
                        calendar=calendar,
                        starttime__gte=datetime.now().time()
                    )

            else:
                slots = Slot.objects.all().filter(
                            calendar=calendar
                        )

        serializer = SlotSerializer(
            slots,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
