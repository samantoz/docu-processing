import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    print ("Hello World")
    return


if __name__ == "__main__":
    app.run()
