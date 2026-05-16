# scan_perms.ps1 — scan recent Claude Code transcripts and emit a histogram of
# tool calls that are good candidates for the permissions.allow allowlist in
# ~/.claude/settings.json.
#
# Configure $projectsRoot below if your Claude Code transcripts live elsewhere
# (default: ~/.claude/projects). The script reads the last 50 transcript .jsonl
# files, counts each Bash/PowerShell command head and each MCP tool method,
# and prints the ones with >=3 calls. Hand-pick the ones you want to allowlist.

$projectsRoot = "$env:USERPROFILE\.claude\projects"

$files = Get-ChildItem -Path $projectsRoot -Recurse -Filter "*.jsonl" -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending | Select-Object -First 50

$bashCounts = @{}
$mcpCounts = @{}
$bashExamples = @{}

foreach ($f in $files) {
  $lines = Get-Content -LiteralPath $f.FullName -ErrorAction SilentlyContinue
  foreach ($line in $lines) {
    if (-not $line) { continue }
    try { $obj = $line | ConvertFrom-Json -ErrorAction Stop } catch { continue }
    if ($obj.type -ne 'assistant') { continue }
    $content = $obj.message.content
    if (-not $content) { continue }
    foreach ($c in $content) {
      if ($c.type -ne 'tool_use') { continue }
      $name = $c.name
      if ($name -eq 'Bash' -or $name -eq 'PowerShell') {
        $cmd = $c.input.command
        if (-not $cmd) { continue }
        $cmd = $cmd.Trim()
        $first = ($cmd -split '(\|\||&&|;|\|)')[0].Trim()
        while ($first -match '^[A-Za-z_][A-Za-z0-9_]*=\S+\s+') {
          $first = $first -replace '^[A-Za-z_][A-Za-z0-9_]*=\S+\s+', ''
        }
        $tokens = $first -split '\s+'
        if ($tokens.Count -eq 0) { continue }
        $idx = 0
        while ($idx -lt $tokens.Count -and ($tokens[$idx] -in @('sudo','timeout','time','nohup','exec','&'))) { $idx++ }
        if ($idx -ge $tokens.Count) { continue }
        $cmd0 = $tokens[$idx]
        $cmd1 = if ($idx+1 -lt $tokens.Count) { $tokens[$idx+1] } else { '' }
        if ($cmd1 -and -not ($cmd1.StartsWith('-')) -and -not ($cmd1.StartsWith('"')) -and -not ($cmd1.StartsWith("'")) -and -not ($cmd1.StartsWith('$')) -and -not ($cmd1.Contains('/')) -and -not ($cmd1.Contains('\'))) {
          $key = "$name`::$cmd0 $cmd1"
        } else {
          $key = "$name`::$cmd0"
        }
        if ($bashCounts.ContainsKey($key)) { $bashCounts[$key]++ } else {
          $bashCounts[$key] = 1
          $bashExamples[$key] = $first.Substring(0, [Math]::Min(120, $first.Length))
        }
      } elseif ($name -like 'mcp__*') {
        if ($mcpCounts.ContainsKey($name)) { $mcpCounts[$name]++ } else { $mcpCounts[$name] = 1 }
      }
    }
  }
}

Write-Output "=== BASH/POWERSHELL (count >= 3) ==="
$bashCounts.GetEnumerator() | Where-Object { $_.Value -ge 3 } | Sort-Object Value -Descending | ForEach-Object {
  $ex = $bashExamples[$_.Key]
  "{0,4}  {1,-50}  {2}" -f $_.Value, $_.Key, $ex
}
Write-Output ""
Write-Output "=== MCP (count >= 3) ==="
$mcpCounts.GetEnumerator() | Where-Object { $_.Value -ge 3 } | Sort-Object Value -Descending | ForEach-Object {
  "{0,4}  {1}" -f $_.Value, $_.Key
}
