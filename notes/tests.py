from django.test import TestCase
from django.utils import timezone
from termcolor import colored
from .models import TitleNote, ContentNote, DataNote


class TitleNoteModelTest(TestCase):
    """Testy dla modelu TitleNote"""
    
    def setUp(self):
        """Przygotowanie danych testowych"""
        self.note = TitleNote.objects.create(
            title="Test Note",
            content="This is a test content"
        )
    
    def test_title_note_creation(self):
        """Test tworzenia notatki z tytułem"""
        self.assertIsNotNone(self.note)
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is a test content")
        print(colored("✓ Test tworzenia TitleNote - OK", "green"))
    
    def test_title_note_str(self):
        """Test metody __str__"""
        self.assertEqual(str(self.note), "Test Note")
        print(colored("✓ Test __str__ TitleNote - OK", "green"))
    
    def test_title_note_timestamps(self):
        """Test automatycznego ustawiania dat"""
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)
        self.assertLessEqual(self.note.created_at, timezone.now())
        print(colored("✓ Test timestampów TitleNote - OK", "green"))
    
    def test_title_note_max_length(self):
        """Test maksymalnej długości tytułu"""
        long_title = "x" * 200
        note = TitleNote.objects.create(title=long_title, content="test")
        self.assertEqual(len(note.title), 200)
        print(colored("✓ Test max_length tytułu - OK", "green"))


class ContentNoteModelTest(TestCase):
    """Testy dla modelu ContentNote"""
    
    def setUp(self):
        """Przygotowanie danych testowych"""
        self.note = ContentNote.objects.create(
            content="This is a longer content that should be truncated in __str__"
        )
    
    def test_content_note_creation(self):
        """Test tworzenia notatki bez tytułu"""
        self.assertIsNotNone(self.note)
        self.assertEqual(self.note.content, "This is a longer content that should be truncated in __str__")
        print(colored("✓ Test tworzenia ContentNote - OK", "green"))
    
    def test_content_note_str(self):
        """Test metody __str__ (powinna zwracać pierwsze 50 znaków)"""
        self.assertEqual(str(self.note), "This is a longer content that should be trun")
        print(colored("✓ Test __str__ ContentNote - OK", "green"))
    
    def test_content_note_timestamps(self):
        """Test automatycznego ustawiania dat"""
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)
        print(colored("✓ Test timestampów ContentNote - OK", "green"))


class DataNoteModelTest(TestCase):
    """Testy dla modelu DataNote"""
    
    def setUp(self):
        """Przygotowanie danych testowych"""
        self.test_data = {
            "name": "Test",
            "value": 123,
            "items": [1, 2, 3],
            "nested": {"key": "value"}
        }
        self.note = DataNote.objects.create(data=self.test_data)
    
    def test_data_note_creation(self):
        """Test tworzenia notatki z danymi JSON"""
        self.assertIsNotNone(self.note)
        self.assertEqual(self.note.data, self.test_data)
        print(colored("✓ Test tworzenia DataNote - OK", "green"))
    
    def test_data_note_str(self):
        """Test metody __str__"""
        self.assertIn("Test", str(self.note))
        print(colored("✓ Test __str__ DataNote - OK", "green"))
    
    def test_data_note_json_structure(self):
        """Test struktury danych JSON"""
        self.assertEqual(self.note.data["name"], "Test")
        self.assertEqual(self.note.data["value"], 123)
        self.assertEqual(len(self.note.data["items"]), 3)
        print(colored("✓ Test struktury JSON - OK", "green"))
    
    def test_data_note_timestamps(self):
        """Test automatycznego ustawiania dat"""
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)
        print(colored("✓ Test timestampów DataNote - OK", "green"))


class ModelIntegrationTest(TestCase):
    """Testy integracyjne dla wszystkich modeli"""
    
    def test_all_models_can_be_created(self):
        """Test czy wszystkie modele można utworzyć"""
        title_note = TitleNote.objects.create(title="Title", content="Content")
        content_note = ContentNote.objects.create(content="Content only")
        data_note = DataNote.objects.create(data={"test": "data"})
        
        self.assertEqual(TitleNote.objects.count(), 1)
        self.assertEqual(ContentNote.objects.count(), 1)
        self.assertEqual(DataNote.objects.count(), 1)
        print(colored("✓ Test integracyjny - wszystkie modele działają - OK", "green"))
    
    def test_ordering(self):
        """Test sortowania po dacie utworzenia (najnowsze pierwsze)"""
        note1 = TitleNote.objects.create(title="First", content="First note")
        note2 = TitleNote.objects.create(title="Second", content="Second note")
        note3 = TitleNote.objects.create(title="Third", content="Third note")
        
        notes = list(TitleNote.objects.all())
        # Najnowsze powinny być pierwsze (ordering = ['-created_at'])
        self.assertEqual(notes[0].title, "Third")
        self.assertEqual(notes[-1].title, "First")
        print(colored("✓ Test sortowania - OK", "green"))
