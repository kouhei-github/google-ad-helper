if __name__ == '__main__':
    import uvicorn
    uvicorn.run("index:app", host='0.0.0.0', port=8000, reload=True)
