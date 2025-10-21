import os
import datetime

def generate_html_report(screenshots_dir, reports_dir):
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    today = datetime.date.today().strftime("%Y-%m-%d")
    report_filename = os.path.join(reports_dir, f"report_{today}.html")

    with open(report_filename, "w") as f:
        f.write("<html><head><title>Screenshot Report</title></head><body>")
        f.write(f"<h1>Screenshot Report - {today}</h1>")

        for root, _, files in os.walk(screenshots_dir):
            if not files:
                continue

            # Extract the scenario name from the directory path
            scenario_name = os.path.basename(root)
            f.write(f"<h2>{scenario_name}</h2>")

            for file in sorted(files):
                if file.endswith(".png"):
                    screenshot_path = os.path.join(root, file)
                    # Use relative path for the image source in the HTML report
                    relative_screenshot_path = os.path.relpath(screenshot_path, reports_dir)
                    f.write(f'<img src="{relative_screenshot_path}" width="500"><br>')

        f.write("</body></html>")

    print(f"Report generated: {report_filename}")