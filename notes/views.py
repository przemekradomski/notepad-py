from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import TitleNote, ContentNote, DataNote
from .forms import TitleNoteForm, ContentNoteForm, DataNoteForm
import json
import base64
from datetime import datetime


def get_notes_from_cookies(request):
    """Pobiera wszystkie notatki z cookies"""
    notes_cookie = request.COOKIES.get('notes', '[]')
    try:
        # Dekoduj z base64 jeśli potrzeba
        try:
            notes_data = json.loads(base64.b64decode(notes_cookie).decode('utf-8'))
        except:
            notes_data = json.loads(notes_cookie)
        return notes_data
    except:
        return []


def save_notes_to_cookies(response, notes):
    """Zapisuje notatki do cookies"""
    try:
        # Konwertuj na JSON i zakoduj w base64 (dla bezpieczeństwa i kompresji)
        notes_json = json.dumps(notes, ensure_ascii=False)
        notes_encoded = base64.b64encode(notes_json.encode('utf-8')).decode('utf-8')
        # Ustaw cookie na 1 rok
        response.set_cookie('notes', notes_encoded, max_age=365*24*60*60, httponly=False)
    except Exception as e:
        print(f"Błąd zapisu do cookies: {e}")


def get_note_from_cookies(request, note_id):
    """Pobiera konkretną notatkę z cookies po ID"""
    notes = get_notes_from_cookies(request)
    for note in notes:
        if str(note.get('id')) == str(note_id):
            return note
    return None


def note_detail(request, note_id):
    """Wyświetla szczegóły notatki z cookies"""
    note = get_note_from_cookies(request, note_id)
    
    if note is None:
        messages.error(request, 'Notatka nie została znaleziona.')
        return redirect('notepad_dashboard')
    
    # Utwórz obiekt podobny do modelu dla kompatybilności z szablonem
    class NoteObj:
        def __init__(self, note_data):
            self.id = note_data.get('id')
            self.title = note_data.get('title', '')
            self.content = note_data.get('content', '')
            self.data = note_data.get('data', {})
            self.created_at = datetime.fromisoformat(note_data.get('created_at', datetime.now().isoformat()))
            self.updated_at = datetime.fromisoformat(note_data.get('updated_at', datetime.now().isoformat()))
        
        def __str__(self):
            if self.title:
                return self.title
            elif self.content:
                return self.content[:50]
            else:
                return str(self.data)[:50]
    
    note_obj = NoteObj(note)
    note_type = note.get('type', 'content')
    
    context = {
        'note': note_obj,
        'note_type': note_type
    }
    
    return render(request, 'note_detail.html', context)


def delete_note(request, note_id):
    """Usuwa pojedynczą notatkę z cookies"""
    # Dla bezpieczeństwa usuwamy notatkę tylko przez POST
    if request.method != 'POST':
        return redirect('note_detail', note_id=note_id)

    notes = get_notes_from_cookies(request)
    original_count = len(notes)
    # Filtrowanie listy notatek, aby usunąć wskazaną
    notes = [n for n in notes if str(n.get('id')) != str(note_id)]

    response = redirect('notepad_dashboard')

    if len(notes) == original_count:
        messages.error(request, 'Notatka nie została znaleziona.')
    else:
        messages.success(request, 'Notatka została usunięta.')

    save_notes_to_cookies(response, notes)
    return response


def notepad_dashboard(request):
    notes = get_notes_from_cookies(request)
    response = None
    
    # Obsługa formularzy
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        now = datetime.now().isoformat()
        
        # Generuj nowe ID (największe istniejące + 1 lub 1)
        if notes:
            new_id = max([note.get('id', 0) for note in notes]) + 1
        else:
            new_id = 1
        
        if form_type == 'title':
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            if title or content:
                new_note = {
                    'id': new_id,
                    'type': 'title',
                    'title': title,
                    'content': content,
                    'created_at': now,
                    'updated_at': now
                }
                notes.append(new_note)
                messages.success(request, 'Notatka z tytułem została dodana!')
        elif form_type == 'content':
            content = request.POST.get('content', '')
            if content:
                new_note = {
                    'id': new_id,
                    'type': 'content',
                    'content': content,
                    'created_at': now,
                    'updated_at': now
                }
                notes.append(new_note)
                messages.success(request, 'Notatka z treścią została dodana!')
        elif form_type == 'data':
            data_str = request.POST.get('data', '{}')
            try:
                data = json.loads(data_str) if isinstance(data_str, str) else data_str
                new_note = {
                    'id': new_id,
                    'type': 'data',
                    'data': data,
                    'created_at': now,
                    'updated_at': now
                }
                notes.append(new_note)
                messages.success(request, 'Notatka z danymi JSON została dodana!')
            except json.JSONDecodeError:
                messages.error(request, 'Nieprawidłowy format JSON!')
        
        # Zapisz do cookies
        response = redirect('notepad_dashboard')
        save_notes_to_cookies(response, notes)
        return response
    
    # Pobierz statystyki z cookies
    title_notes = [n for n in notes if n.get('type') == 'title']
    content_notes = [n for n in notes if n.get('type') == 'content']
    data_notes = [n for n in notes if n.get('type') == 'data']
    
    title_notes_count = len(title_notes)
    content_notes_count = len(content_notes)
    data_notes_count = len(data_notes)
    
    # Przygotuj notatki do wyświetlenia
    class NoteObj:
        def __init__(self, note_data):
            self.id = note_data.get('id')
            self.title = note_data.get('title', '')
            self.content = note_data.get('content', '')
            self.data = note_data.get('data', {})
            self.created_at = datetime.fromisoformat(note_data.get('created_at', datetime.now().isoformat()))
            self.updated_at = datetime.fromisoformat(note_data.get('updated_at', datetime.now().isoformat()))
        
        def __str__(self):
            if self.title:
                return self.title
            elif self.content:
                return self.content[:50]
            else:
                return str(self.data)[:50]
    
    # Połącz wszystkie notatki
    recent_notes = []
    for note_data in notes:
        note_obj = NoteObj(note_data)
        note_type = note_data.get('type', 'content')
        recent_notes.append({
            'note': note_obj,
            'type': note_type,
            'type_name': 'TitleNote' if note_type == 'title' else ('ContentNote' if note_type == 'content' else 'DataNote')
        })
    
    # Sortuj po dacie utworzenia (najnowsze pierwsze)
    recent_notes.sort(key=lambda x: x['note'].created_at, reverse=True)
    recent_notes = recent_notes[:10]  # Maksymalnie 10 najnowszych
    
    # Utwórz formularze
    title_form = TitleNoteForm()
    content_form = ContentNoteForm()
    data_form = DataNoteForm()
    
    context = {
        'title_notes_count': title_notes_count,
        'content_notes_count': content_notes_count,
        'data_notes_count': data_notes_count,
        'recent_notes': recent_notes,
        'title_form': title_form,
        'content_form': content_form,
        'data_form': data_form,
    }
    
    response = render(request, 'admin/notepad.html', context)
    # Zapisujemy notatki do cookies (na wypadek gdyby coś się zmieniło)
    save_notes_to_cookies(response, notes)
    return response
