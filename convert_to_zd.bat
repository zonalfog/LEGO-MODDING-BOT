@echo off

echo .zip to .zd Converter
echo =====================
echo.

if "%~1"=="" (
    echo Usage: convert_to_zd.bat filename.zip
    echo.
    echo Drag and drop a .zip file onto this script to convert it to .zd
    echo Or run: convert_to_zd.bat yourfile.zip
    echo.
    pause
    exit /b 1
)

set "input_file=%~1"
set "input_ext=%~x1"

if /i not "%input_ext%"==".zip" (
    echo Error: File must have .zip extension
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

echo Input file: %input_file%
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
