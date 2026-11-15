$pptxPath = "C:\Users\madia\Documents\antigravity\materiales\polimeros.pptx"
$exportDir = "C:\Users\madia\Documents\antigravity\materiales\preview_slides"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Force -Path $exportDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, 1, 0, 0)
for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $slideName = "slide_{0:D2}.png" -f $i
    $pres.Slides.Item($i).Export("$exportDir\$slideName", "PNG", 1920, 1080)
}
$pres.Close()
Write-Host "Exported all $($pres.Slides.Count) slides successfully!"
