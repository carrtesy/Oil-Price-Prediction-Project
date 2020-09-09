import ft

#mode = "daily"
mode = "weekly"
#mode = "monthly"
#mode = "weekly_data+"
#mode = "monthly_data+"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if (mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-08-31')
elif(mode == "weekly"): # Weekly
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    data = ft.readData(monthlyfile, '1946-01-01', '2020-08-01')
elif(mode == "weekly_data+"): # weekly_data+
    print("===WEEKLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')
elif(mode == "monthly_data+"): # weekly_data+
    print("===MONTHLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')


# data에 대하여 E, tau에 따른 smoothness 값 측정
# 이 함수를 실행시키면 폴더에 sm.txt라는 파일이 생성됩니다.
ft.smoothnessMeasure(data, mode)

