import io
import csv
import codecs
import logging
import time

from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename

from group import group_addresses, groups_to_names


ALLOWED_FILE_EXT = "csv"
RESULT_FILE = "result.txt"
HEADERS = "Name,Address"
HOMEPAGE = "index.html"

app = Flask(__name__, template_folder="templates")
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
app.logger.addHandler(handler)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", message=e), 500


@app.route("/", methods=["GET", "POST"])
def index():
    ct = time.time()
    errors = []
    output = None
    if request.method == "POST":
        try:
            if request.files.get("file") and request.form.get("text"):
                errors.append("WARNING: Please upload or file or text not both")
                return render_template(HOMEPAGE, errors=errors)
            elif request.files.get("file") and request.files["file"].filename:
                file = request.files["file"]
                filename = secure_filename(file.filename)
                if not filename.endswith(ALLOWED_FILE_EXT):
                    errors.append("WARNING: Incorrect file type. We only work with csv files")
                    return render_template(HOMEPAGE, errors=errors)
                stream = codecs.iterdecode(file.stream, "utf-8-sig")
            elif request.form.get("text"):
                raw_text = request.form["text"]
                if not raw_text.startswith(HEADERS):
                    errors.append("WARNING: Please prepare correct data")
                    return render_template(HOMEPAGE, errors=errors)
                stream = io.StringIO(raw_text)
            else:
                errors.append("WARNING: Please provide file or text to upload")
                return render_template(HOMEPAGE, errors=errors)
        except Exception as exc:
            abort(500, description=exc)

        try:
            csv_dict, data, addresses = csv.DictReader(stream), [], []
            for row in csv_dict:
                if row["Name"] and row["Address"]:
                    data.append((row["Name"], row["Address"]))
                    addresses.append(row["Address"])

            if not data:
                errors.append("WARNING: No data rows. Please prepare correct data")
                return render_template(HOMEPAGE, errors=errors)

            app.logger.info("Grouping addresses by matches")
            grouped_addresses = group_addresses(addresses)

            app.logger.info("Mapping grouped addresses to names")
            address_groups_to_names = groups_to_names(data, grouped_addresses)

            app.logger.info("Sorting names of a group alphabetically")
            [n.sort() for _, n in address_groups_to_names.items()]

            app.logger.info("Sorting groups alphabetically")
            output = sorted(address_groups_to_names.values())
        except Exception as exc:
            abort(500, description=exc)

    app.logger.info(f"Processing took us: {time.time() - ct:.2f} sec")
    return render_template(HOMEPAGE, errors=errors, output=output, data=output)


@app.route("/download")
def download():
    try:
        app.logger.info("Downloading results as a txt file")
        output = request.args.get("output")
        output_file = io.BytesIO(output.encode())
        return send_file(output_file, download_name=RESULT_FILE, as_attachment=True)
    except Exception as exc:
        abort(500, description=exc)


# Run the app in development mode
if __name__ == "__main__":
    app.run(debug=True)
