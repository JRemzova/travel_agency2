# Travel Agency 2

Projekt cestovní kanceláře postavený na frameworku **Django**.  
Umožňuje spravovat zájezdy, registrovat uživatele a provádět rezervace.

---

## Spuštění projektu

1. Naklonujte si repozitář:

    ```bash
   git clone https://github.com/JRemzova/travel_agency2.git
   cd travel_agency2

2. Vytvořte virtuální prostředí a aktivujte ho:

  python -m venv .venv
  .venv\Scripts\activate   # Windows
  source .venv/bin/activate   # Linux/Mac

3. Nainstalujte závislosti:

   pip install -r requirements.txt

4. Proveďte migrace databáze:

   python manage.py migrate

 5. python manage.py runserver

---

Aplikace poběží na adrese: http://127.0.0.1:8000

