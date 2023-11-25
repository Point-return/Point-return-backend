import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title='ProSept',
)


@app.get('/')
def index():
    return 'Hello'


def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
