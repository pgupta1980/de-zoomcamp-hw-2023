from prefect.filesystems import GitHub

block = GitHub(
    repository="https://github.com/pgupta1980/de-zoomcamp-hw-2023.git"
)
block.save("de-zoomcamp-github", overwrite=True)