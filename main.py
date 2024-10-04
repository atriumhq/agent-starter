#!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright © 2024 Atrium [Reframe AI, Inc.]"

# Standard Libraries
import asyncio
import json
from pprint import pformat

# External Libraries
import boto3
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.exceptions import HTTPException

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
app = FastAPI()

async def example_llm_gen(data):
    model_id = "mistral.mistral-large-2402-v1:0"

    assert 'messages' in data
    if 'system' not in data: data['system'] = []

    mistral_params = {"messages": data['messages'], "modelId": model_id, "system": data['system'] }

    try:
        response = bedrock_client.converse_stream(**mistral_params)
        stream = response.get('stream')
        if stream:
            for idx, event in enumerate(stream):
                await asyncio.sleep(0.000001)
                # Return data in the style of bedrock converse stream.
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse_stream.html
                event['format'] = 'aws-bedrock-converse_stream'

                if 'messageStart' in event:
                    print(f"\nRole: {event['messageStart']['role']}")

                if 'contentBlockDelta' in event:
                    print(event['contentBlockDelta']['delta']['text'], end="")

                if 'messageStop' in event:
                    print(f"\nStop reason: {event['messageStop']['stopReason']}")

                if 'metadata' in event:
                    metadata = event['metadata']
                    if 'usage' in metadata:
                        print("\nToken usage ... ")
                        print(f"Input tokens: {metadata['usage']['inputTokens']}")
                        print(
                            f":Output tokens: {metadata['usage']['outputTokens']}")
                        print(f":Total tokens: {metadata['usage']['totalTokens']}")
                    if 'metrics' in event['metadata']:
                        print(f"Latency: {metadata['metrics']['latencyMs']} milliseconds")

                yield json.dumps(event) + "\n"  # Yield streamed data. Note that the new line is absolutely necessary
                                                # as we set media_type="application/x-ndjson" in the expected stream
                                                # response
    except Exception as e:
        msg = f"\nError: {str(e)[:200]}"
        print(msg)
        yield json.dumps({
            "messageStop": {"stopReason": "error running agent"},
            "contentBlockDelta": {"delta": {"text": msg}}
        }) + "\n"
        raise HTTPException(status_code=500, detail=msg) from None

async def illustration_gen(data):
    print(f"Received input message {pformat(data)}")
    try:
        events = [
            {"messageStart": {"role": "system", "type": 'RT_BLOCK'}},
            {"contentBlockDelta": {"delta": {'block': {
                "children": [
                    {
                        "id": "12",
                        "type": "h1",
                        "children": [{ "text": "🌱 Hello world 👋!" }]
                    },
                    {
                        "id": "jihnx",
                        "type": "p",
                        "children": [
                            {
                            "text": "This is my very first message to the universe via Atrium's Agent platform."
                            }
                        ]
                        },
                    {
                    "id": "14",
                    "type": "p",
                    "children": [
                        { "text": "You can output rich text. Make text " },
                        { "bold": True, "text": "bold" },
                        { "text": ", " },
                        { "text": "italic", "italic": True },
                        { "text": ", " },
                        { "text": "underlined", "underline": True },
                        { "text": ", or apply a " },
                        {
                        "bold": True,
                        "text": "combination",
                        "italic": True,
                        "underline": True
                        },
                        { "text": " of these styles for a visually striking effect." }
                    ]
                    },
                    {
                    "id": "ng1xl",
                    "type": "p",
                    "children": [
                        { "text": "Learn more on how to format your message using the" },
                        {
                        "id": "ppvtq",
                        "url": "https://atrium.st/editor/playground/",
                        "type": "a",
                        "children": [{ "text": "Rich Text" }]
                        },
                        { "text": " editor." }
                    ]
                    }
                ]
                }
                }}
            },
            {"messageStop": {"stopReason": "stop"}},
            {"metadata": {
                "usage": {"inputTokens": 300, "outputTokens": 1500, "totalTokens": 1800},
                "metrics": {"latencyMs": 300}},
                "atrium": {
                    "billing": {
                        "credits_consumed": 20
                        }
                }
            }
        ]

        for event in events:
            yield json.dumps(event) + "\n"  # Yield streamed data. Note that the new line is absolutely necessary
                                        # as we set media_type="application/x-ndjson" in the expected stream
                                        # response
    except Exception as e:
        msg = f"\nError: {str(e)[:200]}"
        print(msg)
        yield json.dumps({
            "messageStop": {"stopReason": "error running agent"},
            "contentBlockDelta": {"delta": {"text": msg}}
        }) + "\n"
        raise HTTPException(status_code=500, detail=msg) from None

@app.post("/on_preprocess")
async def on_preprocess(request: Request):
    data = await request.json()
    return StreamingResponse(example_llm_gen(data), media_type="application/x-ndjson")

@app.post("/on_prompt")
async def on_prompt(request: Request):
    data = await request.json()

    # return StreamingResponse(example_llm_gen(data), media_type="application/x-ndjson")
    return StreamingResponse(illustration_gen(data), media_type="application/x-ndjson")


@app.post("/on_postprocess")
async def on_postprocess(request: Request):
    data = await request.json()
    return StreamingResponse(example_llm_gen(data), media_type="application/x-ndjson")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
