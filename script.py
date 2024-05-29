import requests
import json 
import time

# This is our workspaces in Grafana and we need to generate keys for each workspace
workspaces = [
    {"url": "http://grafana-workspace.us-east-1.amazonaws.com/", "api_key": "API_KEY_1"},
    {"url": "http://grafana-workspace.us-east-1.amazonaws.com/", "api_key": "API_KEY_2"},
]

def format_alerts_for_dashboard(alerts):
    # This function will format the alerts in a way that we can display them in a dashboard
    # Based on our keys in the alerts the alert keys will change accordingly
    rows = []
    for alert in alerts:
        rows.append([
            alert['name'],
            alert['state'],
            alert.get["severity", "N/A"],
            alert['workspace'],
        ])
        
    return rows

# Fetch alerts from workspaces and using example data for now
def fetch_alerts():
    all_alerts = []
    for workspace in workspaces:
        headers = {
            "Authorization": f"Bearer{workspace['api_key']}"
        }
        response = requests.get(workspace['url'], headers=headers)
        if response.status_code == 200:
            alerts = response.json()
            for alert in alerts:
                alert['workspace'] = workspace['url']
            all_alerts.extend(alerts)
        else:
            print(f"Failed to fetch alerts from {workspace['url']}: {response.status_code}")
    return all_alerts

def update_dashboard_with_alerts(alerts):
# Read dashboard JSON here
    with open("dashboard_template.json", "r") as file:
        dashboard = json.load(file)
    
# Update the dashboard with the alerts
    dashboard["dashboard"]["panels"][0]["options"]["data"]["rows"] = format_alerts_for_dashboard(alerts)

# Write updated dashboard JSON
    with open("dashboard_with_alerts.json", "w") as file:
        json.dump(dashboard, file, indent=2)
        
    return dashboard

# Push the updated dashboard to Grafana    
def push_dashboard_to_grafana(dashboard_json):
    url = "http://grafana-workspace.us-east-1.amazonaws.com/api/dashboards/db"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer OUR_MAIN_GRAFANA_API_KEY"
    }
    response = requests.post(url, headers=headers, data=json.dumps(dashboard_json))
    if response.status_code == 200:
        print("Dashboard updated successfully")
    else:
        print(f"Failed to update dashboard: {response.status_code}")
        
def main():
    alerts = fetch_alerts()
    dashboard_json = update_dashboard_with_alerts(alerts)
    push_dashboard_to_grafana(dashboard_json)
    time.sleep(300)
    
if __name__ == "__main__":
    main()