from flask import Flask, render_template

app = Flask(__name__)

# ChronosMatch dashboard metrics
orders_processed = 10
average_latency = 610.33
minimum_latency = 554.70
maximum_latency = 928.60


@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        orders_processed=orders_processed,
        average_latency=average_latency,
        minimum_latency=minimum_latency,
        maximum_latency=maximum_latency,
    )


if __name__ == "__main__":
    app.run(debug=True)