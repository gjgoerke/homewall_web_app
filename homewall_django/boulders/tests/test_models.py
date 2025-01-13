from django.test import TestCase
from boulders.models import Boulder
from django.utils import timezone
from django.core.exceptions import ValidationError

class BoulderModelTests(TestCase):
    def setUp(self):
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

    def test_boulder_creation(self):
        self.assertEqual(self.boulder.name, "Test Boulder")
        self.assertEqual(self.boulder.grade, 5)
        self.assertEqual(self.boulder.holds_start, [1, 2])
        self.assertEqual(self.boulder.holds_finish, [3, 4])

    def test_boulder_str_representation(self):
        self.assertEqual(str(self.boulder), "Test Boulder V5")

    def test_invalid_grade(self):
        with self.assertRaises(ValidationError):
            boulder = Boulder(
                name="Invalid Grade Boulder",
                grade=17,  # Grade too high
                description="Test description",
                date_set=timezone.now(),
                holds_start=[1]
            )
            boulder.full_clean()

    def test_empty_holds(self):
        boulder = Boulder.objects.create(
            name="Empty Holds Boulder",
            grade=5,
            description="Test description",
            date_set=timezone.now(),
            holds_start=[],
            holds_finish=[],
            holds_general=[],
            holds_feet_only=[],
            holds_hands_only=[]
        )
        self.assertEqual(boulder.holds_start, [])
        self.assertEqual(boulder.holds_general, [])

    def test_duplicate_holds(self):
        boulder = Boulder.objects.create(
            name="Duplicate Holds Boulder",
            grade=5,
            description="Test description",
            date_set=timezone.now(),
            holds_start=[1, 1, 2],  # Duplicate hold
            holds_finish=[3, 4]
        )
        # The list should automatically remove duplicates
        self.assertEqual(boulder.holds_start, [1, 2]) 