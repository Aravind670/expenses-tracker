from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ExpenseSerializer
from .models import Expense

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
        return queryset

    def perform_create(self, serializer):
        # ✅ ALWAYS creates a new expense row for this user
        serializer.save(user=self.request.user)
