# Bản Windows của new-project.sh (không cần Git Bash).
# Dùng:  powershell -ExecutionPolicy Bypass -File new-project.ps1 <skill> <slug> [-Theme <tên>] [-Kit <thư-mục-herk-edit-kit>]
#        ... <skill> -Theme list     liệt kê bảng màu của skill
param(
  [Parameter(Mandatory = $true, Position = 0)][string]$Skill,
  [Parameter(Position = 1)][string]$Slug = "",
  [string]$Theme = "",
  [string]$Kit = ""
)
$ErrorActionPreference = "Stop"
$Here = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path   # skills-v2
$Repo = (Resolve-Path (Join-Path $Here "..")).Path              # vidskill
$Root = (Resolve-Path (Join-Path $Repo "..")).Path
if (-not $Kit) { $Kit = Join-Path $Root "herk-edit-kit" }
$Out = Join-Path $Root "output"
$ThemeDir = Join-Path $Here "$Skill\themes"

function Get-Themes { if (Test-Path $ThemeDir) { (Get-ChildItem $ThemeDir -Filter *.css).BaseName } else { @() } }

if ($Theme -eq "list") { Get-Themes; exit 0 }
if (-not $Slug) { throw "Thiếu slug" }
$Template = Join-Path $Here "$Skill\template\index.html"
if (-not (Test-Path $Template)) { throw "Không có template cho $Skill" }
$Dest = Join-Path $Kit "video-projects\$Slug"
if (Test-Path $Dest) { throw "$Dest đã tồn tại" }
if ($Theme) {
  $ThemeFile = Join-Path $ThemeDir "$Theme.css"
  if (-not (Test-Path $ThemeFile)) { throw "Không có màu '$Theme' cho $Skill. Có: $((Get-Themes) -join ', ')" }
}

New-Item -ItemType Directory -Force -Path (Join-Path $Dest "assets\fonts"), $Out | Out-Null
Copy-Item $Template (Join-Path $Dest "index.html")
Copy-Item (Join-Path $Here "_shared\gsap.min.js") (Join-Path $Dest "assets")
Copy-Item (Join-Path $Here "_shared\fonts\*.ttf") (Join-Path $Dest "assets\fonts")
Copy-Item (Join-Path $Here "_shared\audio\*.wav") (Join-Path $Dest "assets")
Copy-Item (Join-Path $Kit "examples\starter\meta.json") $Dest
Copy-Item (Join-Path $Kit "examples\starter\hyperframes.json") $Dest
$AssetSpec = Join-Path $Here "$Skill\template\assets.json"
if (Test-Path $AssetSpec) { Copy-Item $AssetSpec (Join-Path $Dest "assets.json") }

if ($Theme) {
  $utf8 = New-Object System.Text.UTF8Encoding($false)
  $css = [IO.File]::ReadAllText($ThemeFile, $utf8).Trim()
  $idx = Join-Path $Dest "index.html"
  $html = [IO.File]::ReadAllText($idx, $utf8)
  $html = $html.Replace("</head>", "<style id=`"theme`">$css</style></head>")
  [IO.File]::WriteAllText($idx, $html, $utf8)
  Write-Host "Đã áp dụng màu: $Theme"
}

Write-Host "Đã tạo $Dest"
Write-Host "Lint  : cd `"$Kit`"; npx hyperframes lint video-projects/$Slug"
Write-Host "Render: cd `"$Kit`"; npx hyperframes render video-projects/$Slug --output `"$Out\$Slug.mp4`""
