# Generate html

def generate_html(param):

    style = """
    <style>
    table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 60%;
    }
    td, th {
    border: 1px solid #dddddd;
    text-align: right;
    padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #dddd11;
    }
    </style>
    """

    list_weather = param['weather']
    str_forecast = ''
    for idx, item in enumerate(list_weather):
        str_forecast += ("<tr style=\"background-color: #dddddd\">" if (idx % 2 == 0) else "<tr>") + \
                        "<th>" + item[0] + \
                        "</th><th>" + str(item[1]['min_temp']) + \
                        "</th><th>" + str(item[1]['max_temp']) + \
                        "</th><th>" + item[1]['weather'] + "</th></tr>\n"

    weather_info = '''
    <h2>Weather information</h2>
    <table>
    <caption>Weather forecast of the following 6 days</caption>
    <tr><th>Date</th><th>Min Temp.</th><th>Max Temp.</th><th>Weather</th></tr>
    {forecast}
    </table>
    '''.format(forecast=str_forecast)

    # Food expenses
    df = pd.read_csv(conf.data_path + '/' + 'food_expense', sep='\t')
    cost = round(df['Expense'].sum(), 2)
    days_since_landing = days_between(date_of_landing, date_of_today)
    mail_msg = u"""
    <!DOCTYPE html>
    <html>
    <head>
    {style}
    </head>
    <body>
    <h2>Date information</h2>
    <p>Today is <b>{date}</b>, <b>{week}</b>, the {doy} day in this year.</p>
    <p>This year's progress is as follows: </p>
    <p><font size="4" color="#3498DB" style="line-height:50%">{progress}</font></p>
    <hr />
    {exchange_rate_info}
    <hr />
    <h2>Expenses on food</h2>
    <p>We've landed in Toronto for {dsl} days, and spent ${cost} on food.</p>
    <p>Our average daily expense on food is: <font size="5" color="#E74C3C"> ${cpd} / d </font>.</p>
    <hr />
    {weather_info}
    <hr />
    <h4>This is an automatically generated email, however, you can reply if you insist. To unsubscribe, please discuss with your husband in person.</h4>
    --------------
    <h4>Have a nice day!</h4>
    </body>
    </html>
    """.format(date=date_of_today, week=day_of_week, doy=num2ord(int(day_of_year)),
               weather_info=weather_info, style=style, exchange_rate_info=exchange_rate_info,
               progress=progress_bar, dsl=days_since_landing, cost=cost, cpd=round(float(cost) / days_since_landing, 2))