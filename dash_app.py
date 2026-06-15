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

    return pd.DataFrame(data)


live_df = load_live_predictions()
live_df["Risk Category"] = live_df["Fraud Probability"].apply(get_risk_category)

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
df = pd.read_csv("dashboard/flagged_transactions.csv")
model_df = pd.read_csv("data/model_comparison.csv")
cm_df = pd.read_csv("data/confusion_matrix_summary.csv")

# KPIs
total_transactions = len(df)
predicted_frauds = int(df["Predicted_Class"].sum())
fraud_rate = (predicted_frauds / total_transactions) * 100
fraud_df = df[df["Predicted_Class"] == 1]
fraud_loss = fraud_df["Amount"].sum()
avg_fraud_amount = fraud_df["Amount"].mean()

# Best model
best_model_row = model_df.sort_values("AUC", ascending=False).iloc[0]
best_model = best_model_row["Model"]

app = Dash(__name__)
app.title = "Credit Card Fraud Detection Dashboard"


def kpi_card(title, value):
    return html.Div([
        html.H4(title),
        html.H2(value)
    ], style={
        "backgroundColor": "#f8f9fa",
        "padding": "20px",
        "borderRadius": "10px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
        "width": "18%",
        "display": "inline-block",
        "margin": "1%"
    })

def fraud_alert_banner(fraud_count, exposure):
    if fraud_count > 0:
        return html.Div(
            [
                html.H2("🚨 HIGH RISK FRAUD ALERT"),
                html.H3(f"{fraud_count} fraud transactions detected"),
                html.P(f"Estimated live fraud exposure: £{exposure:,.2f}")
            ],
            style={
                "backgroundColor": "#ffe6e6",
                "color": "red",
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

    # fraud_alert_banner(live_fraud_count, live_fraud_exposure),


    # html.Div([
    #     kpi_card("Live Fraud Alerts", f"{live_fraud_count:,}"),
    #     kpi_card("Live Genuine Transactions", f"{live_genuine_count:,}"),
    #     kpi_card("Live Fraud Exposure", f"£{live_fraud_exposure:,.2f}"),
    # ], style={"textAlign": "center"}),
    html.Div(id="live-alert-banner"),

    html.Div(id="live-kpi-cards"),

    html.Div(id="risk-category-kpi-cards"),

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

    html.H2("Fraud Prediction Simulator"),

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

    html.H2("Fraud Exposure by Merchant"),

    dcc.Graph(
        figure=px.bar(
        fraud_by_merchant,
        x="Merchant",
        y="Amount (£)",
        title="Fraud Exposure by Merchant",
        text="Amount (£)"
    )
),

html.H2("Fraud Exposure by Country"),

dcc.Graph(
    figure=px.choropleth(
        fraud_by_country,
        locations="Country",
        color="Amount (£)",
        hover_name="Country",
        color_continuous_scale="Reds",
        locationmode="country names",
        title="Fraud Exposure by Country"
    )
),

html.H2("Fraud Exposure by Channel"),

dcc.Graph(
    figure=px.pie(
        fraud_by_channel,
        names="Channel",
        values="Amount (£)",
        title="Fraud Exposure by Channel"
    )
),

# html.H2("Top 10 Highest Risk Transactions"),

# dash_table.DataTable(
#     data=top_risk_transactions.to_dict("records"),
#     columns=[
#         {"name": "ID", "id": "ID"},
#         {"name": "Customer", "id": "Customer"},
#         {"name": "Merchant", "id": "Merchant"},
#         {"name": "Country", "id": "Country"},
#         {"name": "Channel", "id": "Channel"},
#         {"name": "Amount (£)", "id": "Amount (£)"},
#         {"name": "Fraud Probability", "id": "Fraud Probability"},
#         {"name": "Recommended Action", "id": "Recommended Action"},
#         {"name": "Created At", "id": "Created At"},
#     ],
#     page_size=10,
#     style_table={"overflowX": "auto"},
#     style_cell={"textAlign": "center", "padding": "8px"},
#     style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
#     style_data_conditional=[
#         {
#             "if": {"filter_query": "{Risk Label} = 'Fraud'"},
#             "backgroundColor": "#ffe6e6",
#             "color": "red",
#             "fontWeight": "bold",
#         }
#     ],
# ),

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
    
    
#     style_data_conditional=[
#         {
#             "if": {"filter_query": "{Risk Label} = 'Fraud'"},
#             "backgroundColor": "#ffe6e6",
#             "color": "red",
#             "fontWeight": "bold",
#         }
#     ],
# ),

# html.H2("Fraud Trend Over Time"),

# dcc.Graph(
#     figure=px.line(
#         fraud_trend,
#         x="Created At",
#         y="Fraud Count",
#         title="Live Fraud Trend"
#     )
# ),
# html.H2("🌍 Fraud By Country"),

# dcc.Graph(id="fraud-country-chart"),

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
            names="Predicted_Class",
            title="Fraud vs Non-Fraud Transactions",
            color="Predicted_Class",
            color_discrete_map={0: "green", 1: "red"}
        )
    ),

    html.H2("Fraud Amount Distribution"),
    dcc.Graph(
        figure=px.histogram(
            fraud_df,
            x="Amount",
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
        data=fraud_df.sort_values("Amount", ascending=False).head(20).to_dict("records"),
        columns=[
            {"name": "Time", "id": "Time"},
            {"name": "Amount", "id": "Amount"},
            {"name": "Actual Class", "id": "Actual_Class"},
            {"name": "Predicted Class", "id": "Predicted_Class"},
        ],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
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

    sample_transaction["Amount"] = amount

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

    fraud_rate = (
        (live_fraud_count / total_live_transactions) * 100
        if total_live_transactions > 0
        else 0
    )

    banner = fraud_alert_banner(live_fraud_count, live_fraud_exposure)

    cards = html.Div([
        kpi_card("Live Fraud Alerts", f"{live_fraud_count:,}"),
        kpi_card("Live Genuine Transactions", f"{live_genuine_count:,}"),
        kpi_card("Live Fraud Exposure", f"£{live_fraud_exposure:,.2f}"),
        kpi_card("Fraud Rate", f"{fraud_rate:.2f}%"),
    ], style={"textAlign": "center"})

    return banner, cards

@app.callback(
    Output("live-fraud-trend-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_live_fraud_trend(n):
    live_df = load_live_predictions()

    fraud_trend = live_df[live_df["Risk Label"] == "Fraud"].copy()

    fraud_trend["Created At"] = pd.to_datetime(fraud_trend["Created At"])

    fraud_trend = (
        fraud_trend
        .groupby(pd.Grouper(key="Created At", freq="1min"))
        .size()
        .reset_index(name="Fraud Count")
    )

    return px.line(
        fraud_trend,
        x="Created At",
        y="Fraud Count",
        title="Live Fraud Trend Over Time"
    )

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
#     Output("fraud-country-chart", "figure"),
#     Input("live-update-interval", "n_intervals")
# )
# def update_country_chart(n):

#     live_df = load_live_predictions()

#     frauds = live_df[live_df["Risk Label"] == "Fraud"]

#     country_df = (
#         frauds.groupby("Country")
#         .size()
#         .reset_index(name="Fraud Count")
#         .sort_values("Fraud Count", ascending=False)
#     )

#     fig = px.bar(
#         country_df,
#         x="Country",
#         y="Fraud Count",
#         title="Live Fraud Transactions by Country"
#     )

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
        frauds.groupby("Merchant")
        .size()
        .reset_index(name="Fraud Count")
        .sort_values("Fraud Count", ascending=False)
    )

    fig = px.bar(
        merchant_df,
        x="Merchant",
        y="Fraud Count",
        title="Live Fraud Transactions by Merchant"
    )

    return fig

@app.callback(
    Output("fraud-channel-chart", "figure"),
    Input("live-update-interval", "n_intervals")
)
def update_channel_chart(n):

    live_df = load_live_predictions()

    frauds = live_df[
        live_df["Risk Label"] == "Fraud"
    ]

    channel_df = (
        frauds.groupby("Channel")
        .size()
        .reset_index(name="Fraud Count")
    )

    fig = px.pie(
        channel_df,
        names="Channel",
        values="Fraud Count",
        title="Live Fraud by Channel"
    )

    return fig

# @app.callback(
#     Output("live-top-risk-table", "data"),
#     Input("live-update-interval", "n_intervals")
# )
# def update_top_risk_table(n):
#     live_df = load_live_predictions()

#     top_risk = (
#         live_df[live_df["Risk Label"] == "Fraud"]
#         .sort_values("ID", ascending=False)
#         .head(10)
#     )

#     return top_risk.to_dict("records")

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

    country_df = (
        fraud_df
        .groupby("Country")
        .size()
        .reset_index(name="Fraud Count")
        .sort_values("Fraud Count", ascending=False)
    )

    fig = px.bar(
        country_df,
        x="Country",
        y="Fraud Count",
        color="Fraud Count",
        title="Live Fraud By Country"
    )

    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)