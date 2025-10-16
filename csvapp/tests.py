from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class CSVUploadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('upload')

    def test_valid_csv_upload(self):
        csv_content = b"name,email,age\nAlice,alice@example.com,25\nBob,bob@example.com,30"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saved_count'], 2)
        self.assertEqual(response.data['rejected_count'], 0)

    def test_invalid_csv_data(self):
        csv_content = b"name,email,age\n,invalidemail,150"
        csv_file = SimpleUploadedFile("invalid.csv", csv_content, content_type="text/csv")
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saved_count'], 0)
        self.assertEqual(response.data['rejected_count'], 1)
        self.assertIn('name', response.data['errors'][0]['errors'])
        self.assertIn('age', response.data['errors'][0]['errors'])
        self.assertIn('email', response.data['errors'][0]['errors'])

    def test_duplicate_email(self):
        csv_content_1 = b"name,email,age\nAlice,alice@example.com,25"
        csv_content_2 = b"name,email,age\nAlice,alice@example.com,30"

        file1 = SimpleUploadedFile("file1.csv", csv_content_1, content_type="text/csv")
        file2 = SimpleUploadedFile("file2.csv", csv_content_2, content_type="text/csv")

        response1 = self.client.post(self.url, {'file': file1}, format='multipart')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['saved_count'], 1)

        response2 = self.client.post(self.url, {'file': file2}, format='multipart')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['saved_count'], 0)
        self.assertEqual(response2.data['rejected_count'], 1)
        self.assertIn('email', response2.data['errors'][0]['errors'])
