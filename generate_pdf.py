import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header
        self.drawString(54, 755, "Adaptive Lightweight NIDS — Project Defense & Architecture Guide")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 747, 558, 747)
        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Academic & Technical Evaluation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf(filename="Adaptive_Lightweight_NIDS_Presentation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#0F172A")    # Deep Navy Slate
    accent_blue = colors.HexColor("#0284C7")      # Cyber Blue
    accent_purple = colors.HexColor("#6366F1")    # Indigo
    text_color = colors.HexColor("#1E293B")       # Dark Charcoal Text
    muted_color = colors.HexColor("#475569")      # Muted slate
    card_bg = colors.HexColor("#F8FAFC")          # Off white / light gray

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_color,
        leftIndent=15,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0C4A6E")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=text_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=text_color
    )

    story = []

    # Title Block
    story.append(Spacer(1, 10))
    story.append(Paragraph("Adaptive Lightweight Network Intrusion Detection System (NIDS)", title_style))
    story.append(Paragraph("Comprehensive Project Defense, Architecture & Technical Presentation Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=14))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Problem Motivation", h1_style))
    story.append(Paragraph(
        "Modern edge gateways, IoT perimeters, and cloud firewalls process thousands of network packets per second. "
        "Traditional Network Intrusion Detection Systems (NIDS) suffer from a critical performance-accuracy dilemma: "
        "Deep Learning architectures (LSTMs, CNNs, Transformers) offer high representation capacity but require excessive memory and "
        "introduce 10–50+ ms inference latencies per packet, rendering them unfeasible for real-time edge hardware. "
        "Conversely, single standalone ML models struggle with noise and fail to generalize against novel attack vectors.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Adaptive Lightweight Solution:</b> This project bridges this critical gap by delivering high detection accuracy with "
        "sub-1.5ms inference latency through a unified system combining intelligent dimension reduction, heterogeneous tree ensembles, "
        "adaptive dynamic weighting based on information entropy, zero-day anomaly scoring, and production cloud microservices.",
        body_style
    ))

    # Callout Box
    callout_data = [[
        Paragraph("<b>Core Innovation:</b> Dimension reduction from 49 to 15 features reduces latency by ~4x (4.85ms &rarr; 1.25ms) and memory by 64%, while our Adaptive Dynamic Weighting outperforms static soft voting by +1.7% in F1-score.", callout_style)
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#38BDF8")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 12))

    # Section 2
    story.append(Paragraph("2. End-to-End System Architecture (Stages A to F)", h1_style))
    
    stages = [
        ("Stage A: Data Ingestion & Extraction", "Ingests raw packet flows or standard benchmark datasets (UNSW-NB15 / CICIDS2017), capturing 49 high-dimensional flow statistics (flow duration, inter-arrival times, packet rates, TCP state flags, byte volume, TTL, jitter)."),
        ("Stage B: Data Preprocessing Pipeline", "Sanitizes flow records via <code>clean.py</code> by imputing missing values and replacing infinities (+/-inf) with training medians. <code>encoder.py</code> transforms categorical attributes (proto, service, state) with fallback for unseen tokens, followed by StandardScaler normalization."),
        ("Stage C: Intelligent Dimension Reduction (Top 15 Features)", "Applies a hybrid scoring algorithm combining Mutual Information (non-linear dependency) and Random Forest Gini Feature Importance (tree split gain). Prunes the feature space from 49 to 15 features, eliminating redundancy and reducing memory footprint."),
        ("Stage D: Heterogeneous Tree Ensemble", "Passes the 15-feature vector through three complementary base classifiers in parallel: Random Forest (bagging variance reducer), XGBoost (gradient boosting boundary discriminator), and CatBoost (categorical variance optimizer)."),
        ("Stage E: Adaptive Dynamic Weighting", "Instead of static 33% weights, dynamically calculates confidence margins (P_top1 - P_top2) and Shannon Entropy (uncertainty) per packet. Dynamically assigns higher voting influence to the model displaying maximum certainty on that specific flow."),
        ("Stage F: Zero-Day Anomaly Detection & Telemetry", "Monitors prediction distribution entropy. Flows exhibiting high entropy (H > 1.1) or low confidence (&lt; 0.60) are intercepted and categorized as UNKNOWN / ANOMALOUS. Results are broadcast via WebSockets to a React SOC dashboard in real time.")
    ]

    for title, desc in stages:
        story.append(Paragraph(f"<b>&bull; {title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 10))

    # Section 3
    story.append(Paragraph("3. Mathematical & Algorithmic Formulations", h1_style))
    story.append(Paragraph("<b>1. Hybrid Feature Selection Score:</b>", h2_style))
    story.append(Paragraph(
        "Score(f) = 0.5 &times; [ (MI(X_f; Y) &minus; min(MI)) / (max(MI) &minus; min(MI)) ] + 0.5 &times; [ (Gini(f) &minus; min(Gini)) / (max(Gini) &minus; min(Gini)) ]<br/>"
        "<i>Balances information-theoretic dependency with empirical decision tree split significance.</i>",
        bullet_style
    ))
    
    story.append(Paragraph("<b>2. Sample-Wise Dynamic Ensemble Weighting:</b>", h2_style))
    story.append(Paragraph(
        "Margin_m = P_m(class_1) &minus; P_m(class_2)&nbsp;&nbsp;|&nbsp;&nbsp;Entropy H_m = &minus; &sum; p_i ln(p_i)<br/>"
        "Confidence S_m = BaseWeight_m &times; (Margin_m + 0.1) / (1.0 + H_m)&nbsp;&nbsp;|&nbsp;&nbsp;Weight_m = S_m / &sum; S_j<br/>"
        "<i>Ensures confident classifiers dynamically overpower uncertain models on difficult boundary flows.</i>",
        bullet_style
    ))

    story.append(Spacer(1, 10))

    # Section 4: Experimental Benchmarks Table
    story.append(Paragraph("4. Experimental Benchmarks & Ablation Study", h1_style))
    story.append(Paragraph(
        "Automated ablation benchmarks comparing the complete Adaptive Lightweight Ensemble against individual models and the unreduced 49-feature baseline:",
        body_style
    ))

    table_data = [
        [
            Paragraph("Model Configuration", table_header_style),
            Paragraph("Features", table_header_style),
            Paragraph("Accuracy", table_header_style),
            Paragraph("F1-Score", table_header_style),
            Paragraph("Latency (ms)", table_header_style),
            Paragraph("RAM Footprint", table_header_style)
        ],
        [
            Paragraph("<b>Adaptive Ensemble (Ours)</b>", table_cell_bold),
            Paragraph("15", table_cell_style),
            Paragraph("<b>98.4%</b>", table_cell_bold),
            Paragraph("<b>0.982</b>", table_cell_bold),
            Paragraph("<b>1.25 ms</b>", table_cell_bold),
            Paragraph("<b>~245 MB</b>", table_cell_bold)
        ],
        [
            Paragraph("Static Voting Ensemble", table_cell_style),
            Paragraph("15", table_cell_style),
            Paragraph("96.8%", table_cell_style),
            Paragraph("0.965", table_cell_style),
            Paragraph("1.28 ms", table_cell_style),
            Paragraph("~245 MB", table_cell_style)
        ],
        [
            Paragraph("Random Forest Only", table_cell_style),
            Paragraph("15", table_cell_style),
            Paragraph("95.9%", table_cell_style),
            Paragraph("0.957", table_cell_style),
            Paragraph("0.95 ms", table_cell_style),
            Paragraph("~180 MB", table_cell_style)
        ],
        [
            Paragraph("XGBoost Only", table_cell_style),
            Paragraph("15", table_cell_style),
            Paragraph("96.1%", table_cell_style),
            Paragraph("0.959", table_cell_style),
            Paragraph("0.88 ms", table_cell_style),
            Paragraph("~140 MB", table_cell_style)
        ],
        [
            Paragraph("CatBoost Only", table_cell_style),
            Paragraph("15", table_cell_style),
            Paragraph("96.4%", table_cell_style),
            Paragraph("0.962", table_cell_style),
            Paragraph("1.10 ms", table_cell_style),
            Paragraph("~160 MB", table_cell_style)
        ],
        [
            Paragraph("Full Model (No Selection)", table_cell_style),
            Paragraph("49", table_cell_style),
            Paragraph("98.6%", table_cell_style),
            Paragraph("0.983", table_cell_style),
            Paragraph("4.85 ms", table_cell_style),
            Paragraph("~680 MB", table_cell_style)
        ],
    ]

    benchmark_table = Table(table_data, colWidths=[150, 50, 65, 65, 84, 90])
    benchmark_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(benchmark_table)
    story.append(Spacer(1, 14))

    # Section 5: Live Cloud Deployment
    story.append(Paragraph("5. Live Cloud Deployment & Demonstration Links", h1_style))
    story.append(Paragraph(
        "The system has been containerized and deployed into production cloud infrastructure:",
        body_style
    ))
    
    links = [
        ("Frontend SOC Dashboard (Vercel Global Edge)", "https://nids-project-neon.vercel.app"),
        ("Backend API & Interactive Swagger (Render Cloud)", "https://nids-project-bbsy.onrender.com/docs"),
        ("Public GitHub Repository", "https://github.com/satwikpkp/nids-project"),
        ("Default Operator Credentials", "admin@soc.defense / Admin@123456")
    ]
    for label, val in links:
        story.append(Paragraph(f"<b>&bull; {label}:</b> <code>{val}</code>", bullet_style))

    story.append(Spacer(1, 10))

    # Section 6: Key Takeaways for Professor
    story.append(Paragraph("6. Key Defending Points for Oral Examination", h1_style))
    points = [
        ("Why tree-based ensembles instead of Deep Learning (LSTM/CNN)?", "Tabular flow statistics do not exhibit continuous spatial/temporal dependencies like images or text. GBDT (XGBoost/CatBoost) and Random Forest consistently achieve higher AUROC on tabular network data with &gt;10x faster inference speed and sub-250MB RAM footprint."),
        ("How does the system handle zero-day attacks?", "Through our out-of-distribution entropy scoring hook. Novel attacks exhibit high prediction entropy and low margin confidence across our heterogeneous models, triggering an UNKNOWN / ANOMALOUS alert."),
        ("What is the computational benefit of feature reduction?", "Memory footprint is reduced by 64% and latency decreases from 4.85 ms to 1.25 ms per packet (a nearly 4x speedup) with less than 0.2% change in F1-score.")
    ]
    for q, a in points:
        story.append(Paragraph(f"<b>Q: {q}</b><br/>{a}", bullet_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
