#######################################################################################################################################
# 
# This function finds the Qi model names associated with your Bloomberg tickers.
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         tickers - e.g. ['AAPL US Equity', 'FB US Equity', 'GOOG US Equity']
#
# Output: 
#         dataframe with the following columns:
#               * Tickers - dataframe index. 
#               * Qi Model Name. 
#               * e.g.
#
#                |                | Qi Model Name |
#                | AAPL US Equity |        AAPL   | 
#                | FB US Equity   |          FB   | 
#                | GOOG US Equity |        GOOG   | 
#
#######################################################################################################################################


def get_model_names_from_tickers(tickers):

    ### Load US Models from API

    API_US = [x.name for x in api_instance.get_models(tags='USD')][::2]


    ### Load other Models from API

    API_other = [x.name for x in api_instance.get_models()][::2]
    [API_other.remove(model) for model in API_US if model in API_other]
    
    potential_models = [model for model in API_other if model.split(' ')[0] in [x.split(' ')[0] for x in tickers]]
    potential_tickers = [api_instance.get_model(model).definition.timeseries_ety1.instrument.identifiers['BloombergTicker'] for model in potential_models]

    model_names = []

    for ticker in tickers:

        ### Check US tickers

        if any([x in ticker for x in [' US ',' UN ',' UW ']]):

            temp_model = ticker.split(' ')[0]

            if temp_model in API_US:
                model_names.append(temp_model)

            elif temp_model + ' US' in API_US:
                model_names.append(temp_model + ' US')
                
            elif ticker in potential_tickers:
                idx = potential_tickers.index(ticker)
                model_names.append(potential_models[idx])

            else:
                model_names.append(None)



        ### Check other tickers

        else:
            
            ### Adjust German & Japan Tickers
            
            if ' GR ' in ticker:
                temp_ticker = ticker.replace(' GR ',' GY ')
                
            elif ' JP ' in ticker:
                temp_ticker = ticker.replace(' JP ',' JT ')
                
            else:
                temp_ticker = ticker


            if temp_ticker in potential_tickers:
                idx = potential_tickers.index(temp_ticker)
                model_names.append(potential_models[idx])

            else:

                model_names.append(None)
                
    return pandas.DataFrame(model_names,tickers, columns = ['Qi Model Name'])
