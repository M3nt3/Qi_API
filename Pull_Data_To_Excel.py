def get_sensitivity_grid(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    sensitivity = {}
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
    
#         print("Gathering data for %s from %s to %s..." % (model,
#         date_from,
#         date_to))
    
        sensitivity.update(
        api_instance.get_model_sensitivities(model=model,date_from=date_from,date_to=date_to,term=term))


    #sensitivity = api_instance.get_model_sensitivities(model=model,date_from=start_date,date_to=end_date,term=term)
    
    
    df_sensitivities = pandas.DataFrame()
    sensitivity_grid = pandas.DataFrame()
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

            
    return sensitivity_grid
    
    
    
    
def get_model_data(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series = []
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
    
#         print("Gathering data for %s from %s to %s..." % (model,
#         date_from,
#         date_to))
    
        time_series += api_instance.get_model_timeseries(model=model,date_from=date_from,date_to=date_to,term=term)
    
    # time_series = api_instance.get_model_timeseries(model=model,date_from=start_date,date_to=end_date,term=term)

    FVG = [data.sigma for data in time_series]
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    
    model_value = [data.fair_value for data in time_series]
    percentage_gap = [data.percentage_gap for data in time_series]
    absolute_gap = [data.absolute_gap for data in time_series]
#     target_mean = [data.target_mean for data in time_series]
#     target_stdev = [data.target_stdev for data in time_series]
#     target_zscore = [data.target_zscore for data in time_series]
#     zscore = [data.zscore for data in time_series]


    df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                            'Absolute Gap':absolute_gap})
    df_.index = dates
    
    return df_
     
    
    
    
stocks = sp1500_names
writer = pandas.ExcelWriter('C:/Users/field/OneDrive/QI/S&P1500 api data (5 years).xlsx', engine='openpyxl')
for stock in stocks:
    model_data = get_model_data(stock,'2015-01-01','2019-04-02','Long Term')
    sens_data = get_sensitivity_grid(stock,'2015-01-1','2019-04-02','Long Term')

    model_data.index = [str(x).split(' ')[0] for x in model_data.index]

    df_final = pandas.concat([model_data,sens_data], axis=1, join = 'inner')

    df_final.to_excel(writer, sheet_name = stock)
    writer.save()
    
    print(sp1500_names.tolist().index(stock))
