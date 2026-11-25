# Stand-ins for Windows-only CIM cmdlets so the action's PowerShell can run on
# Linux under act. Get-CimInstance emits one fake sshd process per remaining
# count in $env:FAKE_SSH_COUNT_FILE (decrementing it), so tests can control how
# many polls report an active ssh session.
function Get-CimInstance {
    param([string]$ClassName, [string]$Filter)
    $countFile = $env:FAKE_SSH_COUNT_FILE
    if ($countFile -and (Test-Path $countFile)) {
        $n = [int]((Get-Content $countFile -Raw).Trim())
        if ($n -gt 0) {
            Set-Content -Path $countFile -Value ($n - 1)
            [pscustomobject]@{ Name = 'sshd.exe' }
        }
    }
}

function Get-CimAssociatedInstance {
    param(
        [Parameter(ValueFromPipeline = $true)] $InputObject,
        [string]$Association
    )
    process {
        if ($Association -eq 'Win32_LoggedOnUser') {
            [pscustomobject]@{ Name = 'testuser' }
        } else {
            $InputObject
        }
    }
}
