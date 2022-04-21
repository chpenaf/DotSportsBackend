from datetime import datetime
from dateutil.relativedelta import relativedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.employees.models import Employee
from applications.locations.models import Location
from applications.members.models import Member
from applications.users.models import User

from ..models import Credit_Header, Credit_Pos
from .serializers import CreditHeaderSerializer

class CreditView(APIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = CreditHeaderSerializer

    def post(self, request: Request) -> Response:

        data = request.data
                    
        user: User = request.user
        if user:
            employee = Employee.objects.all().filter(
                doc_num = user.doc_num
            ).first()

        if data.get('location'):
            location = Location.objects.all().filter(
                id = request.data.get('location')
            ).first()

        if data.get('member'):
            member = Member.objects.all().filter(
                id = request.data.get('member')
            ).first()

        if data.get('begin_validity'):
            begin_validity = datetime.strptime(
                                request.data.get('begin_validity'),
                                '%Y-%m-%d')

        end_validity = ( begin_validity + relativedelta( months = +1 ) ).date()

        
        header: Credit_Header = Credit_Header.objects.create(
            location=location,
            member=member,
            quantity=request.data.get('quantity'),
            status=Credit_Header.ACTIVE,
            begin_validity=begin_validity,
            end_validity=end_validity,
            entered_by=employee,
            doc_ref=request.data.get('doc_ref'),
        )

        header.save()

        quantity: int = int(header.quantity)
        
        for index in range(quantity):
            pos: Credit_Pos = Credit_Pos.objects.create(
                header = header,
                pos = index + 1,
                begin_validity = begin_validity,
                end_validity = end_validity,
                status = Credit_Pos.AVAILABLE
            )
            pos.save()
        
        result = self.serializer_class(
            Credit_Header.objects.all().filter( id = header.id ).first()
        )
        
        return Response(
            result.data,
            status=status.HTTP_200_OK
        )
    

    def get(self, request: Request, id_member: int = None) -> Response:

        if( id_member ):
            member = Member.objects.all().filter(
                id = id_member
            ).first()

            serializer = self.serializer_class(
                Credit_Header.objects.all().filter( 
                    member = member,
                    status = Credit_Header.ACTIVE
                ),
                many=True
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok':False,
                    'message':'ID member required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
def get_quant_credits(request: Request, id_member: int) -> Response:

    member: Member = Member.objects.all().filter(
        id = id_member
    ).first()

    result: int = 0

    if member:
        headers_list: list = Credit_Header.objects.all().filter(
            member = member,
            status = Credit_Header.ACTIVE
        )

        for header in headers_list:
            positions: list = Credit_Pos.objects.all().filter(
                header = header,
                used_at = None
            )
            result += len(positions)
        
        return Response(
            {
                'ok': True,
                'message': 'Correct',
                'quantity': result
            }, status= status.HTTP_200_OK
        )

    
    else:
        return Response(
            {
                'ok': False,
                'message': 'Member not found'
            }, status= status.HTTP_404_NOT_FOUND
        )