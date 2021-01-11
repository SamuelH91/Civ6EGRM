@echo off
setlocal EnableDelayedExpansion
SET TargetDir="%cd%"
:loop
IF EXIST "endGameReplay.py" (
  echo Found "endGameReplay.py" starting code
  python endGameReplay.py -d %TargetDir% %*
) ELSE (
  SET PreviousDir="!cd!"
  cd..
  IF !PreviousDir! == "!cd!" (
	echo Failed to find "endGameReplay.py" file from parent directories of %TargetDir%
	goto stop
  )
  goto loop
)
:stop
pause
