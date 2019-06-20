# Use-Case Functions

## Description

This function creates a portfolio of European stocks based on sensitivities to a given factor. 

**Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** factor - 'factor' (e.g. 'ADXY')
            size - number of stocks to be in resulting portfolio (e.g. 10)
            date - 'date' (e.g. '2019-05-17')
            term - 'term' (e.g. 'Long Term')
               
**Output:** dataframe with the following columns:
            * Position - dataframe index. 
            * Name - top 5 factor drivers' names. 
            * Weight - weights of the top 5 factor drivers.
            * Factor Sensitivity - Factor top 5 drivers' sensitivity.

## Code

```python
import qi_client
import pandas
from datetime import datetime

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

#################################################################################################################
#                                                      Functions
#################################################################################################################
# 
# This function retrieves the buckets' sensitivities for a given model, a given date and a given model term. 
def get_portfolio(factor,size,date,term):

    FACTOR_sensitivity = []
    names = []
    POSITION = []

    # Get ID's of the Euro Stoxx 600 Stocks.
    # Stocks can be changed by specifying another stock's tag. 
    euro_stoxx_600 = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::2]

    for asset in euro_stoxx_600:

        sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

        df_sensitivities = pandas.DataFrame()

        if len(sensitivity) > 0:
            date = [x for x in sensitivity][0]

            for data in sensitivity[date]:
                df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]
            # We want the top 5 drivers in absolute terms. 
            top5 = abs(df_sensitivities).T.nlargest(5,0)
            Factor_sens = float(df_sensitivities[factor])

            if factor in top5.index:
                FACTOR_sensitivity.append(Factor_sens)
                names.append(asset)
                position = top5.index.tolist().index(factor)+1
                POSITION.append(position)

    df_factor_sensit = pandas.DataFrame({'Name':names,'Position':POSITION,factor+' Sensitivity':FACTOR_sensitivity})
    portfolio = df_factor_sensit.nlargest(size,str(factor)+' Sensitivity')

    sw = 1/(portfolio['Position']+2)
    Weights = sw/sw.sum()

    portfolio = portfolio.drop(['Position'], axis=1)
    portfolio.insert(1,'Weight',Weights)
    
    return portfolio
    
    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

get_portfolio(factor = 'ADXY', size = 10, date = '2019-05-17', term = 'Long Term')
```

## Output

|    | Name | Weight    | ADXY Sensitivity |
|----|:----:|:---------:|:----------------:| 
| 18 | ENEL | 0.108527  | 0.12556          |
| 27 | GET  | 0.077519  | 0.12079          |
| 71 | VIE  | 0.108527  | 0.11375          |
| 67 | TEL  | 0.090439  | 0.11198          |
| 5  | ATL  | 0.108527  | 0.10966          |
| 2  | ALT  | 0.108527  | 0.10409          |
| 53 | RHM  | 0.090439  | 0.10178          |
| 1  | AENA | 0.108527  | 0.10067          |
| 62 | SGRE | 0.090439  | 0.10050          |
| 40 | LOOMB| 0.108527  | 0.09925          |
