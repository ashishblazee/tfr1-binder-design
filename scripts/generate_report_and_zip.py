"""
Generate Academic HTML and PDF Methods Report, and create complete submission ZIP
"""
import os
import shutil
import zipfile
import subprocess

def convert_md_to_html(md_text):
    # Minimal clean markdown to html converter
    import html
    lines = md_text.splitlines()
    html_out = []
    in_table = False
    in_list = False
    
    html_out.append('''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TfR1 Binder Design Methods Report</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
  }
  h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; font-size: 26px; }
  h2 { color: #1e293b; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-top: 30px; font-size: 20px; }
  h3 { color: #334155; margin-top: 20px; font-size: 16px; }
  p, li { font-size: 14px; }
  code { background-color: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 13px; }
  table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }
  th, td { border: 1px solid #cbd5e1; padding: 8px 10px; text-align: left; }
  th { background-color: #f8fafc; font-weight: 600; }
  tr:nth-child(even) { background-color: #f8fafc; }
  hr { border: none; border-top: 1px solid #e2e8f0; margin: 25px 0; }
  ul { padding-left: 20px; }
  @page { margin: 20mm 15mm; size: A4; }
</style>
</head>
<body>''')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_out.append("</ul>")
                in_list = False
            if in_table:
                html_out.append("</table>")
                in_table = False
            continue
            
        if stripped.startswith("# "):
            html_out.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            html_out.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            html_out.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("---"):
            html_out.append("<hr>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_out.append("<ul>")
                in_list = True
            html_out.append(f"<li>{html.escape(stripped[2:])}</li>")
        elif stripped.startswith("|"):
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if all(set(p) <= set("- :") for p in parts if p):
                continue # header separator
            if not in_table:
                html_out.append("<table>")
                html_out.append("<tr>" + "".join(f"<th>{html.escape(p)}</th>" for p in parts) + "</tr>")
                in_table = True
            else:
                html_out.append("<tr>" + "".join(f"<td>{html.escape(p)}</td>" for p in parts) + "</tr>")
        else:
            if in_list:
                html_out.append("</ul>")
                in_list = False
            if in_table:
                html_out.append("</table>")
                in_table = False
            html_out.append(f"<p>{html.escape(line)}</p>")
            
    if in_list: html_out.append("</ul>")
    if in_table: html_out.append("</table>")
    html_out.append("</body></html>")
    return "\n".join(html_out)

def main():
    proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_md_path = os.path.join(proj_dir, "METHODS_REPORT.md")
    with open(report_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    html_text = convert_md_to_html(md_text)
    html_path = os.path.join(proj_dir, "TfR1_Binder_Design_Methods_Report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    print(f"[PASS] HTML Report generated: {html_path}")
    
    # Generate PDF using Edge headless
    pdf_path = os.path.join(proj_dir, "TfR1_Binder_Design_Methods_Report.pdf")
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_exe):
        cmd = [
            edge_exe,
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        try:
            subprocess.run(cmd, check=True, timeout=15)
            print(f"[PASS] PDF Report generated: {pdf_path}")
        except Exception as e:
            print(f"[NOTE] Edge PDF print note: {e}")
            
    # Build complete submission zip
    zip_path = os.path.join(proj_dir, "TfR1_Binder_Design_Submission_Package.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists(pdf_path):
            zipf.write(pdf_path, arcname="TfR1_Binder_Design_Methods_Report.pdf")
        zipf.write(report_md_path, arcname="METHODS_REPORT.md")
        csv_path = os.path.join(proj_dir, "data", "proteinbase_submission_tfr1.csv")
        if os.path.exists(csv_path):
            zipf.write(csv_path, arcname="proteinbase_submission_tfr1.csv")
        
        # Add structures
        struct_dir = os.path.join(proj_dir, "structures")
        for root, dirs, files in os.walk(struct_dir):
            for file in files:
                fpath = os.path.join(root, file)
                arcname = os.path.relpath(fpath, proj_dir)
                zipf.write(fpath, arcname=arcname)
                
    print(f"[PASS] Submission ZIP archive generated: {zip_path}")
    
    # Copy to Downloads for easy selection
    downloads_dir = os.path.expanduser(r"~\Downloads")
    if os.path.exists(downloads_dir):
        if os.path.exists(pdf_path):
            shutil.copyfile(pdf_path, os.path.join(downloads_dir, "TfR1_Binder_Design_Methods_Report.pdf"))
            print(f"[EXPORT] PDF in Downloads: {os.path.join(downloads_dir, 'TfR1_Binder_Design_Methods_Report.pdf')}")
        shutil.copyfile(zip_path, os.path.join(downloads_dir, "TfR1_Binder_Design_Submission_Package.zip"))
        print(f"[EXPORT] ZIP in Downloads: {os.path.join(downloads_dir, 'TfR1_Binder_Design_Submission_Package.zip')}")

if __name__ == "__main__":
    main()
