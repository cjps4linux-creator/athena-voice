# Realtime/local voice server launcher — local-first mode
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $env:LOCALAPPDATA 'hermes\hermes-agent\venv\Scripts\speech-to-speech.exe'
if (-not (Test-Path $venv)) { throw "speech-to-speech.exe not found at $venv" }
& $venv `
  --mode local `
  --thresh 0.6 `
  --stt parakeet-tdt `
  --llm_backend responses-api `
  --tts pocket `
  --model_name LiquidAI/LFM2.5-Audio-1.5B-GGUF:F16 `
  --chat_size 30 `
  --responses_api_stream `
  --enable_live_transcription `
  --responses_api_base_url http://127.0.0.1:8080/v1 `
  --responses_api_api_key local
