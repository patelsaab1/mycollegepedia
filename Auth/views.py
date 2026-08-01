from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from App.settings import TEMPLATES_BASE_URL
from .sms import send_password_reset_sms
from .models import Student, PasswordResetToken, Education, OTP, CollegeAdmin, CounsellorAdmin, User
from .serializers import RegisterSerializer, ProfileSerializer, EducationSerializer, CustomTokenObtainPairSerializer, \
    CustomUserSerializer, StudentProfileSerializer, CollegeProfileSerializer, CounsellorProfileSerializer, \
    StudentSerializer, PasswordResetSerializer, CounsellorRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .otp_genrator import generate_otp
from twilio.rest import Client
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string


# class RegisterView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = RegisterSerializer(data=data)

#         if serializer.is_valid():
#             user = Student(
#                 email=data['email'],
#                 name=data['name'],
#                 mobile=data['mobile'],
#                 is_active=True,
#             )
#             user.set_password(data['password'])
#             user.save()

#             return Response({'message': 'Registration successfully.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = Student(
                email=data['email'],
                name=data['name'],
                mobile=data['mobile'],
                is_active = False,
                is_student=True,
            )
            user.set_password(data['password'])
            user.save()

            otp = generate_otp()  
            OTP.objects.create(user=user, otp=otp)

            # self.send_otp(user, otp)

            return Response({'message': 'User registered successfully. OTP sent.','OTP':otp}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_otp(self, user, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms_body = render_to_string("sms/register_otp.txt", {
            "otp": otp,
            "user": user.name,
        })

        message = client.messages.create(
            body=sms_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.mobile
        )


class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        entered_otp = request.data.get('otp')

        try:
            user = Student.objects.get(mobile=mobile)
            otp_obj = OTP.objects.get(user=user, otp=entered_otp)

            if (timezone.now() - otp_obj.timestamp).seconds > 300:
                return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()

            otp_obj.delete()

            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        except OTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')

        try:
            user = Student.objects.get(mobile=mobile)
            otp = generate_otp()

            # Check if an OTP record already exists and delete it
            try:
                existing_otp = OTP.objects.get(user=user)
                existing_otp.delete()
            except OTP.DoesNotExist:
                pass

            # Create a new OTP record
            OTP.objects.create(user=user, otp=otp)

            # Send OTP via Twilio
            # RegisterView().send_otp(user, otp)

            return Response({'message': 'New OTP sent successfully.','OTP':otp}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
class CounsellorRegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = CounsellorRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            # self.send_otp(user, otp)
            return Response({'message': 'Counsellor registered successfully. OTP sent.','OTP':otp},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_otp(self, user, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms_body = render_to_string("sms/counsellor_register_otp.txt", {
            "otp": otp,
            "user": user.name,
        })
        message = client.messages.create(
            body=sms_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.mobile
        )


class CounsellorVerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        entered_otp = request.data.get('otp')

        try:
            user = CounsellorAdmin.objects.get(mobile=mobile)
            otp_obj = OTP.objects.get(user=user, otp=entered_otp)

            if (timezone.now() - otp_obj.timestamp).seconds > 300:
                return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = False
            user.save()
            self.send_otp(user)
            otp_obj.delete()

            return Response({'message': 'Registration successful. Your profile is under verification.',
                             'user_id': user.id,
                             'name': user.name
                             },
                            status=status.HTTP_200_OK)

        except CounsellorAdmin.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        except OTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

    def send_otp(self, user):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms_body = render_to_string("sms/counsellor_review.txt", {
            "user": user.name,
        })

        message = client.messages.create(
            body=sms_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.mobile
        )



class CounsellorResendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')

        try:
            user = CounsellorAdmin.objects.get(mobile=mobile)
            otp = generate_otp()

            try:
                existing_otp = OTP.objects.get(user=user)
                existing_otp.delete()
            except OTP.DoesNotExist:
                pass

            # Create a new OTP record
            OTP.objects.create(user=user, otp=otp)

            # Send OTP via Twilio
            # CounsellorRegisterView().send_otp(user, otp)

            return Response({'message': 'New OTP sent successfully.','OTP':otp}, status=status.HTTP_200_OK)

        except CounsellorAdmin.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = CustomUserSerializer(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=400)


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is missing'}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, email=email)
        return send_password_reset_sms(user)
        user = User.objects.filter(email=email).first()
        if user:
            # send_otp(email)
            return Response({'message': 'Link sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetFormAPIView(APIView):
    def get(self, request, email, token):
        token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
        if token_instance:
            if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
                return Response({
                    "email": email,
                    "token": token,
                    "base_url": TEMPLATES_BASE_URL
                })
            else:
                token_instance.delete()
                return Response({"error": "Reset link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')
            confirmPassword = serializer.validated_data.get('confirmPassword')
            token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()

            if token_instance:
                if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
                    try:
                        validate_password(password, user=token_instance.user)

                        if password == confirmPassword:
                            user = token_instance.user
                            user.password = make_password(password)
                            user.save()
                            token_instance.delete()
                            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": "Password and confirm password don't match"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except ValidationError as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token_instance.delete()
                    return Response({"error": "Reset link has expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def password_reset_form(request, email, token):
#     token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
#     link_expired = get_template('pages/link_expired.html').render()
#     if token_instance:
#         if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
#             return render(request, 'pages/new_password_form.html', {
#                 "email": email,
#                 "token": token,
#                 "base_url": TEMPLATES_BASE_URL
#             })
#         else:
#             token_instance.delete()
#             return HttpResponse(link_expired)
#     else:
#         return HttpResponse(link_expired)


# @api_view(['POST'])
# def password_reset_confirm(request):
#     email = request.data.get('email')
#     token = request.data.get('token')
#     password = request.data.get('password')
#     confirmPassword = request.data.get('confirmPassword')
#     token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
#     link_expired = get_template('pages/link_expired.html').render()

#     if token_instance:
#         if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
#             try:
#                 validate_password(password, user=token_instance.user)

#                 if password == confirmPassword:
#                     user = token_instance.user
#                     user.password = make_password(password)
#                     user.save()
#                     token_instance.delete()
#                     return render(request, 'pages/password_update.html')
#                 else:
#                     return render(request, 'pages/new_password_form.html', {
#                         "email": email,
#                         "token": token,
#                         "base_url": TEMPLATES_BASE_URL,
#                         "error": "Password and confirm password don't match!",
#                     })
#             except ValidationError as e:
#                 return render(request, 'pages/new_password_form.html', {
#                     "email": email,
#                     "token": token,
#                     "base_url": TEMPLATES_BASE_URL,
#                     "error": str(e),
#                 })
#         else:
#             token_instance.delete()
#             return HttpResponse(link_expired)
#     else:
#         return HttpResponse(link_expired)

class StudentViewSet(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class StudentProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.student

    def perform_update(self, serializer):
        serializer.save()

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
# College Profile
class CollegeProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CollegeAdmin.objects.all()
    serializer_class = CollegeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.collegeadmin

    def perform_update(self, serializer):
        serializer.save()
        
        
# Counsellor Profile
class CounsellorProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CounsellorAdmin.objects.all()
    serializer_class = CounsellorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.counselloradmin

    def perform_update(self, serializer):
        serializer.save()