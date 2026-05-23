import uvicorn
from fastapi import FastAPI
from routes.risk_route import router as risk_router
from routes.cnpj_route import router as get_cnpj_summary

app = FastAPI()

app.include_router(risk_router)

# Route to get the CNPJ information
app.include_router(get_cnpj_summary)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)