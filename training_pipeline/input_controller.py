
from training_pipeline.input_ingestor import train_input_ingestion
from config import all_variables, string_variables, int_variables, float_variables, boolean_variables
from config import encoded_variables

import pandas as pd

class train_input_controller:

    def __init__(self) -> None:
        
        '''
        questa classe controlla all'ingresso il DF di Training
        - esistenza delle chiavi 
        - correttezza del tipo dei valori
        '''
                
        self.ingest = train_input_ingestion()

    def keys_controller_dataframe(self, df:pd.DataFrame):
        
        '''
        la funzione per controllare l'esistenza delle chiavi
        perciò, controlla ogni livello è non accetta mancanza
        di nessun chiave in ingresso.
        le variabili le trova dal file config:
            all_variables
        '''
        # check variable presence
        error, flag, code = '', False, 200
        for variable in all_variables:
            if not variable in df.columns:
                error = 'variable {} is missing in input, please send a valid request'.format(variable)
                flag, code = True, 400
                break

        return {"flag" : flag, "response" : error, "response_code" : code}

    def type_check_int(self, df:pd.DataFrame):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere INTEGER
        le variabili le trova dal file config: 
            int_variables
        '''
                
        # check 
        flag, code, error = False, 200, ""

        for variable in int_variables:
            
            if not df[variable].dtype in [int]:

                flag, code, error = True, 422, 'variable {} at {} should be a positive integer number, please send a valid request'.format(variable, df[variable][0])
                break

            elif df[variable].min() < 0 :
                
                flag, code, error = True, 422, 'variable {} at {} should be a positive integer number, please send a valid request'.format(variable, df[variable][0])
                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
        
    def type_check_float(self, df:pd.DataFrame):

        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere FLOAT ma va bene anche L'INTEGER
        le variabili le trova dal file config: 
            float_variables
        '''

        # check
        flag, code, error = False, 200, ""
        for variable in float_variables:
            
            if not df[variable].dtype in [int, float]:

                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

            elif df[variable].min() < 0 :
                
                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

        return {"flag" : flag, "response" : error, "response_code" : code}
    
    def type_check_bool(self, df:pd.DataFrame):

        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere BOOL
        le variabili le trova dal file config: 
            boolean_variables
        '''

        # check
        flag, code, error = False, 200, ""
        for variable in boolean_variables:

            if not df[variable].dtype in [bool]:

                flag, code, error = True, 422, 'variable {} should be a boolean number, please send a valid request'.format(variable)
                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}

    def type_check_str(self, df:pd.DataFrame):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere STR
        le variabili le trova dal file config: 
            string_variables
        '''
  
        # check
        flag, code, error = False, 200, ""
        for variable in string_variables:

            if not df[variable].dtype in ['O', int]:

                flag, code, error = True, 422, 'variable {} should be a string, please send a valid request'.format(variable)

                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
       
    def value_check_encoded(self, df:pd.DataFrame):
        
        '''
        controlla le variabili che sono codificate
        le variabili le trova dal file config: 
            encoded_variables
        '''
              
        # check
        flag, code, error = False, 200, ""
        
        for variable, limit in encoded_variables.items():
            
            if df[variable].any() > limit["upper"] or df[variable].any() < limit["lower"]:

                flag, code, error = True, 422, '''not expected values for variable {},please send a valid request with an integer number in this range: [{}, {}]'''.format(variable, limit["lower"], limit["upper"])

                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_job(self, df:pd.DataFrame):

        '''
        la funzione controlla la variabile User_Job_Employed
        contro la variabile User_Job_Position 
        che devono corrispondere
        '''

        flag, code, error = False, 200, ""

        # check user_job and User_Job_Position

        for idx, row in df.iterrows():
            if df.loc[idx, "User_Job_Employed"] == False and df.loc[idx, "User_Job_Position"] != 7:

                flag, code, error = True, 422, f'not expected values for variable User_Job_Position at {idx}, please insert: 7 while User_Job_Employed is false'

                return {"flag" : flag, "response" : error, "response_code" : code}
            
            elif df.loc[idx, "User_Job_Employed"] == True and df.loc[idx, "User_Job_Position"] == 7:
                    
                flag, code, error = True, 422, f'not expected values for variable User_Job_Position at {idx}, please insert: [1, 6] while User_Job_Employed is True'
                
                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_japan_date_time(self, df:pd.DataFrame):

        '''
        controlla la correttezza delle variabili datetime
        in formato GIAPPONESE
        
        il valore di: 
            User_GenericInfo_Birth, User_Behaviour_Lifetime
        deve essere un INTEGER del genere:
            yyyymmdd

        il valore di: 
            User_Behaviour_RegistrationDatetime
        deve essere un STRING del genere:
            hhmmss
        '''
   
        flag, code, error = False, 200, ""

        for idx, row in df.iterrows():

            # 1) check User_GenericInfo_Birth, and User_Behaviour_Lifetime
            variables = ["User_GenericInfo_Birth", "User_Behaviour_Lifetime"]

            for variable in variables:
                
                value = str(df.loc[idx, variable])

                if not len(value) == 8:
                    
                    flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708, seen lenght: {}'.format(variable, idx, len(value))

                    return {"flag" : flag, "response" : error, "response_code" : code}

                elif (int(value[0:4]) > 2030) | (int(value[0:4]) < 1900):
                    
                    flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for year, please insert a value with 8 numeric characters, representing (year, month, day), the year shold look like: 1980'.format(variable, idx)

                    return {"flag" : flag, "response" : error, "response_code" : code}

                elif (int(value[4:6]) > 12) | (int(value[4:6]) < 1):

                    flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for month, please insert a value with 8 numeric characters, representing (year, month, day), the month should look like: 07'.format(variable, idx)

                    return {"flag" : flag, "response" : error, "response_code" : code}

                elif (int(value[6:8]) > 31) | (int(value[6:8]) < 1):

                    flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for day, please insert a value with 8 numeric characters, representing (year, month, day), the day should look like: 08'.format(variable, idx)

                    return {"flag" : flag, "response" : error, "response_code" : code}

            # 2) check User_Behaviour_RegistrationDatetime
            variable = "User_Behaviour_RegistrationDatetime"

            value = str(df.loc[idx, variable])

            if not len(value) == 6:

                flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a value with 6 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable, idx)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[0:2]) > 24) | (int(value[0:2]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for hours, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable, idx)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[2:4]) > 60) | (int(value[2:4]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for minutes, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable, idx)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[4:6]) > 60) | (int(value[4:6]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {} at {}, please insert a correct value for seconds, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable, idx)

                return {"flag" : flag, "response" : error, "response_code" : code}
            
        return {"flag" : flag, "response" : error, "response_code" : code}

    def run(self, df:pd.DataFrame):

        # 0)
        result = self.keys_controller_dataframe(df)
        if result["flag"] == True: return result

        # 2)
        result = self.type_check_int(df)
        if result["flag"] == True: return result

        # 3)
        result = self.type_check_float(df)
        if result["flag"] == True: return result

        # 4)
        result = self.type_check_bool(df)
        if result["flag"] == True: return result

        # 5)
        result = self.type_check_str(df)
        if result["flag"] == True: return result

        # 6)
        result = self.value_check_encoded(df)
        if result["flag"] == True: return result

        # 7)
        result = self.value_check_japan_date_time(df)
        if result["flag"] == True: return result

        # 8)
        result = self.value_check_job(df)
        if result["flag"] == True: return result

        return {"flag" : False, "response" : '', "response_code" : 200}


