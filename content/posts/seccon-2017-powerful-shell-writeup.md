+++
title = "SECCON 2017 - Powerful_Shell Writeup"
date = "2017-12-11 10:27:58"
categories = ["rev", "writeup"]
+++

> Powerful\_Shell 300 points Powerful\_Shell Crack me. powerful_shell.ps1-1fb3af91eafdbebf3b3efa3b84fcc10cfca21ab53db15c98797b500c739b0024 [Download](https://a.safe.moe/fmq8i.ps1-1fb3af91eafdbebf3b3efa3b84fcc10cfca21ab53db15c98797b500c739b0024)

Diberikan sebuah file powershell. Untuk menjalankan filenya, bisa menggunakan pwsh di Linux/PowerShell di Windows.

```
$ECCON="";
$ECCON+=\[char\](3783/291);
$ECCON+=\[char\](6690/669);
$ECCON+=\[char\](776-740);
$ECCON+=\[char\](381-312);
$ECCON+=\[char\](403-289);
$ECCON+=\[char\](-301+415);
$ECCON+=\[char\](143-32);
$ECCON+=\[char\](93594/821);
....
$ECCON+=\[char\](721-708);
$ECCON+=\[char\](803-793);
$ECCON+=\[char\](10426/802);
Write-Progress -Activity "Extracting Script" -status "20040" -percentComplete 99;
$ECCON+=\[char\](520-510);
Write-Progress -Completed -Activity "Extracting Script";.(\[ScriptBlock\]::Create($ECCON))
```

Hmm... seems legit. File ini akan mengeksekusi sesuatu di $ECCON. Nah, daripada dieksekusi drop saja variabel $ECCON ke suatu file agar bisa di analisa lebih lanjut dengan mengganti line terakhir menjadi

```
...
$ECCON+=\[char\](721-708);
$ECCON+=\[char\](803-793);
$ECCON+=\[char\](10426/802);
Write-Progress -Activity "Extracting Script" -status "20040" -percentComplete 99;
$ECCON+=\[char\](520-510);
$ECCON >> eccon.ps1
```

Output dari eccon.ps1 seperti berikut,

```
$ErrorActionPreference = "ContinueSilently"
\[console\]::BackgroundColor = "black";\[console\]::ForegroundColor = "white";cls;Set-Alias -Name x -Value Write-Host;$host.UI.RawUI.BufferSize = New-Object System.Management.Automation.Host.Size 95,25;$host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size 95,25;$host.UI.RawUI.BufferSize = New-Object System.Management.Automation.Host.Size 95,25;$host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size 95,25;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 12 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 0 -n;x '  ' -b 15 -n;x;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x '  ' -b 15 -n;x;x;


Write-Host -b 00 -f 15 Checking Host... Please wait... -n
Try{
    If ((Get-EventLog -LogName Security | Where EventID -Eq 4624).Length -Lt 1000) {
        Write-Host "This host is too fresh!"
        Exit
    }
}Catch{
    Write-Host "Failed: No admin rights!"
    Exit
}
Write-Host "Check passed"

$keytone=@{'a'=261.63}
$pk='a'
ForEach($k in ('w','s','e','d','f','t','g','y','h','u','j','k')){
    $keytone+=@{$k=$keytone\[$pk\]*\[math\]::pow(2,1/12)};$pk=$k    
}
Write-Host -b 00 -f 15 "Play the secret melody."

Write-Host -b 15 -f 00 -n '   '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '   |   '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 '   |    ' 
Write-Host -b 15 -f 00 -n '   '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '   |   '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n '   '
Write-Host -b 15 -f 00 '   |    ' 
Write-Host -b 15 -f 00 -n '   '
Write-Host -b 00 -f 15 -n ' w '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n ' e '
Write-Host -b 15 -f 00 -n '   |   '
Write-Host -b 00 -f 15 -n ' t '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n ' y '
Write-Host -b 15 -f 00 -n '  '
Write-Host -b 00 -f 15 -n ' u '
Write-Host -b 15 -f 00 '   |    ' 
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00  '    '
Write-Host -b 15 -f 00 -n '  a |'
Write-Host -b 15 -f 00 -n '  s |'
Write-Host -b 15 -f 00 -n '  d |'
Write-Host -b 15 -f 00 -n '  f |'
Write-Host -b 15 -f 00 -n '  g |'
Write-Host -b 15 -f 00 -n '  h |'
Write-Host -b 15 -f 00 -n '  j |'
Write-Host -b 15 -f 00  '  k '
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00 -n '    |'
Write-Host -b 15 -f 00  '    '
Write-Host
$stage1=@();$f="";
While($stage1.length -lt 14){
    $key=(Get-Host).ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    $k=\[String\]$key.Character
    $f+=$k;
    If($keytone.Contains($k)){
        $stage1+=\[math\]::floor($keytone\[$k\])
        \[console\]::beep($keytone\[$k\],500)
    }
}
$secret=@(440,440,493,440,440,493,440,493,523,493,440,493,440,349)
If($secret.length -eq $stage1.length){
    For ($i=1; $i -le $secret.length; $i++) {
        If($secret\[$i\] -ne $stage1\[$i\]){
            Exit
        }
    }
    x "Correct. Move to the next stage."
}
$text=@"
YkwRUxVXQ05DQ1NOE1sVVU4TUxdTThBBFVdDTUwTURVTThMqFldDQUwdUxVRTBNEFVdAQUwRUxtT
TBEzFVdDQU8RUxdTbEwTNxVVQUNOEFEVUUwdQBVXQ0NOE1EWUUwRQRtVQ0FME1EVUU8RThdVTUNM
EVMVUUwRFxdVQUNCE1MXU2JOE0gWV0oxSk1KTEIoExdBSDBOE0MVO0NKTkAoERVDSTFKThNNFUwR
FBVINUFJTkAqExtBSjFKTBEoF08RVRdKO0NKTldKMUwRQBc1QUo7SlNgTBNRFVdJSEZCSkJAKBEV
QUgzSE8RQxdMHTMVSDVDSExCKxEVQ0o9SkwRQxVOE0IWSDVBSkJAKBEVQUgzThBXFTdDRExAKhMV
Q0oxTxEzFzVNSkxVSjNOE0EWN0NITE4oExdBSjFMEUUXNUNTbEwTURVVSExCKxEVQ0o9SkwRQxVO
EzEWSDVBSkJAKBEVQUgzThAxFTdDREwTURVKMUpOECoVThNPFUo3U0pOE0gWThNEFUITQBdDTBFK
F08RQBdMHRQVQUwTSBVOEEIVThNPFUNOE0oXTBFDF0wRQRtDTBFKFU4TQxZOExYVTUwTSBVMEUEX
TxFOF0NCE0oXTBNCFU4QQRVBTB1KFU4TThdMESsXQ04TRBVMEUMVThNXFk4TQRVNTBNIFUwRFBdP
EUEXQ0ITShdME0EVThBXFU4TWxVDThNKF0wRMBdMETUbQ0wRShVOE0MWThMqFU1ME0gVTBFDF08R
QxdMHUMVQUwTSBVOEEEVThNNFUwRNRVBTBFJF0wRQxtME0EVTBFAF0BOE0gVQhNGF0wTKhVBTxFK
F0wdMxVOEzUXQ04QSBVOE0AVTBFVFUFMEUkXTBFDG0wTQRVMETMXQE4TSBVCE0MXTBNBFU4QQRVB
TB1KFU4TQxdMEVYXTBEUG0NMEUoVThNBFk4TQRVCEygXQ0wRShdPEUMXTB1DFU4TQBdDThBIFU4T
SBVMESgVQUwRSRdMEUYbTBMWFUNOE0gWThNCFUITFBdDTBFKF08RQxdMHUMVThNVF0NOEEgVThNN
FUwRQxVOE0IWQUwRShtME0EVTBFVF08RQxdDQhNKF0wTQRVOEEEVThM9FUNOE0oXTBFFF0wRKBtD
TBFKFU4TQRZOE0EVQhNAF0NMEUoXTxFDF0wdVRVOEzMXQ04QSBVOE00VTBFVFU4TQRZBTBFKG0wT
RBVMESgXQE4TSBVCE0MXTBNBFU4QKhVBTB1KFU4TFBdMEUIXQ04TRBVMEUMVThNBFk4TNxVNTBNI
FUwRQxdPEUMXTB01FUFME0gVThBBFU4TTRVMERQVQUwRSRdMEUMbTBNBFUwRQxdAThNIFUITQxdM
E0EVThAxFUFMHUoVThNDF0wRVhdMEVUbQ0wRShVOE0QWThMWFU1ME0gVTBFDF08RRhdDQhNKF0wT
QRVOEFcVQUwdShVOE0EXTBFFF0NOE0QVTBFDFU4TVxZOEyoVTUwTSBVMETMXTxFVF0NCE0oXTBNE
FU4QQhVBTB1KFU4TQBdMERcXQ04TRBVMEUAVThNDFkFMEUobTBNCFUwRQRdAThNIFUITQRdMExYV
QU8RShdMHUEVThNOF0NOEEgVThNIFUwRKBVBTBFJF0wRMxtMEzcVQ04TSBZOE0EVQhNVF0wTQRVB
TxFKF0wdQxVOE0MXTBFFF0NOE0QVTBFGFU4TKhZBTBFKG0wTRBVMERQXQE4TSBVCE04XTBNXFUFP
EUoXTB0zFU4TThdDThBIFU4TTRVMEUMVThMWFkFMEUobTBNCFUwRFBdAThNIFUITQxdME0EVThAx
FUFMHUoVThNGF0wRQxdDThNEFUwRQRVOEyoWQUwRShtMEzcVTBFDF0BOE0gVQhMzF0wTFhVBTxFK
F0wdMxVOExQXQ04QSBVOE0gVTBEUFUFMEUkXTBEzG0wTQRVDThNIFk4TQRVCEygXTBNEFUFPEUoX
TB1DFU4TRhdDThBIFU4TTRVMEVUVQUwRSRdMERQbQ0wRShVOE0wWThNDFU1ME0gVTBFDF08RQxdM
HTMVQUwTSBVOEEEVThNbFUwRNRVBTBFJF0wRQxtME0EVTBFAF0BOE0gVQhNDF0wTVxVOEEEVQUwd
ShVOEzMXTBE2F0NOE0QVTBFBFU4TKhZBTBFKG0wTQRVMEUMXTxFDF0NCE0oXTBNBFU4QQRVOEzsV
Q04TShdMEUAXTBFDG0wTQhVDThNIFk4TRBVCEygXQ0wRShdPEUYXTB0UFUFME0gVThBDFU4TTRVD
ThNKF0wRQBdMEUMbTBNBFUNOE0gWThNBFUITQxdME0EVQU8RShdMHUMVThNVF0wRVhdDThNEFUwR
RhVOEyoWQUwRShtME0MVTBEzF0BOE0gVQhNDF0wTQRVOEEEVQUwdShVOExQXTBFNF0NOE0QVTBFG
FU4TRBZBTBFKG0wTRBVMERQXQE4TSBVCEzUXTBMWFUFPEUoXTB1DFU4TRhdDThBIFU4TTRVMEVUV
QUwRSRdMERQbQ0wRShVOE0wWThNDFU1ME0gVTBFDF08RQxdMHTMVQUwTSBVOEEEVThNbFUwRNRVB
TBFJF0wRQxtME0EVTBFAF0BOE0gVQhNDF0wTVxVOEEEVQUwdShVOEzMXTBE2F0NOE0QVTBFBFU4T
KhZBTBFKG0wTQRVMEUMXTxFDF0NCE0oXTBNBFU4QQRVOEzsVQ04TShdMEUAXTBFDG0wTQhVDThNI
Fk4TRBVCEygXQ0wRShdPEUYXTB0zFUFME0gVThBMFU4TSBVDThNKF0wRQxdMERQbQ0wRShVOE0IW
ThNDFU1ME0gVTBFAF08RQRdDQhNKF0wTQxVOEBYVQUwdShVOE0EXTBFNF0NOE0QVTBFDFU4TKhZO
E0QVTUwTSBVMEUYXTxFAF0NCE0oXTBNCFU4QFhVBTB1KFU4TQBdMEUIXQ04TRBVMEUAVThNDFkFM
EUobTBNDFUwRFBdAThNIFUITQRdME0wVQU8RShdMHUMVThMoF0wRNhdDThNEFUwRRhVOEzEWQUwR
ShtME0EVTBFGF0BOE0gVQhNDF0wTVxVBTxFKF0wdQxVOEygXTBE2FxROE10VShZOTBFTF2E=
"@

$plain=@()
$byteString = \[System.Convert\]::FromBase64String($text)
$xordData = $(for ($i = 0; $i -lt $byteString.length; ) {
    for ($j = 0; $j -lt $f.length; $j++) {
        $plain+=$byteString\[$i\] -bxor $f\[$j\]
        $i++
        if ($i -ge $byteString.Length) {
            $j = $f.length
        }
    }
})
iex(\[System.Text.Encoding\]::ASCII.GetString($plain))
```

Uh oh.. masih bersangkutan dengan Powershell lagi. Script ini juga akan mengeksekusi sesuatu di variabel `plain`. `plain` ini didapat dari `bas64decode($text)` yang dixor dengan `f`. `f` sendiri didapat dengan membandingkan input `stage1` dengan `secret`.

```
$stage1=@();$f="";
While($stage1.length -lt 14){
    $key=(Get-Host).ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    $k=\[String\]$key.Character
    $f+=$k;
    If($keytone.Contains($k)){
        $stage1+=\[math\]::floor($keytone\[$k\])
        \[console\]::beep($keytone\[$k\],500)
    }
}
$secret=@(440,440,493,440,440,493,440,493,523,493,440,493,440,349)
If($secret.length -eq $stage1.length){
    For ($i=1; $i -le $secret.length; $i++) {
        If($secret\[$i\] -ne $stage1\[$i\]){
            Exit
        }
    }
    x "Correct. Move to the next stage."
}
```

`stage1` ini diperoleh nilai floor dari `keytone`. Untuk mengetahui value dari `keytone*`, jalanlkan sebagian code yang didapat dari script ini,

```
$keytone=@{'a'=261.63}
$pk='a'
ForEach($k in ('w','s','e','d','f','t','g','y','h','u','j','k')){
    $keytone+=@{$k=$keytone\[$pk\]*\[math\]::pow(2,1/12)};$pk=$k    
}
```
Value dari keytone

| Name |    Value         |
|------|------------------|
|   t  | 370.000694323673
|   e  | 311.132257498162
|   w  | 277.187329377222
|   d  | 329.633144283996
|   a  | 261.63
|   g  | 392.002080523246
|   s  | 293.669745699181
|   k  | 523.26
|   u  | 466.171663254114
|   j  | 493.891672853823
|   y  | 415.31173722644
|   f  | 349.234151046506
|   h  | 440.007458245659

Bandingkan dengan $secret

```
$secret=@(440,440,493,440,440,493,440,493,523,493,440,493,440,349)
```

`440 -> h 440 -> h 493 -> j ...` Nah, dari hasil nguli didapat `$f = hhjhhjhjkjhjhf`. Pakai python buat xor decrypt $text dengan key $f. Lalu didapatkan.... masih script Powershell `lagi`. Berikut scriptnya,

```
${;}=+$();
${=}=${;};
${+}=++${;};
${@}=++${;};
${.}=++${;};
${\[}=++${;};
${\]}=++${;};
${(}=++${;};
${)}=++${;};
${&}=++${;};
${|}=++${;};
${"}="\["+"$(@{})"\[${)}\]+"$(@{})"\["${+}${|}"\]+"$(@{})"\["${@}${=}"\]+"$?"\[${+}\]+"\]";
${;}="".("$(@{})"\["${+}${\[}"\]+"$(@{})"\["${+}${(}"\]+"$(@{})"\[${=}\]+"$(@{})"\[${\[}\]+"$?"\[${+}\]+"$(@{})"\[${.}\]);
${;}="$(@{})"\["${+}${\[}"\]+"$(@{})"\[${\[}\]+"${;}"\["${@}${)}"\];"${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${(}${+}+${"}${&}${@}+${"}${+}${=}${+}+${"}${|}${)}+${"}${+}${=}${=}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${\[}${\]}+${"}${&}${=}+${"}${+}${+}${\[}+${"}${+}${+}${+}+${"}${+}${=}${|}+${"}${+}${+}${@}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${|}+${"}${(}${|}+${"}${+}${+}${=}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${+}${+}${\[}+${"}${.}${@}+${"}${+}${+}${(}+${"}${+}${=}${\[}+${"}${+}${=}${+}+${"}${.}${@}+${"}${+}${+}${@}+${"}${|}${)}+${"}${+}${+}${\]}+${"}${+}${+}${\]}+${"}${+}${+}${|}+${"}${+}${+}${+}+${"}${+}${+}${\[}+${"}${+}${=}${=}+${"}${.}${|}+${"}${+}${.}+${"}${+}${=}+${"}${)}${.}+${"}${+}${=}${@}+${"}${\[}${=}+${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${.}${@}+${"}${\[}${\]}+${"}${+}${=}${+}+${"}${+}${+}${.}+${"}${.}${@}+${"}${.}${|}+${"}${&}${=}+${"}${\[}${&}+${"}${+}${+}${|}+${"}${(}${|}+${"}${+}${+}${\[}+${"}${.}${(}+${"}${)}${@}+${"}${\]}${+}+${"}${\[}${|}+${"}${\[}${|}+${"}${.}${|}+${"}${\[}${+}+${"}${+}${@}${.}+${"}${+}${.}+${"}${+}${=}+${"}${|}+${"}${&}${)}+${"}${+}${+}${\[}+${"}${+}${=}${\]}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${|}+${"}${)}${+}+${"}${+}${+}${+}+${"}${+}${+}${+}+${"}${+}${=}${=}+${"}${.}${@}+${"}${)}${\[}+${"}${+}${+}${+}+${"}${|}${&}+${"}${.}${.}+${"}${.}${|}+${"}${\]}${|}+${"}${+}${.}+${"}${+}${=}+${"}${|}+${"}${&}${)}+${"}${+}${+}${\[}+${"}${+}${=}${\]}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${\[}+${"}${&}${.}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${+}${@}${.}+${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${+}${@}${\]}+${"}${.}${\[}+${"}${+}${.}+${"}${+}${=}+${"}${+}${@}${\]}|${;}"|&${;}
```

Oh, wow. Much code. Such Obfucate. Intinya, masih sama seperti pada sebelumnya, dengan menggunakan teknik drop value (read: echo) pada variabel satu-persatu.

```
PS /home/kyra/Downloads> ${;}=+$();
PS /home/kyra/Downloads> ${=}=${;};
PS /home/kyra/Downloads> ${+}=++${;};
PS /home/kyra/Downloads> ${@}=++${;};
PS /home/kyra/Downloads> ${.}=++${;};
PS /home/kyra/Downloads> ${\[}=++${;};
PS /home/kyra/Downloads> ${\]}=++${;};
PS /home/kyra/Downloads> ${(}=++${;};
PS /home/kyra/Downloads> ${)}=++${;};
PS /home/kyra/Downloads> ${&}=++${;};
PS /home/kyra/Downloads> ${|}=++${;};
PS /home/kyra/Downloads> ${"}="\["+"$(@{})"\[${)}\]+"$(@{})"\["${+}${|}"\]+"$(@{})"\["${@}${=}"\]+"$?"\[${+}\]+"\]";
PS /home/kyra/Downloads> ${;}="".("$(@{})"\["${+}${\[}"\]+"$(@{})"\["${+}${(}"\]+"$(@{})"\[${=}\]+"$(@{})"\[${\[}\]+"$?"\[${+}\]+"$(@{})"\[${.}\]);
PS /home/kyra/Downloads> ${;}="$(@{})"\["${+}${\[}"\]+"$(@{})"\[${\[}\]+"${;}"\["${@}${)}"\];"${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${(}${+}+${"}${&}${@}+${"}${+}${=}${+}+${"}${|}${)}+${"}${+}${=}${=}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${\[}${\]}+${"}${&}${=}+${"}${+}${+}${\[}+${"}${+}${+}${+}+${"}${+}${=}${|}+${"}${+}${+}${@}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${|}+${"}${(}${|}+${"}${+}${+}${=}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${+}${+}${\[}+${"}${.}${@}+${"}${+}${+}${(}+${"}${+}${=}${\[}+${"}${+}${=}${+}+${"}${.}${@}+${"}${+}${+}${@}+${"}${|}${)}+${"}${+}${+}${\]}+${"}${+}${+}${\]}+${"}${+}${+}${|}+${"}${+}${+}${+}+${"}${+}${+}${\[}+${"}${+}${=}${=}+${"}${.}${|}+${"}${+}${.}+${"}${+}${=}+${"}${)}${.}+${"}${+}${=}${@}+${"}${\[}${=}+${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${.}${@}+${"}${\[}${\]}+${"}${+}${=}${+}+${"}${+}${+}${.}+${"}${.}${@}+${"}${.}${|}+${"}${&}${=}+${"}${\[}${&}+${"}${+}${+}${|}+${"}${(}${|}+${"}${+}${+}${\[}+${"}${.}${(}+${"}${)}${@}+${"}${\]}${+}+${"}${\[}${|}+${"}${\[}${|}+${"}${.}${|}+${"}${\[}${+}+${"}${+}${@}${.}+${"}${+}${.}+${"}${+}${=}+${"}${|}+${"}${&}${)}+${"}${+}${+}${\[}+${"}${+}${=}${\]}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${|}+${"}${)}${+}+${"}${+}${+}${+}+${"}${+}${+}${+}+${"}${+}${=}${=}+${"}${.}${@}+${"}${)}${\[}+${"}${+}${+}${+}+${"}${|}${&}+${"}${.}${.}+${"}${.}${|}+${"}${\]}${|}+${"}${+}${.}+${"}${+}${=}+${"}${|}+${"}${&}${)}+${"}${+}${+}${\[}+${"}${+}${=}${\]}+${"}${+}${+}${(}+${"}${+}${=}${+}+${"}${\[}${\]}+${"}${)}${@}+${"}${+}${+}${+}+${"}${+}${+}${\]}+${"}${+}${+}${(}+${"}${.}${@}+${"}${.}${\[}+${"}${&}${.}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${+}${@}${.}+${"}${.}${(}+${"}${(}${|}+${"}${(}${)}+${"}${(}${)}+${"}${)}${|}+${"}${)}${&}+${"}${+}${@}${\]}+${"}${.}${\[}+${"}${+}${.}+${"}${+}${=}+${"}${+}${@}${\]}|${;}"
\[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]61+\[CHar\]82+\[CHar\]101+\[CHar\]97+\[CHar\]100+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]45+\[CHar\]80+\[CHar\]114+\[CHar\]111+\[CHar\]109+\[CHar\]112+\[CHar\]116+\[CHar\]32+\[CHar\]39+\[CHar\]69+\[CHar\]110+\[CHar\]116+\[CHar\]101+\[CHar\]114+\[CHar\]32+\[CHar\]116+\[CHar\]104+\[CHar\]101+\[CHar\]32+\[CHar\]112+\[CHar\]97+\[CHar\]115+\[CHar\]115+\[CHar\]119+\[CHar\]111+\[CHar\]114+\[CHar\]100+\[CHar\]39+\[CHar\]13+\[CHar\]10+\[CHar\]73+\[CHar\]102+\[CHar\]40+\[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]32+\[CHar\]45+\[CHar\]101+\[CHar\]113+\[CHar\]32+\[CHar\]39+\[CHar\]80+\[CHar\]48+\[CHar\]119+\[CHar\]69+\[CHar\]114+\[CHar\]36+\[CHar\]72+\[CHar\]51+\[CHar\]49+\[CHar\]49+\[CHar\]39+\[CHar\]41+\[CHar\]123+\[CHar\]13+\[CHar\]10+\[CHar\]9+\[CHar\]87+\[CHar\]114+\[CHar\]105+\[CHar\]116+\[CHar\]101+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]39+\[CHar\]71+\[CHar\]111+\[CHar\]111+\[CHar\]100+\[CHar\]32+\[CHar\]74+\[CHar\]111+\[CHar\]98+\[CHar\]33+\[CHar\]39+\[CHar\]59+\[CHar\]13+\[CHar\]10+\[CHar\]9+\[CHar\]87+\[CHar\]114+\[CHar\]105+\[CHar\]116+\[CHar\]101+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]34+\[CHar\]83+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]123+\[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]125+\[CHar\]34+\[CHar\]13+\[CHar\]10+\[CHar\]125|iex
```

Hm...? Another string again? Coba run untuk bagian yang banyak \[CHar\]-nya

```
PS /home/kyra/Downloads> \[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]61+\[CHar\]82+\[CHar\]101+\[CHar\]97+\[CHar\]100+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]45+\[CHar\]80+\[CHar\]114+\[CHar\]111+\[CHar\]109+\[CHar\]112+\[CHar\]116+\[CHar\]32+\[CHar\]39+\[CHar\]69+\[CHar\]110+\[CHar\]116+\[CHar\]101+\[CHar\]114+\[CHar\]32+\[CHar\]116+\[CHar\]104+\[CHar\]101+\[CHar\]32+\[CHar\]112+\[CHar\]97+\[CHar\]115+\[CHar\]115+\[CHar\]119+\[CHar\]111+\[CHar\]114+\[CHar\]100+\[CHar\]39+\[CHar\]13+\[CHar\]10+\[CHar\]73+\[CHar\]102+\[CHar\]40+\[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]32+\[CHar\]45+\[CHar\]101+\[CHar\]113+\[CHar\]32+\[CHar\]39+\[CHar\]80+\[CHar\]48+\[CHar\]119+\[CHar\]69+\[CHar\]114+\[CHar\]36+\[CHar\]72+\[CHar\]51+\[CHar\]49+\[CHar\]49+\[CHar\]39+\[CHar\]41+\[CHar\]123+\[CHar\]13+\[CHar\]10+\[CHar\]9+\[CHar\]87+\[CHar\]114+\[CHar\]105+\[CHar\]116+\[CHar\]101+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]39+\[CHar\]71+\[CHar\]111+\[CHar\]111+\[CHar\]100+\[CHar\]32+\[CHar\]74+\[CHar\]111+\[CHar\]98+\[CHar\]33+\[CHar\]39+\[CHar\]59+\[CHar\]13+\[CHar\]10+\[CHar\]9+\[CHar\]87+\[CHar\]114+\[CHar\]105+\[CHar\]116+\[CHar\]101+\[CHar\]45+\[CHar\]72+\[CHar\]111+\[CHar\]115+\[CHar\]116+\[CHar\]32+\[CHar\]34+\[CHar\]83+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]123+\[CHar\]36+\[CHar\]69+\[CHar\]67+\[CHar\]67+\[CHar\]79+\[CHar\]78+\[CHar\]125+\[CHar\]34+\[CHar\]13+\[CHar\]10+\[CHar\]125
$ECCON=Read-Host -Prompt 'Enter the password'
If($ECCON -eq 'P0wEr$H311'){
        Write-Host 'Good Job!';
        Write-Host "SECCON{$ECCON}"
}
```

boom. That's the flag.

FLAG : `SECCON{P0wEr$H311}`