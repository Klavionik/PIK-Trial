from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from construction.models import Building


class TestBuildingView(APITestCase):
    def setUp(self):
        self.building_url = reverse('building')
        self.current_year = datetime.now().year

    def test_creation(self):
        building = {'address': 'Тестовый адрес 1', 'built': self.current_year + 5}
        response = self.client.post(self.building_url, building, format='json')
        self.assertEqual(response.status_code, 201)

    def test_year_validation(self):
        building = {'address': 'Тестовый адрес 1', 'built': self.current_year - 1}
        response = self.client.post(self.building_url, building, format='json')
        self.assertEqual(response.status_code, 400, "Built value must at least this year")

    def test_address_validation(self):
        address = 'Адрес'
        Building.objects.create(address=address, built=self.current_year + 5)

        building = {'address': address, 'built': self.current_year + 5}
        response = self.client.post(self.building_url, building, format='json')
        self.assertEqual(response.status_code, 400, "Address must be unique")


class TestJobView(APITestCase):
    def setUp(self):
        self.current_year = datetime.now().year
        self.sample_built = self.current_year + 5
        self.building = Building.objects.create(
            address='Тестовый адрес 9',
            built=self.sample_built)
        self.job_url = reverse('building') + f'{self.building.id}' + '/add_bricks/'

    def test_creation(self):
        job_time = datetime.strptime(f'{self.sample_built - 2}-01-01 10:00', '%Y-%m-%d %H:%M')
        job = {'bricks_amount': 10000, 'execution_time': job_time, 'building': self.building.id}

        response = self.client.post(self.job_url, job, format='json')
        self.assertEqual(response.status_code, 201)

    def test_year_validation(self):
        job_time = datetime.strptime(f'{self.building.built + 1}-01-01 10:00', '%Y-%m-%d %H:%M')
        job = {'bricks_amount': 10000, 'execution_time': job_time, 'building': self.building.id}

        response = self.client.post(self.job_url, job, format='json')
        self.assertEqual(response.status_code, 400,
                         "Job execution time must not be after building's built year")

    def test_bricks_amount_validation(self):
        job_time = datetime.strptime(f'{self.sample_built + 2}-01-01 10:00', '%Y-%m-%d %H:%M')
        job = {'bricks_amount': 0, 'execution_time': job_time, 'building': self.building.id}

        response = self.client.post(self.job_url, job, format='json')
        self.assertEqual(response.status_code, 400, "Bricks amount must be greater than 0")

    def test_time_validation(self):
        job_time = datetime.strptime(f'{self.current_year - 1}-01-01 10:00', '%Y-%m-%d %H:%M')
        job = {'bricks_amount': 1000, 'execution_time': job_time, 'building': self.building.id}

        response = self.client.post(self.job_url, job, format='json')
        self.assertEqual(response.status_code, 400, "Job execution time must not be in the past")
