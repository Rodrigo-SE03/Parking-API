from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parking.router import router
from core.configs import ENV
import uvicorn

app = FastAPI(
  title="Parking API",
  description="API Para registro de entrada, pagamento e saída de veículos em um estacionamento.",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["Content-Type", "Authorization", "Accept"],
)

app.include_router(router)

if __name__ == "__main__":
  # Desenvolvimento local
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)