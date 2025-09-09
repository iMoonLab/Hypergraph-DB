@echo off
REM Hypergraph-DB Development Commands

if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="docs" goto docs
if "%1"=="docs-serve" goto docs-serve
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="help" goto help
goto help

:install
echo Installing package dependencies...
uv sync
goto end

:install-dev
echo Installing package with development dependencies...
uv sync --extra dev
goto end

:test
echo Running tests...
uv run pytest tests/
goto end

:lint
echo Running linting checks...
uv run black --check hyperdb/ tests/
uv run isort --check-only hyperdb/ tests/
goto end

:format
echo Formatting code...
uv run black hyperdb/ tests/
uv run isort hyperdb/ tests/
goto end

:docs
echo Building documentation...
uv run --extra docs mkdocs build
goto end

:docs-serve
echo Serving documentation locally...
uv run --extra docs mkdocs serve
goto end

:clean
echo Cleaning build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"
goto end

:build
call :clean
echo Building package...
uv build
goto end

:help
echo Available commands:
echo   install     - Install package dependencies
echo   install-dev - Install package with development dependencies
echo   test        - Run tests
echo   lint        - Run linting checks
echo   format      - Format code with black and isort
echo   docs        - Build documentation
echo   docs-serve  - Serve documentation locally
echo   clean       - Clean build artifacts
echo   build       - Build package
echo.
echo Usage: dev.bat [command]
goto end

:end
