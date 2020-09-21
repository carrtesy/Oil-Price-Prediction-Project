import ft

print("=== Smoothness Measure ===")

"""Data Load"""
#mode = "daily"
#mode = "weekly_origin"
#mode = "weekly_tau1"
#mode = "weekly_tau1_for_monthly"
#mode = "monthly"
#mode = "weekly_data+"
mode = "monthly_data+"
print("Loading dataset, mode: ", mode)

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("=== DAILY DATASET ===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')
elif(mode == "weekly_origin"): # Weekly_original
    print("=== WEEKLY DATASET ===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "weekly_tau1"): # Weekly_tau1
    print("=== WEEKLY DATASET ===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "weekly_tau1_for_monthly"): # Weekly_tau1
    print("=== WEEKLY DATASET ===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "monthly"): # Monthly
    print("=== MONTHLY DATASET ===")
    dates, data = ft.readData(monthlyfile, '1986-01-01', '2020-08-01')
elif(mode == "weekly_data+"): # weekly_data+
    print("=== WEEKLY DATASET ===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')
elif(mode == "monthly_data+"): # weekly_data+
    print("=== MONTHLY DATASET ===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')

"""
Smoothness Measure
Creates sm.txt
"""
print("=== Calculating Smoothness Measure ===")
ft.smoothnessMeasure(data, dates, mode)
print("Finished")
