# Qi API

This repository includes some examples of how to use Quant-Insight's API. 

It contains five main folders:

  * 1.Built_In_Functions: contains the API's built-in functions.
  * 2.Pull_Data: contains useful examples of how to pull the data from Qi's database. 
  * 3.Use_Cases: examples of how Qi data is used.
  * 4.Macro Risk: a comprehensive guide on how to calculate your portfolio's macro risk.
  * 5.Case Studies: contains examples of how Qi uses the API.

## What do you need to start using the API?

* Client Download Token

  * This will be unique to your organisation and is required in order to install the Qi Client. 

* API key

  * If you still don't have an API key, you can contact Quant-Insight. 
  
  * If you already have an API key:
          
          * Install QI client, with your TOKEN instead of DLTOKEN (Note that to install packages on 
          Jupyter Notebooks you need to use !pip install instead of pip install):

                !pip install matplotlib pandas

                !pip install \
                --upgrade \
                --extra-index-url=https://dl.cloudsmith.io/DLTOKEN/quant-insight/python/python/index/ \
                qi-client
               
           * Insert the following piece of code at the start of your script, with your API key instead 
           of 'ADD-YOUR-API-KEY-HERE': 

                import pandas
                import qi_client
                from qi_client.rest import ApiException

                configuration = qi_client.Configuration()

                configuration.api_key['X-API-KEY'] = 'ADD-YOUR-API-KEY-HERE'

                api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))


## How to use Qi wrapper?

* You need to have the library retrying installed:

         !pip install retrying
 
* Download the Qi_wrapper.py file and save it in the same folder your Python files are usually saved. 

* As we did it previously, it is necessary to declare your API Key to use our functions. However, when using the wrapper you will need to declare it just before importing it as follows:

  * If you are using Jupyter Notebooks:
  
         %set_env QI_API_KEY = ADD-YOUR-API-KEY-HERE (Make sure the API key is written without '') 
         import Qi_wrapper
       
  * If you are using regular python IDE: 
  
         import os
         import subprocess
         import sys

         os.environ['QI_API_KEY'] = 'ADD-YOUR-API-KEY-HERE'

         import Qi_wrapper

  * Now you can use all our use case functions as follows: 
                        <br>
                        <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/api_wrapper_functions.png" alt="QI Use Case Functions"/>
                        </br>
