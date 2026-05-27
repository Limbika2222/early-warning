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
# AI EXECUTIVE SUMMARY
# =====================================================

def generate_ai_summary(
    alerts
):

    total_alerts = len(alerts)

    critical_alerts = len(

        [

            a for a in alerts

            if a.severity == "CRITICAL"
        ]
    )

    diseases = list(

        set(
            a.disease
            for a in alerts
        )
    )

    countries = list(

        set(
            a.country
            for a in alerts
        )
    )

    top_disease = (

        diseases[0]

        if diseases

        else "Unknown"
    )

    # =================================================
    # NARRATIVE
    # =================================================

    summary = f"""

    This reporting period detected
    {total_alerts} outbreak-related
    anomaly signals across
    monitored regions.

    """

    if critical_alerts > 0:

        summary += f"""

        {critical_alerts} critical
        outbreak alerts were identified,
        requiring immediate monitoring
        and response coordination.

        """

    summary += f"""

    The most prominent disease signal
    involved {top_disease},
    with elevated anomaly activity
    observed in monitored datasets.

    Google Trends, Reddit symptom
    discussions, WHO surveillance,
    and AI prediction models
    contributed to risk assessment.

    Continued surveillance is
    recommended to monitor
    emerging outbreak patterns
    and seasonal disease activity.
    """

    return summary

# =====================================================
# OUTBREAK FORECASTING
# =====================================================

def generate_forecast(
    alerts
):

    total_alerts = len(alerts)

    critical_alerts = len(

        [

            a for a in alerts

            if a.severity == "CRITICAL"
        ]
    )

    avg_risk = 0

    if alerts:

        avg_risk = (

            sum(
                a.risk_score
                for a in alerts
            )

            / len(alerts)
        )

    # =================================================
    # 7-DAY RISK
    # =================================================

    if critical_alerts >= 2:

        seven_day_risk = "HIGH"

    elif avg_risk >= 75:

        seven_day_risk = "MODERATE"

    else:

        seven_day_risk = "LOW"

    # =================================================
    # 30-DAY PROBABILITY
    # =================================================

    outbreak_probability = min(

        95,

        int(avg_risk)
    )

    # =================================================
    # SEASONAL LIKELIHOOD
    # =================================================

    if avg_risk >= 80:

        seasonal_likelihood = (

            "Elevated seasonal "
            "transmission risk detected."
        )

    elif avg_risk >= 60:

        seasonal_likelihood = (

            "Moderate seasonal "
            "outbreak likelihood."
        )

    else:

        seasonal_likelihood = (

            "Low seasonal "
            "outbreak probability."
        )

    return {

        "seven_day_risk":
            seven_day_risk,

        "thirty_day_probability":
            outbreak_probability,

        "seasonal_likelihood":
            seasonal_likelihood,
    }

# =====================================================
# SEASONAL INTELLIGENCE ENGINE
# =====================================================

def generate_seasonal_analysis(
    alerts,
    country=None
):

    diseases = list(

        set(
            a.disease.lower()
            for a in alerts
        )
    )

    analysis = []

    # =================================================
    # INFLUENZA
    # =================================================

    if "influenza" in diseases:

        analysis.append(

            """
            Influenza activity typically
            increases during colder
            seasonal periods and
            high population mobility.
            """
        )

    # =================================================
    # MALARIA
    # =================================================

    if "malaria" in diseases:

        analysis.append(

            """
            Malaria transmission risk
            often increases during
            rainy seasons due to
            mosquito breeding conditions.
            """
        )

    # =================================================
    # DENGUE
    # =================================================

    if "dengue" in diseases:

        analysis.append(

            """
            Dengue outbreaks frequently
            intensify during humid
            and monsoon conditions.
            """
        )

    # =================================================
    # COVID
    # =================================================

    if "covid-19" in diseases:

        analysis.append(

            """
            COVID-19 transmission
            remains sensitive to
            mobility patterns,
            indoor gatherings,
            and regional healthcare
            response conditions.
            """
        )

    # =================================================
    # DEFAULT
    # =================================================

    if not analysis:

        analysis.append(

            """
            Seasonal disease activity
            remains under continuous
            surveillance monitoring.
            """
        )

    return " ".join(analysis)

# =====================================================
# PDF WATERMARK
# =====================================================

def add_watermark(
    canvas,
    doc
):

    canvas.saveState()

    # -------------------------------------------------
    # WATERMARK
    # -------------------------------------------------

    canvas.setFont(
        "Helvetica-Bold",
        40
    )

    canvas.setFillGray(
        0.9,
        0.3
    )

    canvas.rotate(45)

    canvas.drawCentredString(

        350,

        50,

        "CONFIDENTIAL"
    )

    canvas.drawCentredString(

        350,

        0,

        "AI SURVEILLANCE REPORT"
    )

    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.setFillGray(0)

    canvas.drawRightString(

        560,

        20,

        (
            f"Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    )

    canvas.restoreState()

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

    # =================================================
    # AI SUMMARY
    # =================================================

    ai_summary = generate_ai_summary(
        alerts
    )

    summary = Paragraph(

        f"""
        <b>Executive AI Summary</b>
        <br/><br/>

        {ai_summary}
        """,

        styles["BodyText"],
    )

    elements.append(summary)

    forecast = generate_forecast(
        alerts
    )

    elements.append(
        Spacer(1, 25)
    )

    forecast_section = Paragraph(

        f"""
        <b>Forecasting Outlook</b>
        <br/><br/>

        7-Day Outbreak Risk:
        <b>
        {forecast['seven_day_risk']}
        </b>
        <br/><br/>

        30-Day Outbreak Probability:
        <b>
        {forecast['thirty_day_probability']}
        </b>
        <br/><br/>

        Seasonal Outbreak Likelihood:
        <br/>
        {forecast['seasonal_likelihood']}
        """,

        styles["BodyText"],
    )

    elements.append(
        forecast_section
    )

    # =================================================
    # SEASONAL ANALYSIS
    # =================================================

    seasonal_analysis = (
        generate_seasonal_analysis(
            alerts
        )
    )

    seasonal_section = Paragraph(

        f"""
        <b>Seasonal Intelligence</b>
        <br/><br/>

        {seasonal_analysis}
        """,

        styles["BodyText"],
    )

    elements.append(
        seasonal_section
    )

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

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)
    
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

def generate_monthly_report(
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
        f"reports/monthly_report_"
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
        Monthly Outbreak Intelligence Report
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

    # =================================================
    # AI SUMMARY
    # =================================================

    ai_summary = generate_ai_summary(
        alerts
    )

    summary = Paragraph(

        f"""
        <b>Executive AI Summary</b>
        <br/><br/>

        {ai_summary}
        """,

        styles["BodyText"],
    )

    elements.append(summary)

    forecast = generate_forecast(
        alerts
    )

    elements.append(
        Spacer(1, 25)
    )

    forecast_section = Paragraph(

        f"""
        <b>Forecasting Outlook</b>
        <br/><br/>

        7-Day Outbreak Risk:
        <b>
        {forecast['seven_day_risk']}
        </b>
        <br/><br/>

        30-Day Outbreak Probability:
        <b>
        {forecast['thirty_day_probability']}
        </b>
        <br/><br/>

        Seasonal Outbreak Likelihood:
        <br/>
        {forecast['seasonal_likelihood']}
        """,

        styles["BodyText"],
    )

    elements.append(
        forecast_section
    )

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

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)
    
    # =================================================
    # SAVE REPORT METADATA
    # =================================================

    report = Report(

        filename=(
            f"monthly_report_"
            f"{timestamp}.pdf"
        ),

        report_type="monthly",

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

# =====================================================
# COUNTRY REPORT
# =====================================================

def generate_country_report(

    db: Session,

    country_name: str
):

    # =================================================
    # FILE
    # =================================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (

        f"reports/{country_name}_"
        f"report_{timestamp}.pdf"
    )

    doc = SimpleDocTemplate(

        filename,

        pagesize=letter,
    )

    styles = getSampleStyleSheet()

    elements = []

    # =================================================
    # LOGO
    # =================================================

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):

        logo = Image(

            logo_path,

            width=90,

            height=90,
        )

        elements.append(logo)

        elements.append(
            Spacer(1, 15)
        )

    # =================================================
    # TITLE
    # =================================================

    title = Paragraph(

        f'''
        <font size=22>
        <b>
        {country_name} Outbreak Intelligence Report
        </b>
        </font>
        ''',

        styles["Title"],
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    # =================================================
    # ALERTS
    # =================================================

    alerts = (

        db.query(Alert)

        .filter(
            Alert.country == country_name
        )

        .all()
    )

    # =================================================
    # AI SUMMARY
    # =================================================

    ai_summary = generate_ai_summary(
        alerts
    )

    summary = Paragraph(

        f"""
        <b>Executive AI Summary</b>
        <br/><br/>

        {ai_summary}
        """,

        styles["BodyText"],
    )

    elements.append(summary)

    forecast = generate_forecast(
        alerts
    )

    elements.append(
        Spacer(1, 25)
    )

    forecast_section = Paragraph(

        f"""
        <b>Forecasting Outlook</b>
        <br/><br/>

        7-Day Outbreak Risk:
        <b>
        {forecast['seven_day_risk']}
        </b>
        <br/><br/>

        30-Day Outbreak Probability:
        <b>
        {forecast['thirty_day_probability']}
        </b>
        <br/><br/>

        Seasonal Outbreak Likelihood:
        <br/>
        {forecast['seasonal_likelihood']}
        """,

        styles["BodyText"],
    )

    elements.append(
        forecast_section
    )

    elements.append(
        Spacer(1, 30)
    )

    # =================================================
    # CHARTS
    # =================================================

    if alerts:

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

        elements.append(

            Paragraph(

                "<b>Severity Distribution</b>",

                styles["Heading2"],
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        elements.append(

            Image(

                severity_chart,

                width=300,

                height=300,
            )
        )

        elements.append(
            Spacer(1, 25)
        )

        elements.append(

            Paragraph(

                "<b>Outbreak Trends</b>",

                styles["Heading2"],
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
            Spacer(1, 30)
        )

    # =================================================
    # ALERT TABLE
    # =================================================

    table_data = [

        [

            "Disease",
            "Severity",
            "Risk Score",
            "Source",
        ]
    ]

    for alert in alerts:

        table_data.append(

            [

                alert.disease,

                alert.severity,

                str(alert.risk_score),

                alert.source,
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
                        "#1E40AF"
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
            ]
        )
    )

    elements.append(table)

    # =================================================
    # BUILD
    # =================================================

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    # =================================================
    # SAVE REPORT RECORD
    # =================================================

    report = Report(

        filename=(
            f"{country_name}_"
            f"report_{timestamp}.pdf"
        ),

        report_type="country",

        file_path=filename,

        generated_by="Infodemiology AI Engine",
    )

    db.add(report)

    db.commit()

    return filename
