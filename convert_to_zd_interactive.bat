@echo off

echo .zip to .zd Converter (Interactive)
echo ===================================
echo.

echo Please select a .zip file to convert:
echo.

rem Use PowerShell to create file dialog
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Title = 'Select a .zip file to convert'; $dialog.Filter = 'ZIP Files (*.zip)|*.zip|All Files (*.*)|*.*'; $dialog.InitialDirectory = '%CD%'; if ($dialog.ShowDialog() -eq 'OK') { $dialog.FileName } else { 'CANCELLED' } }" > temp_file.txt

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

if /i not "%input_ext%"==".zip" (
    echo Error: Selected file must have .zip extension
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

set "output_file=%~dpn1.zd"

echo Output file: %output_file%
echo.

if exist "%output_file%" (
    echo Warning: Output file already exists: %output_file%
    set /p "overwrite=Overwrite? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo Conversion cancelled.
        pause
        exit /b 0
    )
)

echo Converting...
copy "%input_file%" "%output_file%" >nul

if %errorlevel% equ 0 (
    echo.
    echo Successfully converted %input_file% to %output_file%
    echo.
    echo Note: .zd files are an alternative format to .zip files
    echo They contain the same compressed data but with a different extension
) else (
    echo.
    echo Error during conversion
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
