call venv\Scripts\activate
FOR /R %%G in (*.ui) DO (
 pyside6-uic %%G -o %%~pG/ui_%%~nG.py
)
