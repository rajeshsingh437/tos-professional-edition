"""
AEGIS Server
Build 0.2.002
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="AEGIS Server",
    version="0.2.002",
)


@app.get("/")
def root():
    return {
        "name": "AEGIS Server",
        "version": "0.2.002",
        "status": "running",
    }


def main():
    print("=" * 55)
    print("AEGIS Server  Build 0.2.002")
    print("=" * 55)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8091,
    )


if __name__ == "__main__":
    main()
