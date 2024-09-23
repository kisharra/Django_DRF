from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Sensor, Measurement
from .serializers import MeasurementSerializer, SensorSerializer, SensorDetailSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def retrieve(self, request, pk=None):
        sensor = self.get_object()
        serializer = SensorDetailSerializer(sensor)
        return Response(serializer.data)

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def create(self, request):
        sensor_id = request.data.get('sensor')  # Извлечение 'sensor'
        temperature = request.data.get('temperature')

        # Проверка существования датчика
        if not Sensor.objects.filter(id=sensor_id).exists():
            return Response({"error": "Sensor not found."}, status=status.HTTP_404_NOT_FOUND)

        measurement = Measurement.objects.create(sensor_id=sensor_id, temperature=temperature)
        serializer = self.get_serializer(measurement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)