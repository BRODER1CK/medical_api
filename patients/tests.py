from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, User


class PatientTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.doctor = User.objects.create(username='doctor', role='doctor')
        self.doctor.set_password('testpass')
        self.doctor.save()

        self.patient_user = User.objects.create(username='patient_user', role='patient')
        self.patient_user.set_password('testpass')
        self.patient_user.save()

        # Создаем пациента
        self.patient = Patient.objects.create(date_of_birth="1990-01-01", diagnoses=["diagnosis1", "diagnosis2"])

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_login_invalid_credentials(self):
        # Тест: Неверные учетные данные для логина
        response = self.client.post('/api/login/', {'username': 'doctor', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields(self):
        # Тест: Пропущенные поля в логине
        response = self.client.post('/api/login/', {'username': 'doctor'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patients_access_as_patient(self):
        # Тест: Попытка доступа к списку пациентов от пользователя с ролью patient
        self.authenticate(self.patient_user)
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patients_access_without_authentication(self):
        # Тест: Попытка доступа к списку пациентов без авторизации
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_creation(self):
        # Тест: Создание пациента (доступно только для доктора)
        self.authenticate(self.doctor)
        data = {
            "date_of_birth": "1985-05-10",
            "diagnoses": '["diabetes", "hypertension"]'
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)

    def test_patient_creation_forbidden_for_patient_role(self):
        # Тест: Создание пациента от пользователя с ролью patient
        self.authenticate(self.patient_user)
        data = {
            "date_of_birth": "1985-05-10",
            "diagnoses": '["diabetes", "hypertension"]'
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_creation_invalid_data(self):
        # Тест: Попытка создания пациента с некорректными данными
        self.authenticate(self.doctor)
        data = {
            "date_of_birth": "invalid-date",  # Некорректный формат даты
            "diagnoses": "not-a-list"  # Некорректный формат диагнозов
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_list_with_multiple_patients(self):
        # Тест: Проверка получения списка пациентов при наличии нескольких записей
        Patient.objects.create(date_of_birth="1985-05-10", diagnoses=["diagnosis3"])
        self.authenticate(self.doctor)
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Теперь два пациента

    def test_update_patient(self):
        # Тест: Обновление данных пациента (доступно только для доктора)
        self.authenticate(self.doctor)
        data = {
            "date_of_birth": "2000-01-01",
            "diagnoses": '["updated-diagnosis"]'
        }
        response = self.client.put(f'/api/patients/{self.patient.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.date_of_birth.strftime("%Y-%m-%d"), "2000-01-01")
        self.assertEqual(self.patient.diagnoses, ["updated-diagnosis"])

    def test_delete_patient(self):
        # Тест: Удаление пациента (доступно только для доктора)
        self.authenticate(self.doctor)
        response = self.client.delete(f'/api/patients/{self.patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)
