@echo off
echo Starting Blockchain Client...
echo.

REM Run the client executable
BlockchainClient.exe

REM Check if error log exists and show it
if exist client_error.log (
    echo.
    echo Error log found. Here are the most recent errors:
    echo.
    type client_error.log
)

echo.
pause