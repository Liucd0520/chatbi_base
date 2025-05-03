from fastapi import FastAPI
from apps.app_excel2db import router as excel2db_router
from apps.app_init import router as init_router
from apps.app_text2sql import router as text2sql_router

import uvicorn


app = FastAPI()

# Include the routers with their respective prefixes
app.include_router(excel2db_router, prefix="/excel2db", tags=["ChatBI-Dev"])
app.include_router(init_router, prefix="/initial", tags=["ChatBI-Dev"])
app.include_router(text2sql_router, prefix="/obtain_data", tags=["ChatBI-Dev"])

if __name__ == '__main__':

    uvicorn.run(app=app, host='0.0.0.0', port=8077)

