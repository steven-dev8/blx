from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infra.sqlalchemy.config.database import create_session_db
from src.routers.product_router import router as product_router
from src.routers.user_router import router as user_router
from src.routers.order_router import router as order_router
from src.routers.auth_router import router as auth_router


create_session_db()

app = FastAPI(
    title="BLX MARKETPLACE",
    description="RESTful API for marketplace management.",
    version="1.0 BETA"
)

origins = ["http://localhost",
           "http://localhost:8080",
           "http://localhost:8000"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(product_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(auth_router, prefix="/auth")