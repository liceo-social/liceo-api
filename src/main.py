import uvicorn


def main():
    uvicorn.run("liceo.infra.api:init", host="0.0.0.0", port=8000, reload=True)


def main_docker():
    from liceo.infra.api import init

    return init()


if __name__ == "__main__":
    main()
