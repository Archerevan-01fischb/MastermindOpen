# check_updates.ps1
# =================
# Daily 7am Scheduled Task that polls for new Claude Code releases and queues
# noteworthy findings to <memory_dir>/pending_self_improvement.md.
#
# Mastermind reads pending_self_improvement.md at session start (Active Resume,
# hook #3) and surfaces non-empty content to you. After discussion, you clear
# the entries.
#
# This is half of the "self-improvement loop." The other half is the startup
# hook surface that reads the file. See ../docs/self-improvement-loop.md.
#
# Replace placeholders before scheduling:
#   {MEMORY_DIR}      — your mastermind memory directory
#   {STATE_FILE}      — path to a tiny state file tracking the last-seen version
#
# Schedule with:
#   schtasks /create /tn "MastermindCheckUpdates" /tr "powershell -NoProfile -ExecutionPolicy Bypass -File <this>" /sc daily /st 07:00 /ru "<user>"

$ErrorActionPreference = 'Stop'

$MemoryDir   = "{MEMORY_DIR}"
$PendingFile = Join-Path $MemoryDir "pending_self_improvement.md"
$StateFile   = "{STATE_FILE}"
$ChangelogUrl = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"

function Log($msg) {
    Write-Host "[$([DateTime]::Now.ToString('yyyy-MM-dd HH:mm:ss'))] $msg"
}

# Pull the changelog.
try {
    $changelog = Invoke-WebRequest -Uri $ChangelogUrl -UseBasicParsing -TimeoutSec 30 | Select-Object -ExpandProperty Content
} catch {
    Log "Failed to fetch changelog: $_"
    exit 1
}

# Find the most recent version heading. Common pattern: "## v2.1.123" or "## 2.1.123".
$versionMatch = [regex]::Match($changelog, '(?m)^##\s+v?([0-9]+\.[0-9]+\.[0-9]+)')
if (-not $versionMatch.Success) {
    Log "No version heading found in changelog."
    exit 0
}
$latestVersion = $versionMatch.Groups[1].Value

# Load last-seen version.
$lastSeen = ""
if (Test-Path $StateFile) {
    $lastSeen = (Get-Content $StateFile -Raw).Trim()
}

if ($lastSeen -eq $latestVersion) {
    Log "No new release (still on v$latestVersion)."
    exit 0
}

# Extract the section for the latest version.
# Crude: take from the latest-version heading to the next heading.
$startIdx = $versionMatch.Index
$nextHeading = [regex]::Match($changelog.Substring($startIdx + 1), '(?m)^##\s+')
$endIdx = if ($nextHeading.Success) { $startIdx + 1 + $nextHeading.Index } else { $changelog.Length }
$section = $changelog.Substring($startIdx, $endIdx - $startIdx).Trim()

# Append to the pending file.
$today = [DateTime]::Now.ToString('yyyy-MM-dd')
$entry = @"

## $today — Claude Code v$latestVersion released

$section

Discuss with mastermind at next session start. Clear this entry after discussion.

"@

# Ensure pending file has its frontmatter header.
if (-not (Test-Path $PendingFile)) {
    @"
---
name: Pending Self-Improvement Topics
description: Claude Code releases not yet discussed. Auto-populated daily.
type: project
---
# Pending Self-Improvement Topics

Surface highlights at session start. Clear entries after discussion.
"@ | Set-Content -Path $PendingFile -Encoding UTF8
}

Add-Content -Path $PendingFile -Value $entry -Encoding UTF8

# Update state file.
$latestVersion | Set-Content -Path $StateFile -Encoding UTF8

Log "Queued v$latestVersion to $PendingFile."
