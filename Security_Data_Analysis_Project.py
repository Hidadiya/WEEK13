# Step1 = Create a Security Dataset
import pandas as pd
import matplotlib.pyplot as plt
data = {
    "IP": ["192.168.1.1","192.168.1.2","192.168.1.1","192.168.1.3","192.168.1.2","192.168.1.4"],
    "Status": ["Success","Failed","Failed","Success","Failed","Failed"],
    "Attempts": [1,3,2,1,4,None],
    "Country": ["India","India","India","US","India","UK"]
}
df = pd.DataFrame(data)
# print(df)

# Step2 = Data Cleaning

# Check missing values
# print(df.isnull().sum())

# Fill missing Attempts
df["Attempts"] = df["Attempts"].fillna(df["Attempts"].mean())

# 3. Remove duplicates
df = df.drop_duplicates()

# print(df)

# Step 3 = Analysis

# To find out how many failed logins
failed = df[df["Status"] == "Failed"]
# print(f"There was {len(failed)} failed logins")

# Which IP has most failed attempts?

# print(f"The IP address {failed["IP"].value_counts()} have most failed attempts")

#Average attempts per IP

# print(df.groupby("IP")["Attempts"].mean())

# STEP 4: Visualization


#Chart 1: Login Status Count

# import matplotlib.pyplot as plt

# df["Status"].value_counts().plot(kind="bar")
# plt.title("Login Status Count")
# plt.grid()
# plt.xlabel("Status")
# plt.ylabel("Count")
# plt.show()

# Chart 2: Failed Attempts per IP

# failed["IP"].value_counts().plot(kind="bar")
# plt.title("Failed Attempts per IP")
# plt.xlabel("IP Address")
# plt.ylabel("Count")
# plt.show()

# Chart 3: Average Attempts per IP

avg_attempts = df.groupby("IP")["Attempts"].mean()

avg_attempts.plot(kind="bar")
plt.title("Average Attempts per IP")
plt.xlabel("IP")
plt.ylabel("Attempts")
plt.show()