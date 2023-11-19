from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interest.models import Interest
from interest.serializers import InterestSerializer


class ListInterestAPIView(APIView):
    def get(self, request: Request):
        interests = Interest.objects.all()

        return Response(data=InterestSerializer(interests, many=True).data)


class RetrieveInterestAPIView(APIView):
    def get(self, request: Request, interest_id: int):
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response({'error': f'Interest with {interest_id=} does not exist'}, status=400)

        return Response(InterestSerializer(interest).data)
