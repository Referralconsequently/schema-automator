from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from subprocess import run
import tempfile
import shutil
import os

app = FastAPI()

@app.post("/infer", response_class=PlainTextResponse)
async def infer_schema(
    file: UploadFile = File(...),
    input_type: str = "json",
    output_format: str = "linkml"
):
    if not file.filename.endswith((".json", ".jsonl", ".csv", ".md", ".yaml", ".yml", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, file.filename)
        output_path = os.path.join(tmpdir, "inferred_schema.yaml")

        # Save uploaded file
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Run schema-automator
        cmd = [
            "schema-automator",
            "--input", input_type,
            input_path,
            "--output", output_format,
            output_path
        ]
        result = run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # Read and return output
        with open(output_path, "r") as f:
            schema = f.read()

        return schema