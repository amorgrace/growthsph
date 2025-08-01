from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import WalletAddressSerializer, FinancesSerializers, RecentTransactionSerializer, KYCSerializer, ChangePasswordSerializer
from .models import WalletAddres, Finance, RecentTransaction, KYC
from djoser.serializers import ActivationSerializer
from djoser.utils import decode_uid
from drf_yasg.utils import swagger_auto_schema


class ActivateUserView(APIView):
    def get(self, request, uid, token, *args, **kwargs):
        serializer = ActivationSerializer(data={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class WalletAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = WalletAddres.objects.first()
        serializer = WalletAddressSerializer(wallet)
        return Response(serializer.data)

class UserFinancesView(ListAPIView):
    serializer_class = FinancesSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Finance.objects.filter(user=self.request.user)
    

class UserTransactionListView(ListAPIView):
    serializer_class = RecentTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecentTransaction.objects.filter(user=self.request.user).order_by('-date')
    

class KYCUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kyc_instance = KYC.objects.filter(user=request.user).first()
        if not kyc_instance:
            return Response({'detail': 'No KYC submitted yet.', 'status': 'pending'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KYCSerializer(kyc_instance)
        return Response({
            'kyc_data': serializer.data,
            'status': kyc_instance.kyc_status,
            'message': f'KYC status is "{kyc_instance.kyc_status}".'
        }, status=status.HTTP_200_OK)


    def post(self, request):
        kyc_instance = KYC.objects.filter(user=request.user).first()

        serializer = KYCSerializer(data=request.data, instance=kyc_instance)
        if serializer.is_valid():
            kyc = serializer.save(user=request.user)

            if kyc.kyc_status == "pending":
                message = 'Submit KYC info.'
            elif kyc.kyc_status == 'in_review':
                message = 'KYC submitted successfully and is now under review.'
            elif kyc.kyc_status == "approved":
                message = 'KYC already approved. No further action required.'
            elif kyc.kyc_status == "rejected":
                message = 'KYC was rejected. Please contact support before resubmitting.'
            else:
                message = f"KYC status is {kyc.kyc_status}."

            return Response({
                'detail': message,
                'status': kyc.kyc_status
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# from django.http import JsonResponse
# from django.core.mail import send_mail

# def test_email_view(request):
#     send_mail(
#         "Test Subject",
#         "Test message",
#         "noreply@example.com",
#         ["youremail@example.com"],
#     )
#     return JsonResponse({"status": "sent"})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if not user.check_password(current_password):
            return Response({'error': 'Current Password is Incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)