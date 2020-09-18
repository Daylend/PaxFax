@echo off
cmd /k "pushd %~dp0 & %~dp0\venv\Scripts\activate & python %~dp0\main.py & popd %~dp0"