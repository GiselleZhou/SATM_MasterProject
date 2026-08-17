param(
    [Parameter(Mandatory = $true)]
    [string]$Text,

    [Parameter(Mandatory = $true)]
    [string]$SceneImage,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [double]$MotionLength = 3.0,
    [int]$Device = 0
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$scene = (Resolve-Path $SceneImage).Path
$output = [System.IO.Path]::GetFullPath($OutputDir)
$model = Join-Path $root 'save\text_image_mdm\model000050000.pt'

if (-not (Test-Path -LiteralPath $model)) {
    throw "Missing checkpoint: $model. See docs/ASSETS.md."
}
if (Test-Path -LiteralPath $output) {
    throw "Output directory already exists: $output. Choose a new directory."
}

Push-Location $root
try {
    & python -m sample.generate `
        --model_path 'save/text_image_mdm/model000050000.pt' `
        --text_prompt $Text `
        --scene_image $scene `
        --output_dir $output `
        --motion_length $MotionLength `
        --num_repetitions 1 `
        --guidance_param 2.5 `
        --device $Device

    if ($LASTEXITCODE -ne 0) {
        throw "Generation failed with exit code $LASTEXITCODE."
    }

    $extension = [System.IO.Path]::GetExtension($scene)
    Copy-Item -LiteralPath $scene -Destination (Join-Path $output "scene_image$extension")
    Get-ChildItem -LiteralPath $output -Filter '*.mp4' -File |
        Where-Object { $_.Name -ne 'sample00_rep00.mp4' } |
        Remove-Item -Force
}
finally {
    Pop-Location
}

Write-Host "Done: $output\sample00_rep00.mp4"
