import pandas as pd
import matplotlib.pyplot as plt
import folium
import os

# Load dataset
file_path = "data/flood_data.csv"
df = pd.read_csv(file_path)

# Flood Risk Logic
def flood_risk(row):
    if row["Rainfall_mm"] > 120 or row["River_Level_m"] > 5:
        return "High Risk"
    elif row["Rainfall_mm"] > 70:
        return "Moderate Risk"
    else:
        return "Low Risk"

df["Flood_Risk"] = df.apply(flood_risk, axis=1)

print("\nFlood Risk Analysis by District\n")
print(df)

# Create output folder
os.makedirs("output", exist_ok=True)

# Graph 1: Rainfall by District
plt.figure()

district_rainfall = df.groupby("District")["Rainfall_mm"].mean()

district_rainfall.plot(kind="bar")

plt.title("Average Rainfall by District")
plt.xlabel("District")
plt.ylabel("Rainfall (mm)")

plt.savefig("output/rainfall_by_district.png")
plt.show()

# Graph 2: River Level Trend
plt.figure()

plt.plot(df["Date"], df["River_Level_m"], marker="o")

plt.title("River Level Trend")
plt.xlabel("Date")
plt.ylabel("River Level (m)")
plt.xticks(rotation=45)

plt.savefig("output/river_level_trend.png")
plt.show()

print("\nGraphs saved in output folder.")



# District coordinates (example)
district_coords = {
    "Saharsa": [25.88, 86.60],
    "Supaul": [26.12, 86.60],
    "Madhepura": [25.92, 86.79]
}

# Create map centered in Bihar
map = folium.Map(location=[25.9, 86.7], zoom_start=8)

# Add markers
for index, row in df.iterrows():

    district = row["District"]
    risk = row["Flood_Risk"]

    if district in district_coords:

        color = "green"

        if risk == "Moderate Risk":
            color = "orange"
        elif risk == "High Risk":
            color = "red"

        folium.CircleMarker(
            location=district_coords[district],
            radius=10,
            popup=f"{district} - {risk}",
            color=color,
            fill=True
        ).add_to(map)

# Save map
map.save("output/flood_risk_map.html")

print("Map saved in output folder.")