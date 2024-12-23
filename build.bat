call venv\Scripts\activate
pyinstaller --onefile --noconsole --add-data "version.json;." ProjectTemplate.py