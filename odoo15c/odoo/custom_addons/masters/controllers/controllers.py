# -*- coding: utf-8 -*-
# from odoo import http


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}