import asyncio
from conva_ai import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="8e482dab3bb7488397f0ff13f5002439", 
    assistant_version="13.0.0", 
    api_key="0ffa97f908fa4760bc2287d350b989db",
    host = "https://omni-inference-dev-v2.thankfulmoss-ed94449a.centralindia.azurecontainerapps.io"
)

query = "How do i sign for dpa without signing up for freshworks?"
response = asyncio.run(client.invoke_capability(query, stream=False))
print(response)