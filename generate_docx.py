import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_docx(filename="Adaptive_Lightweight_NIDS_Presentation_Guide.docx"):
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Title
    title = doc.add_paragraph()
    title_run = title.add_run("Adaptive Lightweight Network Intrusion Detection System (NIDS)")
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42) # Slate Navy

    sub = doc.add_paragraph()
    sub_run = sub.add_run("Comprehensive Project Defense, Architecture & Technical Presentation Guide")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(11)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(2, 132, 199) # Cyber Blue

    doc.add_paragraph("─" * 70)

    # 1. Executive Summary
    h1 = doc.add_heading("1. Executive Summary & Problem Motivation", level=1)
    doc.add_paragraph(
        "Modern enterprise networks, IoT perimeters, and cloud firewalls process thousands of network packets per second. "
        "Traditional Network Intrusion Detection Systems (NIDS) suffer from a critical performance-accuracy dilemma: "
        "Deep Learning architectures (LSTMs, CNNs, Transformers) offer high representation capacity but require excessive memory and "
        "introduce 10–50+ ms inference latencies per packet, rendering them unfeasible for real-time edge hardware. "
        "Conversely, single standalone ML models struggle with noise and fail to generalize against novel attack vectors."
    )
    doc.add_paragraph(
        "The Adaptive Lightweight Solution: This project bridges this critical gap by delivering high detection accuracy with "
        "sub-1.5ms inference latency through a unified system combining intelligent dimension reduction, heterogeneous tree ensembles, "
        "adaptive dynamic weighting based on information entropy, zero-day anomaly scoring, and production cloud microservices."
    )

    # Callout
    p_box = doc.add_paragraph()
    r_box = p_box.add_run("Key Takeaway: Dimension reduction from 49 to 15 features reduces latency by ~4x (4.85ms → 1.25ms) and memory by 64%, while our Adaptive Dynamic Weighting outperforms static soft voting by +1.7% in F1-score.")
    r_box.font.bold = True
    r_box.font.color.rgb = RGBColor(12, 74, 110)

    # 2. System Architecture
    doc.add_heading("2. End-to-End System Architecture (Stages A to F)", level=1)
    stages = [
        ("Stage A: Data Ingestion & Extraction", "Ingests raw packet flows or standard benchmark datasets (UNSW-NB15 / CICIDS2017), capturing 49 high-dimensional flow statistics (flow duration, inter-arrival times, packet rates, TCP state flags, byte volume, TTL, jitter)."),
        ("Stage B: Data Preprocessing Pipeline", "Sanitizes flow records via clean.py by imputing missing values and replacing infinities (+/-inf) with training medians. encoder.py transforms categorical attributes (proto, service, state) with fallback for unseen tokens, followed by StandardScaler normalization."),
        ("Stage C: Intelligent Dimension Reduction (Top 15 Features)", "Applies a hybrid scoring algorithm combining Mutual Information (non-linear dependency) and Random Forest Gini Feature Importance (tree split gain). Prunes the feature space from 49 to 15 features, eliminating redundancy and reducing memory footprint."),
        ("Stage D: Heterogeneous Tree Ensemble", "Passes the 15-feature vector through three complementary base classifiers in parallel: Random Forest (bagging variance reducer), XGBoost (gradient boosting boundary discriminator), and CatBoost (categorical variance optimizer)."),
        ("Stage E: Adaptive Dynamic Weighting", "Instead of static 33% weights, dynamically calculates confidence margins (P_top1 - P_top2) and Shannon Entropy (uncertainty) per packet. Dynamically assigns higher voting influence to the model displaying maximum certainty on that specific flow."),
        ("Stage F: Zero-Day Anomaly Detection & Telemetry", "Monitors prediction distribution entropy. Flows exhibiting high entropy (H > 1.1) or low confidence (< 0.60) are intercepted and categorized as UNKNOWN / ANOMALOUS. Results are broadcast via WebSockets to a React SOC dashboard in real time.")
    ]
    for st_title, st_desc in stages:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(f"{st_title}: ")
        r1.bold = True
        p.add_run(st_desc)

    # 3. Mathematical Formulations
    doc.add_heading("3. Mathematical & Algorithmic Formulations", level=1)
    doc.add_heading("Hybrid Feature Selection Score:", level=2)
    doc.add_paragraph("Score(f) = 0.5 * Normalized_Mutual_Information(f) + 0.5 * Normalized_RF_Gini_Importance(f)")
    doc.add_paragraph("Balances non-linear probabilistic dependency with empirical decision-tree split gain.")

    doc.add_heading("Sample-Wise Dynamic Weighting Formulation:", level=2)
    doc.add_paragraph("Margin_m = P_m(class_1) - P_m(class_2)")
    doc.add_paragraph("Shannon Entropy H_m = - Σ p_i * ln(p_i)")
    doc.add_paragraph("Confidence S_m = BaseWeight_m * (Margin_m + 0.1) / (1.0 + H_m)")
    doc.add_paragraph("Final Dynamic Weight: Weight_m = S_m / Σ S_j")

    # 4. Experimental Benchmarks Table
    doc.add_heading("4. Experimental Benchmarks & Ablation Study", level=1)
    table_data = [
        ["Model Configuration", "Features", "Accuracy", "F1-Score", "Latency (ms)", "RAM Footprint"],
        ["Adaptive Ensemble (Ours)", "15", "98.4%", "0.982", "1.25 ms", "~245 MB"],
        ["Static Voting Ensemble", "15", "96.8%", "0.965", "1.28 ms", "~245 MB"],
        ["Random Forest Only", "15", "95.9%", "0.957", "0.95 ms", "~180 MB"],
        ["XGBoost Only", "15", "96.1%", "0.959", "0.88 ms", "~140 MB"],
        ["CatBoost Only", "15", "96.4%", "0.962", "1.10 ms", "~160 MB"],
        ["Full Model (No Selection)", "49", "98.6%", "0.983", "4.85 ms", "~680 MB"]
    ]
    table = doc.add_table(rows=len(table_data), cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for row_idx, row in enumerate(table_data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = val
            if row_idx == 0:
                set_cell_background(cell, "0F172A")
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
            elif row_idx == 1:
                set_cell_background(cell, "E0F2FE")
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.bold = True
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    # 5. Deployment Links
    doc.add_heading("5. Live Cloud Deployment & Links", level=1)
    links = [
        ("Frontend SOC Dashboard (Vercel Global Edge)", "https://nids-project-neon.vercel.app"),
        ("Backend API & Interactive Swagger (Render Cloud)", "https://nids-project-bbsy.onrender.com/docs"),
        ("Public GitHub Repository", "https://github.com/satwikpkp/nids-project"),
        ("Default Operator Credentials", "admin@soc.defense / Admin@123456")
    ]
    for title_l, link_l in links:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(f"{title_l}: ")
        r.bold = True
        p.add_run(link_l)

    # 6. Oral Exam Defending Points
    doc.add_heading("6. Key Defending Points for Oral Examination", level=1)
    points = [
        ("Why tree-based ensembles instead of Deep Learning (LSTM/CNN)?", "Tabular network traffic does not have continuous spatial or temporal dependencies like images or audio. GBDTs and Random Forest consistently outperform deep neural nets on tabular benchmarks while executing in <1.5ms with sub-250MB RAM."),
        ("How does the system handle zero-day attacks?", "Through our out-of-distribution entropy scoring hook. Novel attacks produce high prediction entropy and low margin confidence, triggering an immediate UNKNOWN / ANOMALOUS alert."),
        ("What is the computational benefit of feature reduction?", "Memory footprint is reduced by 64% and latency decreases from 4.85 ms to 1.25 ms per packet (a nearly 4x speedup) with less than 0.2% change in F1-score.")
    ]
    for q, a in points:
        p = doc.add_paragraph()
        r_q = p.add_run(f"Q: {q}\n")
        r_q.bold = True
        p.add_run(a)

    doc.save(filename)
    print(f"Successfully generated DOCX: {filename}")

if __name__ == "__main__":
    create_docx()
