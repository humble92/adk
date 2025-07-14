# Exploring Google ADK

## Quick commands

```
pip install google-adk
adk web     # OR adk api_server
```

## References

- https://google.github.io/adk-docs/get-started/quickstart/
- https://google.github.io/adk-docs/get-started/about/

## ADKs
- Python: https://github.com/google/adk-python
- Java: https://github.com/google/adk-java

## Further steps

- https://github.com/comet-ml/opik?tab=readme-ov-file (Comet Opik: Integrating open-source LLM observability)
- Audio/Video Streaming (https://google.github.io/adk-docs/get-started/streaming/)
- Leveraging Callbacks (https://google.github.io/adk-docs/callbacks/)
- A2A (https://github.com/a2aproject/A2A)
- A2A examples (https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents)

## Tips on Windows

### adk api_server
```
Invoke-WebRequest -Uri http://localhost:8000/apps/multi_tool_agent/users/u_123/sessions/s_123 `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"state": {"key1": "value1", "key2": 42}}'

Invoke-WebRequest -Uri http://localhost:8000/run `
	-Method POST -ContentType "application/json" `
	-Body '{"appName": "multi_tool_agent", "userId": "u_123", "sessionId": "s_123", "newMessage": {"role": "user", "parts": [{"text": "Hey whats the weather in new york today"}]}}'
```

**Or using JSON body formatted with SSE endpoints:**
1. This approach avoids escaping issues and is easy to maintain.

```
$body = @{
    appName   = "multi_tool_agent"
    userId    = "u_123"
    sessionId = "s_123"
    newMessage = @{
        role  = "user"
        parts = @(@{ text = "Hey whats the weather in new york today" })
    }
    streaming = $false
} | ConvertTo-Json -Depth 5

Invoke-WebRequest -Uri http://localhost:8000/run_sse `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```