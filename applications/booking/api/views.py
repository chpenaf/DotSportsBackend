from datetime import datetime

from django.db.models import QuerySet

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.config.models import CapacityPool
from applications.courses.models import CourseSession
from applications.credits.models import Credit_Header, Credit_Pos
from applications.locations.models import Location, Pool
from applications.members.models import Member
from applications.planning.models import Calendar, Slot

from ..models import Booking
from .serializers import ( 
    BookingSerializer,
    BookingListSerializer
)

class BookingView(APIView):

    serializer_class = BookingSerializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self, pk: int = None, id_member: int = None) -> QuerySet:

        if pk:
            return Booking.objects.all().filter( id = pk ).first()
        elif id_member:
            return Booking.objects.all().filter(
                member = Member.objects.all().filter( id = id_member ).first()
            )
        else:
            return Booking.objects.all()
    

    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(
            data=request.data,
            context={'data':request.data,'request':request}
        )

        if serializer.is_valid():

            member: Member = serializer.validated_data.get('member')
            calendar: Calendar = serializer.validated_data.get('calendar')
            slot: Slot = serializer.validated_data.get('slot')
            location: Location = serializer.validated_data.get('location')
            pool: Pool = serializer.validated_data.get('pool')

            # Valida que la reserva no sea en el pasado
            if slot.calendar.date < datetime.now().date():
                return Response( 
                    {
                        'ok': False,
                        'message': 'No puede reservar en dias pasados'
                    }, status.HTTP_400_BAD_REQUEST
                )

            if slot.starttime < datetime.now().time():
                return Response( 
                    {
                        'ok': False,
                        'message': 'No puede horas pasadas'
                    }, status.HTTP_400_BAD_REQUEST
                )

            # Valida que no tenga reserva en ese mismo bloque
            found: Booking = Booking.objects.all().filter(
                member = member,
                slot = slot
            ).first()

            if found:
                return Response( 
                    {
                        'ok': False,
                        'message': 'Ya posee una reserva en ese bloque para ese día'
                    }, status.HTTP_400_BAD_REQUEST
                )

            # Valida Aforo
            capacity_pool: CapacityPool = CapacityPool.objects.all().filter(
                location = location,
                pool = pool,
                begin_validity__lte = datetime.now().date(),
                end_validity__gte = datetime.now().date()
            ).first()

            course_sessions = CourseSession.objects.all().filter(
                date=calendar,
                slot=slot
            )           

            current_people = Booking.objects.all().filter(
                calendar=calendar,
                slot=slot,
                location=location,
                pool=pool
            )

            max_capacity = ( pool.lanes - course_sessions.__len__() ) * capacity_pool.capacity_lane
            current = current_people.__len__()

            capacity_available = max_capacity - current

            if capacity_available <= 0:

                return Response( 
                    {
                        'ok': False,
                        'message': 'Aforo completo'
                    }, status.HTTP_400_BAD_REQUEST
                )

            # Valida que tenga creditos disponibles
            header: Credit_Header = Credit_Header.objects.all().filter(
                location = location,
                member = member,
                status = Credit_Header.ACTIVE,
                end_validity__gte = datetime.now().date()
            ).order_by('begin_validity').first()

            if not header:
                return Response( 
                    {
                        'ok': False,
                        'message': 'No tiene creditos disponibles'
                    }, status.HTTP_400_BAD_REQUEST
                )

            pos: Credit_Pos = Credit_Pos.objects.all().filter(
                header=header,
                status=Credit_Pos.AVAILABLE
            ).order_by('pos').first()

            if not pos:
                header.status = Credit_Header.FINISHED
                header.save()
                return Response(
                    {
                        'ok': False,
                        'message': 'No tiene creditos disponibles'
                    }, status.HTTP_400_BAD_REQUEST
                )

            # Genera la reserva
            serializer.save()

            booking: Booking = serializer.instance
            booking.credit_header = header
            booking.credit_pos = pos
            booking.save()

            pos.status = Credit_Pos.RESERVED
            pos.used_at = booking.calendar.date
            pos.save()

            # Valida si le quedan mas creditos disponibles posterior a esta reserva
            check_pos =  Credit_Pos.objects.all().filter(
                header=header,
                status=Credit_Pos.AVAILABLE
            ).order_by('pos').first()

            if not check_pos:
                header.status = Credit_Header.FINISHED
                header.save()


            return Response(
                {
                    'ok': True,
                    'message': 'Hora reservada correctamente'
                }, status.HTTP_200_OK
            )

        else:

            return Response(
                {
                   'ok': False,
                   'message': serializer.errors
                }, status.HTTP_400_BAD_REQUEST
            )

    def get(self, request: Request, id_member: int = None) -> Response:

        serializer = BookingListSerializer(
            Booking.objects.all().filter(
                    member = Member.objects.all().filter( id = id_member ).first()
            ).order_by('id'),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )