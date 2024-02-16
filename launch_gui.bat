@echo off
SET VENV=venv

:: Check if the virtual environment exists
IF NOT EXIST "%VENV%" (
    echo Creating virtual environment...
    python -m venv %VENV%
    echo Virtual environment created.
    
    echo Activating virtual environment...
    CALL %VENV%\Scripts\activate.bat
    
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo Dependencies installed.
) ELSE (
    echo Activating virtual environment...
    CALL %VENV%\Scripts\activate.bat
)

:: Check if main/main.csv exists and run data_processing.py if it does not exist
IF NOT EXIST "main\main.csv" (
    echo main/main.csv not found. Running data_processing.py...
    python main/data_processing.py
    echo data_processing.py execution completed.
)

:: Run gui.py
echo Running gui.py...
python main/gui.py
echo gui.py execution completed.

pause
