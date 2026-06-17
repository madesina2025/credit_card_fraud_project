# dash_app.py - Professional Credit Card Fraud Detection Dashboard

import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table, Input, Output

from database.db import SessionLocal
from database.models import FraudPrediction



def get_risk_category(probability):
    if probability >= 0.90:
        return "Critical"
    elif probability >= 0.70:
        return "High"
    elif probability >= 0.50:
        return "Medium"
    else:
        return "Low"

def load_live_predictions():
    db = SessionLocal()
    rows = db.query(FraudPrediction).order_by(FraudPrediction.created_at.desc()).all()

    data = []

    for row in rows:
        data.append({
            "ID": row.id,
            "Customer": row.customer_id,
            "Merchant": row.merchant,
            "Country": row.country,
            "Channel": row.channel,
            "Amount (£)": row.transaction_amount,
            "Prediction": row.prediction,
            "Risk Label": row.risk_label,
            "Fraud Probability": round(row.fraud_probability, 4),
            "Recommended Action": row.recommended_action,
            "Created At": row.created_at   
    })
    db.close()

    live_df = pd.DataFrame(data)

    expected_columns = [
        "ID", "Customer", "Merchant", "Country", "Channel",
        "Amount (£)", "Prediction", "Risk Label",
        "Fraud Probability", "Risk Category",
        "Recommended Action", "Created At"
    ]

    if live_df.empty:
        live_df = pd.DataFrame(columns=expected_columns)

    for col in expected_columns:
        if col not in live_df.columns:
            live_df[col] = None

    return live_df


live_df = load_live_predictions()
# live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)
if "Fraud Probability" not in live_df.columns:
    live_df["Fraud Probability"] = 0

live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)

live_df = load_live_predictions()
required_columns = {
    "Risk Label": "",
    "Fraud Probability": 0,
    "Amount (£)": 0,
    "Risk Category": "Low",
    "Merchant": "",
    "Country": "",
    "Channel": "",
    "Created At": ""
}

for col, default_value in required_columns.items():
    if col not in live_df.columns:
        live_df[col] = default_value


live_fraud_count = len(live_df[live_df["Risk Label"] == "Fraud"])
live_genuine_count = len(live_df[live_df["Risk Label"] == "Genuine"])
live_fraud_exposure = live_df[live_df["Risk Label"] == "Fraud"]["Amount (£)"].sum()

fraud_by_merchant = (
    live_df[live_df["Risk Label"] == "Fraud"]
    .groupby("Merchant")["Amount (£)"]
    .sum()
    .reset_index()
)
fraud_by_country = (
    live_df[live_df["Risk Label"] == "Fraud"]
    .groupby("Country")["Amount (£)"]
    .sum()
    .reset_index()
)
fraud_by_channel = (
    live_df[live_df["Risk Label"] == "Fraud"]
    .groupby("Channel")["Amount (£)"]
    .sum()
    .reset_index()
)
fraud_trend = (
    live_df[live_df["Risk Label"] == "Fraud"]
    .copy()
)

fraud_trend["Created At"] = pd.to_datetime(
    fraud_trend["Created At"]
)

fraud_trend = (
    fraud_trend
    .groupby(pd.Grouper(key="Created At", freq="30s"))
    .size()
    .reset_index(name="Fraud Count")
)

top_risk_transactions = (
    live_df[live_df["Risk Label"] == "Fraud"]
    .sort_values(["Fraud Probability", "Amount (£)"], ascending=False)
    .head(10)
)



# Load data
# df = pd.read_csv("dashboard/flagged_transactions.csv")
model_df = pd.read_csv("data/processed/model_comparison.csv")
cm_df = pd.read_csv("data/processed/confusion_matrix_summary.csv")

# # KPIs
# total_transactions = len(df)
# predicted_frauds = int(df["Predicted_Class"].sum())
# fraud_rate = (predicted_frauds / total_transactions) * 100 if total_transactions > 0 else 0
# fraud_df = df[df["Predicted_Class"] == 1]
# fraud_loss = fraud_df["Amount"].sum()
# avg_fraud_amount = fraud_df["Amount"].mean()

# Load live PostgreSQL data for lower dashboard section
df = load_live_predictions()

# KPIs
total_transactions = len(df)

if total_transactions > 0:
    predicted_frauds = int((df["Risk Label"] == "Fraud").sum())
    fraud_rate = (predicted_frauds / total_transactions) * 100
    fraud_df = df[df["Risk Label"] == "Fraud"]
    fraud_loss = fraud_df["Amount (£)"].sum()
    avg_fraud_amount = fraud_df["Amount (£)"].mean()
else:
    predicted_frauds = 0
    fraud_rate = 0
    fraud_df = pd.DataFrame()
    fraud_loss = 0
    avg_fraud_amount = 0

# Best model
best_model_row = model_df.sort_values("AUC", ascending=False).iloc[0]
best_model = best_model_row["Model"]

app = Dash(__name__)
app.title = "Credit Card Fraud Detection Dashboard"


# def kpi_card(title, value):
#     return html.Div([
#         html.H4(title),
#         html.H2(value)
#     ], style={
#         "backgroundColor": "#f8f9fa",
#         "padding": "20px",
#         "borderRadius": "10px",
#         "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
#         "width": "18%",
#         "display": "inline-block",
#         "margin": "1%"
#     })
def kpi_card(title, value, bg_color="#f8f9fa", text_color="black"):
    return html.Div(
        [
            html.H4(title),
            html.H2(value, style={"color": text_color})
        ],
        style={
            "backgroundColor": bg_color,
            "color": text_color,
            "padding": "25px",
            "borderRadius": "12px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.12)",
            "width": "18%",
            "display": "inline-block",
            "margin": "1%",
            "textAlign": "center",
            "fontWeight": "bold"
        }
    )

# def fraud_alert_banner(fraud_count, exposure):
def fraud_alert_banner(
        fraud_count,
        exposure,
        highest_risk_merchant="N/A",
        highest_risk_country="N/A",
        most_attacked_channel="N/A",
        fraud_rate=0
    ):
    if fraud_rate > 40:
        bg_color = "#ffe6e6"
        txt_color = "red"
    elif fraud_rate > 20:
        bg_color = "#fff0cc"
        txt_color = "darkorange"
    elif fraud_rate > 10:
        bg_color = "#fff9cc"
        txt_color = "#c09000"
    else:
        bg_color = "#e8f5e9"
        txt_color = "green"

    if fraud_count > 0:
        return html.Div(
            [
                html.H2("🚨 CRITICAL FRAUD OPERATIONS ALERT"),
                html.H3(f"{fraud_count} fraud transactions detected"),
                html.H3(f"Total Fraud Exposure: £{exposure/1_000_000:.2f}M"),
                html.P(f"Highest Risk Merchant: {highest_risk_merchant}"),
                html.P(f"Highest Risk Country: {highest_risk_country}"),
                html.P(f"Most Attacked Channel: {most_attacked_channel}"),
                html.P(f"Live Fraud Rate: {fraud_rate:.2f}%"),
            ],
            style={
                "backgroundColor": bg_color,
                "color": txt_color,
                "padding": "20px",
                "borderRadius": "10px",
                "textAlign": "center",
                "fontWeight": "bold",
                "margin": "20px"
            }
        )
    else:
        return html.Div(
            "✅ No live fraud alerts detected",
            style={
                "backgroundColor": "#e8f5e9",
                "color": "green",
                "padding": "20px",
                "borderRadius": "10px",
                "textAlign": "center",
                "fontWeight": "bold",
                "margin": "20px"
            }
        )

app.layout = html.Div([
    html.H1("💳 Credit Card Fraud Detection Dashboard", style={"textAlign": "center"}),

    html.H3(
        "🟢 SYSTEM STATUS : LIVE",
        style={
            "textAlign": "center",
            "color": "green",
            "fontWeight": "bold",
            "marginBottom": "20px"
        }
    ),
    # fraud_alert_banner(live_fraud_count, live_fraud_exposure),


    # html.Div([
    #     kpi_card("Live Fraud Alerts", f"{live_fraud_count:,}"),
    #     kpi_card("Live Genuine Transactions", f"{live_genuine_count:,}"),
    #     kpi_card("Live Fraud Exposure", f"£{live_fraud_exposure:,.2f}"),
    # ], style={"textAlign": "center"}),
    html.Div(id="live-alert-banner"),

    html.Div(id="live-kpi-cards"),

    html.Div(id="risk-category-kpi-cards"),
    
    # added new guage
    html.H2("🚦 Live Fraud Risk Gauge"),
    dcc.Graph(id="fraud-risk-gauge"),

    html.H2("🔥 Fraud Heat Map by Hour"),
    dcc.Graph(id="fraud-heatmap"),

    html.H2("🌍 Top 5 Risk Countries"),
    dcc.Graph(id="top-country-chart"),

    html.H2("🌍 Top 5 Risk Countries"),
dcc.Graph(id="top-risk-countries-chart"),

html.H2("🏪 Top 5 Risk Merchants"),
dcc.Graph(id="top-risk-merchants-chart"),

html.H2("📊 Fraud Probability Distribution"),
dcc.Graph(id="fraud-probability-histogram"),

html.H2("📡 Live Fraud Alert Ticker"),
html.Div(id="live-alert-ticker"),

html.H2("🕒 Hourly Fraud Summary"),
dash_table.DataTable(
    id="hourly-fraud-table",
    page_size=10,
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "center", "padding": "8px"},
    style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
),

html.H2("📌 Executive Summary Panel"),
html.Div(id="executive-summary-panel"),

    html.Div(id="last-updated-time", style={
        "textAlign": "center",
        "fontWeight": "bold",
        "margin": "15px",
        "color": "#555"
        }),

    html.H2("🚨 Latest Fraud Alerts"),

    html.Button("Download Live Fraud Data", id="download-live-btn"),

    dcc.Download(id="download-live-data"),

    html.Div(id="live-alert-feed"),
    # html.H2("🌍 Live Fraud by Country"),

    # html.H2("🏪 Live Fraud by Merchant"),
    # dcc.Graph(id="fraud-merchant-chart"),


    # html.H2("💳 Live Fraud by Channel"),
    # dcc.Graph(id="fraud-channel-chart"),

    html.H2("🏪 Live Fraud by Merchant"),
    dcc.Graph(id="fraud-merchant-chart"),

    html.H2("🌍 Live Fraud by Country"),
    dcc.Graph(id="fraud-country-chart"),

    html.H2("💳 Live Fraud by Channel"),
    dcc.Graph(id="fraud-channel-chart"),

    dcc.Interval(
        id="live-update-interval",
        interval=5000,
        n_intervals=0
    ),

    # html.H2("Fraud Prediction Simulator"),

    dcc.Input(
        id="amount-input",
        type="number",
        placeholder="Transaction Amount",
        value=100
    ),

    html.Button(
        "Predict",
        id="predict-btn",
        n_clicks=0
    ),

# html.H2("Fraud Exposure by Merchant"),
# dcc.Graph(id="fraud-merchant-chart"),

# html.H2("Fraud Exposure by Country"),

# dcc.Graph(
#     figure=px.choropleth(
#         fraud_by_country,
#         locations="Country",
#         color="Amount (£)",
#         hover_name="Country",
#         color_continuous_scale="Reds",
#         locationmode="country names",
#         title="Fraud Exposure by Country"
#     )
# ),

html.H2("Fraud Exposure by Channel"),

dcc.Graph(
    figure=px.pie(
        fraud_by_channel,
        names="Channel",
        values="Amount (£)",
        title="Fraud Exposure by Channel"
    )
),

html.H2("🏆 Live Top 10 Highest Risk Transactions"),

dash_table.DataTable(
    id="live-top-risk-table",
    columns=[
        {"name": "ID", "id": "ID"},
        {"name": "Customer", "id": "Customer"},
        {"name": "Merchant", "id": "Merchant"},
        {"name": "Country", "id": "Country"},
        {"name": "Channel", "id": "Channel"},
        {"name": "Amount (£)", "id": "Amount (£)"},
        {"name": "Fraud Probability", "id": "Fraud Probability"},
        {"name": "Risk Category", "id": "Risk Category"},
        {"name": "Recommended Action", "id": "Recommended Action"},
        {"name": "Created At", "id": "Created At"},
    ],
    data=[],
    page_size=10,
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "center", "padding": "8px"},
    style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},  
    style_data_conditional=[

        {
            "if": {
                "filter_query": '{Risk Category} = "Critical"',
                "column_id": "Risk Category"
            },
            "backgroundColor": "#8B0000",
            "color": "white",
            "fontWeight": "bold"
        },

        {
            "if": {
                "filter_query": '{Risk Category} = "High"',
                "column_id": "Risk Category"
            },
            "backgroundColor": "#FF0000",
            "color": "white",
            "fontWeight": "bold"
        },

        {
            "if": {
                "filter_query": '{Risk Category} = "Medium"',
                "column_id": "Risk Category"
            },
            "backgroundColor": "#FFA500",
            "color": "black",
            "fontWeight": "bold"
        },

        {
            "if": {
                "filter_query": '{Risk Category} = "Low"',
                "column_id": "Risk Category"
            },
            "backgroundColor": "#008000",
            "color": "white",
            "fontWeight": "bold"
        }

    ],
),   
    

html.H2("Fraud Trend Over Time"),

dcc.Graph(id="live-fraud-trend-chart"),

kpi_card("Total Transactions", f"{total_transactions:,}"),

    html.Br(),
    html.Br(),

    html.Div(id="prediction-result"),

    html.Hr(),

    html.Div([
        kpi_card("Total Transactions", f"{total_transactions:,}"),
        kpi_card("Predicted Frauds", f"{predicted_frauds:,}"),
        kpi_card("Fraud Rate", f"{fraud_rate:.2f}%"),
        kpi_card("Estimated Fraud Exposure", f"£{fraud_loss:,.2f}"),
        kpi_card("Best Model", best_model),
    ], style={"textAlign": "center"}),

    html.Hr(),

    html.H2("Fraud vs Non-Fraud Distribution"),
    dcc.Graph(
        figure=px.pie(
            df,
            names="Risk Label",
            title="Fraud vs Non-Fraud Transactions",
            color="Risk Label",
            color_discrete_map={"Genuine": "green", "Fraud": "red"}
        )
    ),

    html.H2("Fraud Amount Distribution"),
    dcc.Graph(
        figure=px.histogram(
            fraud_df,
            x="Amount (£)",
            nbins=50,
            title="Distribution of Predicted Fraud Amounts"
        )
    ),

    html.H2("Model Performance Comparison"),
    dash_table.DataTable(
        data=model_df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in model_df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
        style_data_conditional=[
            {
                "if": {"filter_query": "{Risk Label} = 'Fraud'"},
                "backgroundColor": "#ffe6e6",
                "color": "red",
                "fontWeight": "bold"
            },
            {
                "if": {"filter_query": "{Risk Label} = 'Genuine'"},
                "backgroundColor": "#e8f5e9",
                "color": "green"
            }
        ],
    ),

    html.H2("Confusion Matrix Summary"),
    dash_table.DataTable(
        data=cm_df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in cm_df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},  
    ),

    html.H2("Top Suspicious Transactions"),
    dash_table.DataTable(
        data=fraud_df.sort_values("Amount (£)", ascending=False).head(20).to_dict("records"),
        columns=[
            {"name": "Created At", "id": "Created At"},
            {"name": "Customer", "id": "Customer"},
            {"name": "Merchant", "id": "Merchant"},
            {"name": "Country", "id": "Country"},
            {"name": "Channel", "id": "Channel"},
            {"name": "Amount (£)", "id": "Amount (£)"},
            {"name": "Fraud Probability", "id": "Fraud Probability"},
            {"name": "Risk Label", "id": "Risk Label"},
            {"name": "Recommended Action", "id": "Recommended Action"},
        ],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},

        style_data_conditional=[

            # Fraud rows (red)
            {
                    "if": {
                        "column_id": "Risk Label",
                        "filter_query": '{Risk Label} = "Fraud"'
                    },
                    "backgroundColor": "#8B0000",
                    "color": "white",
                    "fontWeight": "bold"
                },
                {
                    "if": {
                        "column_id": "Risk Label",
                        "filter_query": '{Risk Label} = "Genuine"'
                    },
                    "backgroundColor": "#008000",
                    "color": "white",
                    "fontWeight": "bold"
                },

            # Very high probability (>0.95)
            {
                "if": {
                    "column_id": "Fraud Probability",
                    "filter_query": "{Fraud Probability} >= 0.98"
                },
                "backgroundColor": "#8B0000",
                "color": "white",
                "fontWeight": "bold"
            },
            {
                "if": {
                    "column_id": "Fraud Probability",
                    "filter_query": "{Fraud Probability} >= 0.95 && {Fraud Probability} < 0.98"
                },
                "backgroundColor": "#ff4d4d",
                "color": "white",
                "fontWeight": "bold"
            },
            {
                "if": {
                    "column_id": "Fraud Probability",
                    "filter_query": "{Fraud Probability} >= 0.90 && {Fraud Probability} < 0.95"
                },
                "backgroundColor": "#ffcc66",
                "color": "black",
                "fontWeight": "bold"
            },
            {
                "if": {
                    "column_id": "Fraud Probability",
                    "filter_query": "{Fraud Probability} < 0.70"
                },
                "backgroundColor": "#d9ead3",
                "color": "green"
            },
            # High amount > £4000
            {
                "if": {
                    "column_id": "Amount (£)",
                    "filter_query": "{Amount (£)} >= 4000"
                },
                "backgroundColor": "#ffd966",
                "fontWeight": "bold"
            },
            {
                "if": {
                    "column_id": "Amount (£)",
                    "filter_query": "{Amount (£)} >= 3000 && {Amount (£)} < 4000"
                },
                "backgroundColor": "#fff2cc"
            },
            {
                "if": {
                    "column_id": "Recommended Action",
                    "filter_query":
                    '{Recommended Action} contains "Flag"'
                },
                "backgroundColor": "#ffcccc",
                "color": "darkred",
                "fontWeight": "bold"
            },
            {
                "if": {
                    "column_id": "Recommended Action",
                    "filter_query":
                    '{Recommended Action} contains "Approve"'
                },
                "backgroundColor": "#d9ead3",
                "color": "green",
                "fontWeight": "bold"
            }
        ]
    ),

    html.Br(),

    html.Button("Download Fraud Cases", id="download-btn"),

    html.H2("Live Fraud Predictions from PostgreSQL"),

    dash_table.DataTable(
        id="live-predictions-table",
        style_data_conditional=[
    {
        "if": {"filter_query": "{Risk Label} = 'Fraud'"},
        "backgroundColor": "#ffe6e6",
        "color": "red",
        "fontWeight": "bold"
    },
    {
        "if": {"filter_query": "{Risk Label} = 'Genuine'"},
        "backgroundColor": "#e8f5e9",
        "color": "green"
    }
],
        data=live_df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in live_df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
        ),
        
    dcc.Download(id="download-fraud-cases"),

], style={"padding": "30px", "fontFamily": "Arial"})

@app.callback(
    Output("download-fraud-cases", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_fraud_cases(n_clicks):
    return dcc.send_data_frame(
        fraud_df.to_csv,
        "predicted_fraud_cases.csv",
        index=False
    )

@app.callback(
    Output("prediction-result", "children"),
    Input("predict-btn", "n_clicks"),
    Input("amount-input", "value"),
    prevent_initial_call=True
)
def predict_from_dashboard(n_clicks, amount):

    sample_transaction = df.drop(
        columns=["Actual_Class", "Predicted_Class"]
    ).head(1).to_dict("records")[0]

    sample_transaction["Amount (£)"] = amount

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=sample_transaction
    )

    result = response.json()

    return html.Div([
        html.H3(f"Prediction: {result['risk_label']}"),
        html.P(f"Fraud Probability: {result['fraud_probability']}"),
        html.P(f"Recommended Action: {result['recommended_action']}"),
        html.P(f"Prediction ID: {result['prediction_id']}")
    ], style={
        "backgroundColor": "#f8f9fa",
        "padding": "20px",
        "borderRadius": "10px",
        "marginTop": "10px"
    })

@app.callback(
    Output("live-predictions-table", "data"),
    Input("live-update-interval", "n_intervals")
    )
def update_live_predictions(n):
    live_df = load_live_predictions()
    
    print(f"Loaded records: {len(live_df)}")
    
    return live_df.to_dict("records")

@app.callback(
    Output("live-alert-banner", "children"),
    Output("live-kpi-cards", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_live_summary(n):
    live_df = load_live_predictions()

    live_fraud_count = len(live_df[live_df["Risk Label"] == "Fraud"])
    live_genuine_count = len(live_df[live_df["Risk Label"] == "Genuine"])
    live_fraud_exposure = live_df[live_df["Risk Label"] == "Fraud"]["Amount (£)"].sum()

    total_live_transactions = live_fraud_count + live_genuine_count
    fraud_only = live_df[live_df["Risk Label"] == "Fraud"]

    highest_risk_merchant = fraud_only["Merchant"].mode()[0] if len(fraud_only) > 0 else "N/A"
    highest_risk_country = fraud_only["Country"].mode()[0] if len(fraud_only) > 0 else "N/A"
    most_attacked_channel = fraud_only["Channel"].mode()[0] if len(fraud_only) > 0 else "N/A"

    fraud_rate = (
        (live_fraud_count / total_live_transactions) * 100
        if total_live_transactions > 0
        else 0
    )

    # banner = fraud_alert_banner(live_fraud_count, live_fraud_exposure)
    banner = fraud_alert_banner(
        live_fraud_count,
        live_fraud_exposure,
        highest_risk_merchant,
        highest_risk_country,
        most_attacked_channel,
        fraud_rate
    )

    # cards = html.Div([
    #     kpi_card("Live Fraud Alerts", f"{live_fraud_count:,}"),
    #     kpi_card("Live Genuine Transactions", f"{live_genuine_count:,}"),
    #     kpi_card("Live Fraud Exposure",f"£{live_fraud_exposure/1_000_000:.2f}M"),
    #     kpi_card("Fraud Rate", f"{fraud_rate:.2f}%"),
    # ], style={"textAlign": "center"})
    cards = html.Div([
        kpi_card("Live Fraud Alerts", f"{live_fraud_count:,}", "#ffe6e6", "red"),
        kpi_card("Live Genuine Transactions", f"{live_genuine_count:,}", "#e8f5e9", "green"),
        kpi_card("Live Fraud Exposure", f"£{live_fraud_exposure/1_000_000:.2f}M", "#fff3e0", "#d35400"),
        kpi_card("Fraud Rate", f"{fraud_rate:.2f}%", "#fce4ec", "#b71c1c"),
    ], style={"textAlign": "center"})

    return banner, cards

@app.callback(
    Output("live-fraud-trend-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_live_fraud_trend(n):
    live_df = load_live_predictions()

    fraud_trend = live_df[live_df["Risk Label"] == "Fraud"].copy()

    if fraud_trend.empty:
        return px.line(
            x=[],
            y=[],
            title="Live Fraud Trend Over Time"
        )

    fraud_trend["Created At"] = pd.to_datetime(fraud_trend["Created At"])

    # Last 2 hours only
    cutoff = pd.Timestamp.now() - pd.Timedelta(hours=2)

    # Last 2 hours only
    cutoff = pd.Timestamp.now() - pd.Timedelta(hours=2)

    fraud_trend = fraud_trend[
        fraud_trend["Created At"] >= cutoff
    ]

    fraud_trend = (
        fraud_trend
        .groupby(pd.Grouper(key="Created At", freq="30s"))
        .size()
        .reset_index(name="Fraud Count")
    )

    fig = px.area(
        fraud_trend,
        x="Created At",
        y="Fraud Count",
        title="Live Fraud Trend Over Time"
    )

    fig.update_traces(
        line_color="red",
        fillcolor="rgba(255,0,0,0.2)"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Time",
        yaxis_title="Fraud Count",
        hovermode="x unified"
    )
    return fig

@app.callback(
    Output("live-alert-feed", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_alert_feed(n):

    live_df = load_live_predictions()

    frauds = (
        live_df[live_df["Risk Label"] == "Fraud"]
        .sort_values("ID", ascending=False)
        .head(10)
    )

    alerts = []

    for _, row in frauds.iterrows():

        alerts.append(
            html.Div(
                f"🚨 {row['Merchant']} | "
                f"{row['Country']} | "
                f"£{row['Amount (£)']:,.2f} | "
                f"{row['Fraud Probability']}",
                style={
                    "padding": "10px",
                    "marginBottom": "5px",
                    "backgroundColor": "#ffe6e6",
                    "borderLeft": "5px solid red",
                    "fontWeight": "bold"
                }
            )
        )

    return alerts

# @app.callback(
#     Output("fraud-merchant-chart", "figure"),
#     Input("live-update-interval", "n_intervals")
# )
# def update_merchant_chart(n):

#     live_df = load_live_predictions()

#     frauds = live_df[
#         live_df["Risk Label"] == "Fraud"
#     ]

#     merchant_df = (
#         frauds.groupby("Merchant")["Amount (£)"]
#         .sum()
#         .reset_index(name="Fraud Exposure")
#         .sort_values("Fraud Exposure", ascending=False)
#     )

#     fig = px.bar(
#         merchant_df,
#         x="Merchant",
#         y="Fraud Exposure",
#         text="Fraud Exposure",
#         title="Live Fraud Exposure by Merchant"
#     )

#     fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside")
#     fig.update_layout(yaxis_title="Fraud Exposure (£)")
#     return fig
@app.callback(
    Output("fraud-merchant-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_merchant_chart(n):

    live_df = load_live_predictions()

    frauds = live_df[
        live_df["Risk Label"] == "Fraud"
    ]

    merchant_df = (
        frauds.groupby("Merchant")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
    )

    fig = px.bar(
        merchant_df,
        x="Merchant",
        y="Fraud Exposure",
        text="Fraud Exposure",
        title="Live Fraud Exposure by Merchant",
        color="Fraud Exposure",
        color_continuous_scale="Reds"
    )

    fig.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Fraud Exposure (£)",
        xaxis_title="Merchant",
        showlegend=False,
        height=500
    )

    return fig

@app.callback(
    Output("fraud-channel-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_channel_chart(n):
    live_df = load_live_predictions()

    frauds = live_df[live_df["Risk Label"] == "Fraud"]

    if frauds.empty:
        return px.pie(
            names=["No fraud yet"],
            values=[1],
            title="Live Fraud Exposure by Channel"
        )

    channel_df = (
        frauds.groupby("Channel")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
    )

    fig = px.pie(
        channel_df,
        names="Channel",
        values="Fraud Exposure",
        hole=0.45,
        title="Live Fraud Exposure by Channel"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Exposure: £%{value:,.0f}<br>%{percent}<extra></extra>"
    )

    return fig

    # fig = px.pie(
    #     channel_df,
    #     names="Channel",
    #     values="Fraud Exposure",
    #     title="Live Fraud Exposure by Channel",
    #     hole=0.4
    # )

    # fig.update_traces(
    #     textinfo="label+percent+value",
    #     texttemplate="%{label}<br>£%{value:,.0f}<br>%{percent}"
    # )

    # return fig
    # fig = px.pie(
    #     channel_df,
    #     names="Channel",
    #     values="Amount (£)",
    #     hole=0.45,
    #     title="Live Fraud Exposure by Channel"
    # )

    # fig.update_traces(
    #     textposition='inside',
    #     textinfo='percent+label',
    #     hovertemplate="<b>%{label}</b><br>Exposure: £%{value:,.0f}<br>%{percent}"
    # )

    # return fig


@app.callback(
    Output("live-top-risk-table", "data"),
    Input("live-update-interval", "n_intervals")
)
def update_top_risk_table(n):
    live_df = load_live_predictions()

    live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)

    top_risk = (
        live_df[live_df["Risk Label"] == "Fraud"]
        .sort_values("ID", ascending=False)
        .head(10)
    )

    return top_risk.to_dict("records")

@app.callback(
    Output("risk-category-kpi-cards", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_risk_category_cards(n):
    live_df = load_live_predictions()

    live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)

    critical_count = len(live_df[live_df["Risk Category"] == "Critical"])
    high_count = len(live_df[live_df["Risk Category"] == "High"])
    medium_count = len(live_df[live_df["Risk Category"] == "Medium"])
    low_count = len(live_df[live_df["Risk Category"] == "Low"])

    return html.Div([
        kpi_card("Critical Alerts", f"{critical_count:,}"),
        kpi_card("High Alerts", f"{high_count:,}"),
        kpi_card("Medium Alerts", f"{medium_count:,}"),
        kpi_card("Low Alerts", f"{low_count:,}"),
    ], style={"textAlign": "center"})

@app.callback(
    Output("last-updated-time", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_last_updated_time(n):
    now = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Last updated: {now}"

@app.callback(
    Output("download-live-data", "data"),
    Input("download-live-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_live_fraud_data(n_clicks):
    live_df = load_live_predictions()
    live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)

    fraud_df = live_df[live_df["Risk Label"] == "Fraud"]

    return dcc.send_data_frame(
        fraud_df.to_csv,
        "live_fraud_predictions.csv",
        index=False
    )
@app.callback(
    Output("fraud-country-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_country_chart(n):
    live_df = load_live_predictions()
    
    fraud_df = live_df[live_df["Risk Label"] == "Fraud"]
    # print(fraud_df.columns)
    # country_df = (
    #     fraud_df
    #     .groupby("Country")
    #     .size()
    #     .reset_index(name="Fraud Count")
    #     .sort_values("Fraud Count", ascending=False)
    # )
    country_df = (
        fraud_df
        .groupby("Country")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
    )

    # fig = px.bar(
    #     country_df,
    #     x="Country",
    #     y="Fraud Count",
    #     color="Fraud Count",
    #     title="Live Fraud By Country"
    # )
    fig = px.bar(
        country_df,
        x="Country",
        y="Fraud Exposure",
        color="Fraud Exposure",
        color_continuous_scale="Reds",
        text="Fraud Exposure",
        title="Live Fraud Exposure by Country"
    )

    fig.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Fraud Exposure (£)",
        showlegend=False
    )

    return fig
@app.callback(
    Output("fraud-risk-gauge", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_fraud_risk_gauge(n):
    live_df = load_live_predictions()

    total_transactions = len(live_df)
    fraud_count = len(live_df[live_df["Risk Label"] == "Fraud"])

    fraud_rate = (
        fraud_count / total_transactions * 100
        if total_transactions > 0
        else 0
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fraud_rate,
        title={"text": "Live Fraud Rate (%)"},
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkred"},
            "steps": [
                {"range": [0, 10], "color": "#e8f5e9"},
                {"range": [10, 30], "color": "#fff3cd"},
                {"range": [30, 60], "color": "#ffcc80"},
                {"range": [60, 100], "color": "#ff9999"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": fraud_rate
            }
        }
    ))

    fig.update_layout(height=400)

    return fig

@app.callback(
    Output("fraud-heatmap", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_fraud_heatmap(n):

    live_df = load_live_predictions()

    frauds = live_df[live_df["Risk Label"] == "Fraud"].copy()

    if frauds.empty:
        return px.imshow([[0]], text_auto=True)

    frauds["Created At"] = pd.to_datetime(frauds["Created At"])

    frauds["Hour"] = frauds["Created At"].dt.hour
    frauds["Minute"] = frauds["Created At"].dt.minute

    heatmap_df = (
        frauds.groupby(["Hour", "Minute"])
        .size()
        .reset_index(name="Fraud Count")
    )

    fig = px.density_heatmap(
        heatmap_df,
        x="Minute",
        y="Hour",
        z="Fraud Count",
        color_continuous_scale="Reds",
        title="Fraud Activity Heatmap"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Minute",
        yaxis_title="Hour of Day"
    )

    return fig

@app.callback(
    Output("top-country-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_country_risk(n):

    live_df = load_live_predictions()

    frauds = live_df[live_df["Risk Label"]=="Fraud"]

    country_df = (
        frauds.groupby("Country")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
        .head(5)
    )

    fig = px.bar(
        country_df,
        x="Fraud Exposure",
        y="Country",
        orientation="h",
        color="Fraud Exposure",
        color_continuous_scale="Reds",
        text="Fraud Exposure",
        title="Top 5 Risk Countries"
    )

    fig.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending")
    )

    return fig

@app.callback(
    Output("top-risk-countries-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_top_risk_countries(n):
    live_df = load_live_predictions()
    frauds = live_df[live_df["Risk Label"] == "Fraud"]

    country_df = (
        frauds.groupby("Country")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
        .head(5)
    )

    fig = px.bar(
        country_df,
        x="Fraud Exposure",
        y="Country",
        orientation="h",
        color="Fraud Exposure",
        color_continuous_scale="Reds",
        text="Fraud Exposure",
        title="Top 5 Risk Countries by Fraud Exposure"
    )

    fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside")
    fig.update_layout(height=450, yaxis=dict(categoryorder="total ascending"))

    return fig


@app.callback(
    Output("top-risk-merchants-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_top_risk_merchants(n):
    live_df = load_live_predictions()
    frauds = live_df[live_df["Risk Label"] == "Fraud"]

    merchant_df = (
        frauds.groupby("Merchant")["Amount (£)"]
        .sum()
        .reset_index(name="Fraud Exposure")
        .sort_values("Fraud Exposure", ascending=False)
        .head(5)
    )

    fig = px.bar(
        merchant_df,
        x="Fraud Exposure",
        y="Merchant",
        orientation="h",
        color="Fraud Exposure",
        color_continuous_scale="Reds",
        text="Fraud Exposure",
        title="Top 5 Risk Merchants by Fraud Exposure"
    )

    fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside")
    fig.update_layout(height=450, yaxis=dict(categoryorder="total ascending"))

    return fig


@app.callback(
    Output("fraud-probability-histogram", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_fraud_probability_histogram(n):
    live_df = load_live_predictions()

    fig = px.histogram(
        live_df,
        x="Fraud Probability",
        nbins=30,
        color="Risk Label",
        title="Fraud Probability Distribution",
        color_discrete_map={
            "Fraud": "red",
            "Genuine": "green"
        }
    )

    fig.update_layout(
        height=450,
        xaxis_title="Fraud Probability",
        yaxis_title="Transaction Count"
    )

    return fig


@app.callback(
    Output("live-alert-ticker", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_live_alert_ticker(n):
    live_df = load_live_predictions()

    alerts = (
        live_df[live_df["Risk Label"] == "Fraud"]
        .sort_values("ID", ascending=False)
        .head(8)
    )

    if alerts.empty:
        return html.Div("✅ No live fraud alerts", style={
            "backgroundColor": "#e8f5e9",
            "padding": "15px",
            "fontWeight": "bold",
            "color": "green"
        })

    return html.Div([
        html.Div(
            f"🚨 {row['Merchant']} | {row['Country']} | {row['Channel']} | £{row['Amount (£)']:,.2f} | Risk: {row['Fraud Probability']:.4f}",
            style={
                "backgroundColor": "#ffe6e6",
                "borderLeft": "6px solid red",
                "padding": "12px",
                "marginBottom": "6px",
                "fontWeight": "bold"
            }
        )
        for _, row in alerts.iterrows()
    ])


@app.callback(
    Output("hourly-fraud-table", "data"),
    Output("hourly-fraud-table", "columns"),
    Input("live-update-interval", "n_intervals")
)
def update_hourly_fraud_table(n):
    live_df = load_live_predictions()

    frauds = live_df[live_df["Risk Label"] == "Fraud"].copy()

    if frauds.empty:
        empty_df = pd.DataFrame(columns=[
            "Hour", "Fraud Count", "Fraud Exposure (£)", "Average Probability"
        ])
        return empty_df.to_dict("records"), [{"name": c, "id": c} for c in empty_df.columns]

    frauds["Created At"] = pd.to_datetime(frauds["Created At"])
    frauds["Hour"] = frauds["Created At"].dt.hour

    hourly_df = (
        frauds.groupby("Hour")
        .agg(
            **{
                "Fraud Count": ("Risk Label", "count"),
                "Fraud Exposure (£)": ("Amount (£)", "sum"),
                "Average Probability": ("Fraud Probability", "mean")
            }
        )
        .reset_index()
        .sort_values("Hour", ascending=False)
    )

    hourly_df["Fraud Exposure (£)"] = hourly_df["Fraud Exposure (£)"].round(2)
    hourly_df["Average Probability"] = hourly_df["Average Probability"].round(4)

    return hourly_df.to_dict("records"), [{"name": c, "id": c} for c in hourly_df.columns]


@app.callback(
    Output("executive-summary-panel", "children"),
    Input("live-update-interval", "n_intervals")
)
def update_executive_summary_panel(n):
    live_df = load_live_predictions()

    total_transactions = len(live_df)
    frauds = live_df[live_df["Risk Label"] == "Fraud"]

    fraud_count = len(frauds)
    genuine_count = total_transactions - fraud_count
    fraud_exposure = frauds["Amount (£)"].sum() if fraud_count > 0 else 0
    avg_probability = frauds["Fraud Probability"].mean() if fraud_count > 0 else 0

    top_country = frauds["Country"].mode()[0] if fraud_count > 0 else "N/A"
    top_merchant = frauds["Merchant"].mode()[0] if fraud_count > 0 else "N/A"
    top_channel = frauds["Channel"].mode()[0] if fraud_count > 0 else "N/A"

    fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0

    return html.Div([
        kpi_card("Total Transactions", f"{total_transactions:,}", "#f8f9fa", "black"),
        kpi_card("Fraud Transactions", f"{fraud_count:,}", "#ffe6e6", "red"),
        kpi_card("Genuine Transactions", f"{genuine_count:,}", "#e8f5e9", "green"),
        kpi_card("Fraud Exposure", f"£{fraud_exposure/1_000_000:.2f}M", "#fff3cd", "#d35400"),
        kpi_card("Fraud Rate", f"{fraud_rate:.2f}%", "#fce4ec", "#b71c1c"),
        kpi_card("Avg Fraud Probability", f"{avg_probability:.4f}", "#ffe6e6", "red"),
        kpi_card("Top Country", top_country, "#f8f9fa", "black"),
        kpi_card("Top Merchant", top_merchant, "#f8f9fa", "black"),
        kpi_card("Top Channel", top_channel, "#f8f9fa", "black"),
    ], style={"textAlign": "center"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)