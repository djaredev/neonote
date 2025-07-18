#!/usr/bin/env bash

cd backend

source .venv/bin/activate

source .env

python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../sdk/openapi.json

deactivate

cd ../sdk/typescript-sdk

npm run openapi-ts && npm run build
