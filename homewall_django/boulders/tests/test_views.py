from django.test import TestCase, Client
from django.urls import reverse
from boulders.models import Boulder
from django.utils import timezone

class BoulderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.boulder = Boulder.objects.create(
            name="Test Boulder",
            grade=5,
            description="Test description",
            date_set=timezone.now(),
            holds_start=[1, 2],
            holds_finish=[3, 4],
            holds_general=[5, 6],
            holds_feet_only=[7],
            holds_hands_only=[8]
        )

    def test_index_view(self):
        response = self.client.get(reverse('boulders:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boulders/index.html')
        self.assertContains(response, "Test Boulder")
        self.assertContains(response, "V5")

    def test_boulder_detail_view(self):
        response = self.client.get(reverse('boulders:boulder_view', args=[self.boulder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boulders/boulder.html')
        self.assertContains(response, "Test Boulder")
        self.assertContains(response, "V5")
        self.assertContains(response, "Test description")

    def test_new_boulder_view_get(self):
        response = self.client.get(reverse('boulders:new_boulder_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boulders/new.html')

    def test_new_boulder_view_post(self):
        boulder_data = {
            'name': 'New Test Boulder',
            'grade': 6,
            'description': 'New test description',
            'date_set': timezone.now().date(),
            'holds_start': '[1,2]',
            'holds_finish': '[3,4]',
            'holds_general': '[5,6]',
            'holds_feet_only': '[7]',
            'holds_hands_only': '[8]'
        }
        response = self.client.post(reverse('boulders:new_boulder_view'), boulder_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify the boulder was created
        new_boulder = Boulder.objects.get(name='New Test Boulder')
        self.assertEqual(new_boulder.grade, 6)
        self.assertEqual(new_boulder.holds_start, [1, 2]) 