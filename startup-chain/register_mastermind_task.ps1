# register_mastermind_task.ps1
# ============================
# Registers the ClaudeCodeLauncher Scheduled Task that fires the AHK launcher.
# Idempotent — re-running re-creates the task with current settings.
#
# Run elevated (Run as Administrator) — Scheduled Task creation requires it.
#
# Replace placeholders before running:
#   {AHK_SCRIPT_PATH}     — absolute path to start_mastermind_in_ide.ahk
#   {AHK_EXE_PATH}        — absolute path to AutoHotkey64.exe (typically
#                           C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe)
#   {YOUR_WINDOWS_USER}   — your Windows username (this user runs the task)

$TaskName     = "ClaudeCodeLauncher"
$AhkExe       = "{AHK_EXE_PATH}"
$AhkScript    = "{AHK_SCRIPT_PATH}"
$RunAsUser    = "{YOUR_WINDOWS_USER}"

# Action — run AHK with the launcher script.
$action = New-ScheduledTaskAction `
    -Execute $AhkExe `
    -Argument "`"$AhkScript`""

# No trigger — the task is fired manually by StartMastermind.bat via
# `schtasks /run /tn ClaudeCodeLauncher`. (You CAN add a trigger here for logon,
# but the .bat approach gives explicit boot-ping logging.)
$trigger = $null

# Run as the current user with highest privileges available (LUA — limited user
# is fine if you don't need elevated rights inside the AHK launcher).
$principal = New-ScheduledTaskPrincipal `
    -UserId $RunAsUser `
    -LogonType Interactive `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Register (or replace).
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Write-Host "Removing existing $TaskName task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Principal $principal `
    -Settings $settings `
    -Description "Mastermind: opens IDE terminal and launches Claude Code on boot. Triggered by StartMastermind.bat."

Write-Host "Registered $TaskName."
Write-Host "Test with: schtasks /run /tn $TaskName"
