from django.db.models import Avg
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Professor, Module, Rating
from .serializers import ProfessorSerializer, ModuleSerializer, RatingSerializer, UserSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.annotate(average_rating=Avg('ratings__score'))
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny]

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.AllowAny]

class RatingViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny] 

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)

class ProfessorModuleAverageRatingView(APIView):
    def get(self, request, professor_id, module_code):
        errors = {}

        professor = Professor.objects.filter(identifier=professor_id).first()
        if not professor:
            errors["professor"] = f"Professor with ID '{professor_id}' not found."

        module_instances = Module.objects.filter(code=module_code)
        if not module_instances.exists():
            errors["module"] = f"Module with code '{module_code}' not found."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_404_NOT_FOUND)

        ratings = Rating.objects.filter(professor=professor, module__in=module_instances)

        if not ratings.exists():
            return Response({
                "error": f"No ratings found for Professor {professor_id} in any instance of Module {module_code}."
            }, status=status.HTTP_404_NOT_FOUND)

        avg_score = ratings.aggregate(Avg('score'))['score__avg']
        average_score = round(avg_score) if avg_score is not None else None

        return Response({
            "professor": professor_id,
            "module": module_code,
            "average_rating": average_score
        })
    
class RateProfessorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        try:
            professor = Professor.objects.get(identifier=data['professor_id'])
            module = Module.objects.get(code=data['module_code'], year=data['year'], semester=data['semester'])

            if not Module.objects.filter(code=data['module_code'], year=data['year'], semester=data['semester'], professors=professor).exists():
                return Response(
                    {"error": f"Professor {professor.name} is not teaching {module.name} in {data['year']} Semester {data['semester']}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            rating, created = Rating.objects.get_or_create(
                user=user,
                professor=professor,
                module=module,
                year=data['year'],
                semester=data['semester'],
                defaults={"score": data['rating']}
            )

            if not created:
                return Response(
                    {"error": "You have already rated this professor for this module instance. Ratings cannot be changed or deleted."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({"message": "Rating submitted successfully!"}, status=status.HTTP_201_CREATED)

        except Professor.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Module.DoesNotExist:
            module_exists = Module.objects.filter(code=data['module_code']).exists()
            
            if module_exists:
                return Response(
                    {"error": f"Module '{data['module_code']}' exists, but no instance was found for Year {data['year']} and Semester {data['semester']}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                return Response({"error": f"Module '{data['module_code']}' not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
