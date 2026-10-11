#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#WinActivateForce

target_progrem := "ahk_exe labview.exe"

; CTRL + Right Click = hot swap
^RButton::
	ifWinActive, ahk_exe POWERPNT.EXE
	{
		ifWinExist, %target_progrem%
		{
			; leave presentation if in one
			Send, {Esc}
			; activate target program
			WinActivate, %target_progrem%
			return ; block Windows from getting the hotkey
		}
	}
	else ; otherwise
	{
		ifWinExist, ahk_exe POWERPNT.EXE ; if Powerpoint is open
		{
			WinActivate ; activate it
			
			; and resume slide deck where we left off
			Send, +{F5} 
			return ; block Windows from getting the hotkey
		}
	}


