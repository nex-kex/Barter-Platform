from django.test import TestCase
from django.urls import reverse

from ads.models import Ad, ExchangeProposal
from users.models import User


class AdTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="password",
        )
        self.ad = Ad.objects.create(
            title="Test title",
            description="Test description",
            category="Test category",
            condition="other",
            user=self.user,
        )
        self.client.force_login(self.user)

    def test_ad_create(self):
        """Создание товара."""
        url = reverse("ads:ad-create")
        data = {
            "title": "New title",
            "description": "New description",
            "category": "New category",
            "condition": "used",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title="New title").exists())

    def test_ad_list(self):
        """Получение списка товаров."""
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test title")
        self.assertContains(response, "Test description")

    def test_ad_detail(self):
        """Получение одного товара."""
        response = self.client.get(reverse("ads:ad-detail", args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test title")
        self.assertEqual(str(self.ad), "Test title")

    def test_ad_update(self):
        """Обновление товара."""
        url = reverse("ads:ad-update", args=[self.ad.id])
        data = {
            "title": "Updated title",
            "description": "Updated description",
            "category": "Test category",
            "condition": "other",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Updated title")

    def test_ad_destroy(self):
        """Удаление товара."""
        response = self.client.post(reverse("ads:ad-delete", args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())


class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            password="password",
            username="test_username1",
        )
        self.user2 = User.objects.create_user(
            password="password",
            username="test_username2",
        )
        self.ad1 = Ad.objects.create(
            title="Test title 1",
            description="Test description 1",
            category="Test category 1",
            condition="other",
            user=self.user1,
        )
        self.ad2 = Ad.objects.create(
            title="Test title 2",
            description="Test description 2",
            category="Test category 2",
            condition="new",
            user=self.user2,
        )
        self.ep = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Test comment"
        )
        self.client.force_login(user=self.user1)

    def test_exchange_create(self):
        """Создание предложения обмена."""
        url = reverse("ads:exchange-create")
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "New comment"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(comment="New comment").exists())

    def test_sent_exchange_list(self):
        """Получение списка отправленных предложений обмена."""
        url = reverse("ads:sent-exchange-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('exchangeproposal_list', response.context)
        self.assertEqual(len(response.context['exchangeproposal_list']), 1)
        self.assertEqual(response.context['exchangeproposal_list'][0].comment, "Test comment")


    def test_received_exchange_list(self):
        """Получение списка полученных предложений обмена."""
        url = reverse("ads:received-exchange-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('exchangeproposal_list', response.context)
        self.assertEqual(len(response.context['exchangeproposal_list']), 0)

    def test_exchange_detail(self):
        """Получение одного предложения обмена."""
        response = self.client.get(reverse("ads:exchange-detail", args=[self.ep.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['exchangeproposal'].comment, "Test comment")
        self.assertContains(response, "Test comment")
        self.assertEqual(str(self.ep), f"Предложение номер {self.ep.id}")

    def test_exchange_destroy(self):
        """Удаление предложения обмена."""
        response = self.client.post(reverse("ads:exchange-delete", args=[self.ep.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ExchangeProposal.objects.filter(id=self.ep.id).exists())


    def test_accept_exchange(self):
        """Принятие предложения."""
        self.client.force_login(user=self.user2)
        response = self.client.post(reverse("ads:exchange-accept", args=[self.ep.id]))
        self.assertEqual(response.status_code, 302)
        self.ep.refresh_from_db()
        self.assertEqual(self.ep.status, "accepted")


    def test_decline_exchange(self):
        """Принятие предложения."""
        self.client.force_login(user=self.user2)
        response = self.client.post(reverse("ads:exchange-decline", args=[self.ep.id]))
        self.assertEqual(response.status_code, 302)
        self.ep.refresh_from_db()
        self.assertEqual(self.ep.status, "declined")