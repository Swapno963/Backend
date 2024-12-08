from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from .serializers import ServiceLocationSerializer, FavouriteSerializer
from .models import ServiceLocation, Favourite
from rest_framework.permissions import  IsAuthenticated
from .serializers import ServiceLocationSerializer, FavouriteSerializer, CardSerializer
from .models import ServiceLocation, Favourite, Card
from rest_framework.decorators import action
from decimal import Decimal



class ServiceLoactionView(viewsets.ViewSet):
	serializer_class = ServiceLocationSerializer
	
	def get_queryset(self):
		return ServiceLocation.objects.all()

	@extend_schema(
		description = 'get all service locations list',
		responses={200:ServiceLocationSerializer(many=True)}
		)
	def list(self, request):
		queryset = self.get_queryset()
		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class FavouriteView(viewsets.ModelViewSet):
	serializer_class = FavouriteSerializer
	permission_classes = [IsAuthenticated]
	http_method_names = ['get', 'post', 'delete']
	
	def get_queryset(self):
		return Favourite.objects.filter(user=self.request.user)

	@extend_schema(
		description = 'get list of all favourite cards of a logged in user',
		responses={200:ServiceLocationSerializer(many=True)}
		)
	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)



class CardView(viewsets.ViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.all()


    @extend_schema(
        description='Get list of all cards',
        responses={200: CardSerializer(many=True)}
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Get list of all featured cards',
        responses={200: CardSerializer(many=True)}
    )


    @action(detail=False, methods=['get'], url_path='featured')
    def featured_card(self, request):
        queryset = self.get_queryset().filter(is_feature=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




    @extend_schema(
        description='Get list of cards with filtering options',
        responses={200: CardSerializer(many=True)},
        parameters=[
            OpenApiParameter('location', str, location='query', description='Filter by location'),
            OpenApiParameter('min_price', str, location='query', description='Filter by minimum price'),
            OpenApiParameter('max_price', str, location='query', description='Filter by maximum price'),
            OpenApiParameter('name', str, location='query', description='Filter by card name')
        ]
    )
	


    @action(detail=False, methods=['get'], url_path='filter')
    def filter_card(self, request):
        queryset = self.get_queryset()

        location = request.query_params.get("location")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        name = request.query_params.get("name")


        if location:
               queryset = queryset.filter(service_location__address__icontains=location)


        if min_price:
            try:
                min_price = Decimal(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                return Response(
                    {'error': 'Invalid minimum price value'},
                    status=status.HTTP_400_BAD_REQUEST,
                )


        if max_price:
            try:
                max_price = Decimal(max_price)
                print(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                return Response(
				    {'error': 'Invalid maximum price value'},
				    status=status.HTTP_400_BAD_REQUEST,
				)

        if name:
            queryset = queryset.filter(title__icontains=name)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)