@echo off

echo .zip to .zd Converter (DEBUG VERSION)
echo =====================================
echo.

echo Debug: Parameter received: "%~1"
echo.

if "%~1"=="" (
    echo Usage: convert_to_zd_debug.bat filename.zip
    echo.
    echo Drag and drop a .zip file onto this script to convert it to .zd
    echo Or run: convert_to_zd_debug.bat yourfile.zip
    echo.
    pause
    exit /b 1
)

set "input_file=%~1"
set "input_ext=%~x1"

echo Debug: Input file variable: "%input_file%"
echo Debug: Input extension: "%input_ext%"
echo.

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
    echo Debug: Current directory: %CD%
    echo Debug: Trying to check if file exists with full path...
    dir "%input_file%" 2>nul
    echo.
    pause
    exit /b 1
)

set "output_file=%~dpn1.zd"

echo Debug: Output file variable: "%output_file%"
echo Debug: Output file breakdown:
echo   - Drive: "%~d1"
echo   - Path: "%~p1" 
echo   - Name: "%~n1"
echo   - Extension: .zd
echo.

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

echo Debug: Attempting to copy file...
copy "%input_file%" "%output_file%"

echo Debug: Copy command error level: %errorlevel%

if %errorlevel% equ 0 (
    echo.
    echo Successfully converted %input_file% to %output_file%
    echo.
    echo Debug: Verifying output file exists...
    if exist "%output_file%" (
        echo Debug: Output file confirmed to exist!
        dir "%output_file%"
    ) else (
        echo Debug: WARNING - Output file not found after copy!
    )
    echo.
    echo Note: .zd files are an alternative format to .zip files
    echo They contain the same compressed data but with a different extension
) else (
    echo.
    echo Error during conversion
    echo Debug: Error level: %errorlevel%
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
