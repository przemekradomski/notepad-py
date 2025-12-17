# 📝 Notepad - Aplikacja do zarządzania notatkami

Prosta aplikacja webowa do tworzenia i zarządzania notatkami, zbudowana w Django. Notatki są przechowywane w cookies przeglądarki, więc są dostępne tylko lokalnie i znikają po wyczyszczeniu cookies.

## ✨ Funkcjonalności

- **Trzy typy notatek:**
  - 📌 **Notatki z tytułem** - notatki z tytułem i treścią
  - 📄 **Notatki z treścią** - proste notatki tylko z treścią
  - 📊 **Notatki z danymi JSON** - notatki przechowujące dane w formacie JSON

- **Dashboard z statystykami:**
  - Liczba notatek każdego typu
  - Lista ostatnich 10 notatek
  - Szybkie formularze do dodawania notatek

- **Przeglądanie notatek:**
  - Szczegółowy widok każdej notatki
  - Data utworzenia i modyfikacji
  - Responsywny design

- **Przechowywanie w cookies:**
  - Wszystkie notatki są przechowywane w cookies przeglądarki
  - Brak potrzeby logowania
  - Notatki znikają po wyczyszczeniu cookies

## 🚀 Instalacja

### Wymagania

- Python 3.8+
- Django 6.0+

### Kroki instalacji

1. **Sklonuj repozytorium lub pobierz projekt**

2. **Zainstaluj zależności:**
   ```bash
   pip install django
   ```

3. **Zastosuj migracje (opcjonalne - dla panelu admina):**
   ```bash
   python manage.py migrate
   ```

4. **Uruchom serwer deweloperski:**
   ```bash
   python manage.py runserver
   ```

5. **Otwórz przeglądarkę:**
   ```
   http://127.0.0.1:8000/
   ```

## 📁 Struktura projektu

```
notepad/
├── manage.py                 # Skrypt zarządzania Django
├── db.sqlite3               # Baza danych SQLite (opcjonalna)
├── notepad/                 # Główna konfiguracja projektu
│   ├── settings.py          # Ustawienia Django
│   ├── urls.py              # Główne routingi URL
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
└── notes/                    # Aplikacja notes
    ├── admin.py             # Konfiguracja panelu admina
    ├── models.py            # Modele danych (TitleNote, ContentNote, DataNote)
    ├── views.py             # Widoki aplikacji
    ├── forms.py             # Formularze Django
    ├── templates/           # Szablony HTML
    │   ├── admin/
    │   │   └── notepad.html # Szablon dashboardu
    │   └── note_detail.html # Szablon szczegółów notatki
    └── static/              # Pliki statyczne
        └── notes/
            └── css/
                └── style_notes.css # Style CSS
```

## 🎯 Jak używać

### Dodawanie notatek

1. Przejdź na stronę główną (`http://127.0.0.1:8000/`)
2. Przewiń w dół do sekcji "Dodaj nową notatkę"
3. Wybierz typ notatki i wypełnij formularz
4. Kliknij "Dodaj"

### Przeglądanie notatek

1. Na stronie głównej zobaczysz listę ostatnich notatek
2. Kliknij "Zobacz" przy notatce, aby zobaczyć szczegóły
3. W widoku szczegółów zobaczysz pełną treść notatki i daty

### Usuwanie notatek

Aby usunąć wszystkie notatki, wyczyść cookies w przeglądarce.

## 🔧 Technologie

- **Backend:** Django 6.0
- **Frontend:** HTML, CSS, Django Templates
- **Przechowywanie:** Cookies przeglądarki (JSON + Base64)
- **Baza danych:** SQLite (opcjonalna, tylko dla panelu admina)

## 📝 Uwagi

### Ograniczenia cookies

- Cookies mają limit około **4KB** na cookie
- Jeśli masz dużo notatek, możesz przekroczyć limit
- W takim przypadku rozważ użycie localStorage (JavaScript) zamiast cookies

### Bezpieczeństwo

- Notatki są przechowywane lokalnie w przeglądarce
- Nie są wysyłane na serwer (oprócz zapisu do cookies)
- Po wyczyszczeniu cookies wszystkie notatki znikają

### Panel administracyjny

Aplikacja ma również panel administracyjny Django dostępny pod `/admin/`, ale wymaga utworzenia superusera:

```bash
python manage.py createsuperuser
```

## 🛠️ Rozwój

### Dodawanie nowych funkcji

- Edycja notatek
- Usuwanie pojedynczych notatek
- Eksport notatek do pliku
- Import notatek z pliku
- Kategorie/tagi dla notatek

## 📄 Licencja

Ten projekt jest dostępny do swobodnego użytku.

## 👤 Autor

**Przemysław Radomski**

- GitHub: [@przemekradomski](https://github.com/przemekradomski)

Projekt stworzony jako aplikacja do nauki Django.

---

**Uwaga:** To jest aplikacja deweloperska. Do użycia produkcyjnego należy zmienić `SECRET_KEY` i `DEBUG = False` w `settings.py`.

