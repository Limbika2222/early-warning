from datetime import datetime

import matplotlib.pyplot as plt
from collections import Counter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from reportlab.lib.pagesizes import letter

from sqlalchemy.orm import Session

from app.models.alerts import Alert
from app.models.report import Report

import os

# =====================================================
# SEVERITY DONUT CHART
# =====================================================

def create_severity_chart(
    alerts
):

    severities = [
        a.severity
        for a in alerts
    ]

    counts = Counter(
        severities
    )

    labels = list(
        counts.keys()
    )

    values = list(
        counts.values()
    )

    plt.figure(
        figsize=(5, 5)
    )

    wedges, texts = plt.pie(

        values,

        labels=labels,

        startangle=90,

        wedgeprops=dict(
            width=0.4
        ),
    )

    plt.title(
        "Severity Distribution"
    )

    chart_path = (
        "reports/charts/"
        "severity_chart.png"
    )

    plt.savefig(
        chart_path,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


# =====================================================
# COUNTRY RISK DISTRIBUTION
# =====================================================

def create_country_chart(
    alerts
):

    country_scores = {}

    for alert in alerts:

        country_scores.setdefault(
            alert.country,
            []
        ).append(
            alert.risk_score
        )

    countries = list(
        country_scores.keys()
    )

    avg_scores = [

        sum(scores) / len(scores)

        for scores in (
            country_scores.values()
        )
    ]

    plt.figure(
        figsize=(8, 4)
    )

    plt.bar(
        countries,
        avg_scores,
    )

    plt.title(
        "Country Risk Distribution"
    )

    plt.ylabel(
        "Average Risk Score"
    )

    plt.xticks(
        rotation=20
    )

    chart_path = (
        "reports/charts/"
        "country_chart.png"
    )

    plt.savefig(
        chart_path,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


# =====================================================
# OUTBREAK TREND GRAPH
# =====================================================

def create_trend_chart(
    alerts
):

    diseases = [
        a.disease
        for a in alerts
    ]

    counts = Counter(
        diseases
    )

    x = list(
        counts.keys()
    )

    y = list(
        counts.values()
    )

    plt.figure(
        figsize=(8, 4)
    )

    plt.plot(
        x,
        y,
        marker="o",
    )

    plt.title(
        "Outbreak Trend Graph"
    )

    plt.ylabel(
        "Alert Frequency"
    )

    plt.xticks(
        rotation=20
    )

    chart_path = (
        "reports/charts/"
        "trend_chart.png"
    )

    plt.savefig(
        chart_path,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path

# =====================================================
# REPORT GENERATOR
# =====================================================

def generate_weekly_report(
    db: Session
):

    # =================================================
    # CREATE REPORTS FOLDER
    # =================================================

    os.makedirs(
        "reports/charts",
        exist_ok=True
    )

    # =================================================
    # FILE NAME
    # =================================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"reports/weekly_report_"
        f"{timestamp}.pdf"
    )

    # =================================================
    # PDF DOCUMENT
    # =================================================

    doc = SimpleDocTemplate(

        filename,

        pagesize=letter,
    )

    styles = getSampleStyleSheet()

    elements = []

    # =================================================
    # HEADER
    # =================================================

    title = Paragraph(

        '''
        <font size=22>
        <b>
        Infodemiology Early Warning System
        </b>
        </font>
        ''',

        styles["Title"],
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    subtitle = Paragraph(

        f'''
        <font size=14>
        Weekly Outbreak Intelligence Report
        <br/>
        Generated:
        {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </font>
        ''',

        styles["Normal"],
    )

    elements.append(subtitle)

    elements.append(
        Spacer(1, 25)
    )

    # =================================================
    # EXECUTIVE SUMMARY
    # =================================================

    alerts = (
        db.query(Alert)
        .all()
    )
    
    # =================================================
    # GENERATE CHARTS
    # =================================================

    severity_chart = (
        create_severity_chart(
            alerts
        )
    )

    country_chart = (
        create_country_chart(
            alerts
        )
    )

    trend_chart = (
        create_trend_chart(
            alerts
        )
    )

    total_alerts = len(alerts)

    critical_alerts = len(

        [
            a for a in alerts
            if a.severity == "CRITICAL"
        ]
    )

    countries = len(

        set(
            a.country
            for a in alerts
        )
    )

    summary = Paragraph(

        f'''
        <b>Executive Summary</b>
        <br/><br/>

        Total Alerts:
        {total_alerts}
        <br/>

        Critical Alerts:
        {critical_alerts}
        <br/>

        Countries Under Watch:
        {countries}
        <br/><br/>

        This report summarizes
        outbreak intelligence
        detected from:
        Google Trends,
        Reddit signals,
        WHO surveillance,
        and AI anomaly detection.
        ''',

        styles["BodyText"],
    )

    elements.append(summary)

    elements.append(
        Spacer(1, 30)
    )

    # =================================================
    # ALERT TABLE
    # =================================================

    table_data = [

        [
            "Disease",
            "Country",
            "Source",
            "Severity",
            "Risk Score",
        ]
    ]

    for alert in alerts[:20]:

        table_data.append(

            [
                alert.disease,
                alert.country,
                alert.source,
                alert.severity,
                str(alert.risk_score),
            ]
        )

    table = Table(table_data)

    table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#2563EB"
                    ),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    10,
                ),
            ]
        )
    )

    elements.append(table)

    elements.append(
        Spacer(1, 40)
    )
    
    elements.append(PageBreak())

    # =================================================
    # CHARTS SECTION
    # =================================================

    charts_title = Paragraph(

        '''
        <b>
        Outbreak Analytics
        </b>
        ''',

        styles["Heading2"],
    )

    elements.append(
        charts_title
    )

    elements.append(
        Spacer(1, 20)
    )

    # -------------------------------------------------
    # SEVERITY DONUT
    # -------------------------------------------------

    elements.append(

        Paragraph(

            "<b>Severity Distribution</b>",

            styles["BodyText"],
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Image(

            severity_chart,

            width=320,

            height=320,
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # -------------------------------------------------
    # COUNTRY RISK
    # -------------------------------------------------

    elements.append(

        Paragraph(

            "<b>Country Risk Distribution</b>",

            styles["BodyText"],
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Image(

            country_chart,

            width=450,

            height=250,
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # -------------------------------------------------
    # OUTBREAK TRENDS
    # -------------------------------------------------

    elements.append(

        Paragraph(

            "<b>Outbreak Trend Graph</b>",

            styles["BodyText"],
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Image(

            trend_chart,

            width=450,

            height=250,
        )
    )

    elements.append(
        Spacer(1, 40)
    )

    # =================================================
    # AI RECOMMENDATIONS
    # =================================================

    recommendations = Paragraph(

        '''
        <b>AI Recommendations</b>
        <br/><br/>

        • Increase surveillance
        in high-risk countries.
        <br/>

        • Monitor disease spread
        across neighboring regions.
        <br/>

        • Continue anomaly monitoring
        every 15 minutes.
        <br/>

        • Investigate abnormal
        Google Trends spikes.
        ''',

        styles["BodyText"],
    )

    elements.append(
        recommendations
    )

    elements.append(
        Spacer(1, 60)
    )

    # =================================================
    # SIGNATURE
    # =================================================

    signature = Paragraph(

        '''
        <b>
        Generated by:
        </b>
        <br/><br/>

        Infodemiology AI Engine
        <br/>

        Digital Surveillance Unit
        ''',

        styles["Normal"],
    )

    elements.append(signature)

    # =================================================
    # BUILD PDF
    # =================================================

    doc.build(elements)
    
    # =================================================
    # SAVE REPORT METADATA
    # =================================================

    report = Report(

        filename=(
            f"weekly_report_"
            f"{timestamp}.pdf"
        ),

        report_type="weekly",

        file_path=filename,

        period_start=datetime.now().strftime(
            "%Y-%m-%d"
        ),

        period_end=datetime.now().strftime(
            "%Y-%m-%d"
        ),

        generated_by="Infodemiology AI Engine",
    )

    db.add(report)

    db.commit()

    return filename