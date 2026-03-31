@echo off

echo REAL .zd File Extractor
echo ======================
echo.

echo Select a REAL .zd file to extract:
echo.

rem Use PowerShell to create file dialog
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Title = 'Select a REAL .zd file to extract'; $dialog.Filter = 'ZD Files (*.zd)|*.zd|All Files (*.*)|*.*'; $dialog.InitialDirectory = '%CD%'; if ($dialog.ShowDialog() -eq 'OK') { $dialog.FileName } else { 'CANCELLED' } }" > temp_file.txt

set /p "selected_file=" < temp_file.txt
del temp_file.txt

if "%selected_file%"=="CANCELLED" (
    echo.
    echo No file selected. Operation cancelled.
    echo.
    pause
    exit /b 0
)

if "%selected_file%"=="" (
    echo.
    echo No file selected. Operation cancelled.
    echo.
    pause
    exit /b 0
)

set "input_file=%selected_file%"
for %%F in ("%selected_file%") do set "input_ext=%%~xF"

echo.
echo Selected file: %input_file%
echo.

if /i not "%input_ext%"==".zd" (
    echo Error: Selected file must have .zd extension
    echo Provided file: %input_file%
    echo.
    pause
    exit /b 1
)

if not exist "%input_file%" (
    echo Error: File not found: %input_file%
    echo.
    pause
    exit /b 1
)

rem Create extraction folder
for %%F in ("%selected_file%") do set "folder_name=%%~nF"
set "extract_folder=%folder_name%_extracted"

echo Extracting to folder: %extract_folder%
echo.

if exist "%extract_folder%" (
    echo Warning: Extraction folder already exists: %extract_folder%
    set /p "overwrite=Continue and overwrite existing files? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo Extraction cancelled.
        pause
        exit /b 0
    )
)

rem Create extraction folder
if not exist "%extract_folder%" mkdir "%extract_folder%"

echo Extracting REAL .zd file...
echo This requires the special .zd decoder!
echo.

python create_real_zd.py extract "%input_file%" "%extract_folder%"

if %errorlevel% equ 0 (
    echo.
    echo ✅ Successfully extracted %input_file% to %extract_folder%
    echo.
    
    rem Show extracted files
    echo Extracted files:
    dir /b "%extract_folder%"
    
    echo.
    echo Note: Only the REAL .zd extractor can read these files!
) else (
    echo.
    echo ❌ Failed to extract .zd file
    echo Make sure this is a REAL .zd file created with the special converter
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
