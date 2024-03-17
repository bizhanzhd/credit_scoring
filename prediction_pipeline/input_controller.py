
from prediction_pipeline.input_ingestor import prediction_input_ingestor
from config import variables_1st_layer, variables_user_layer, variables_behaviour_layer
from config import variables_genericinfo_layer, variables_job_layer, variables_finance_layer
from config import variables_balance_layer, variables_cumsum_layer, variables_eop_layer
from config import variables_totalloans_layer, all_variables, string_variables, int_variables, float_variables, boolean_variables
from config import encoded_variables

import pandas as pd

class prediction_input_controller:

    def __init__(self) -> None:
        
        '''
        questa classe controlla all'ingresso il JSON di Prediction
        - esistenza delle chiavi 
        - correttezza del tipo dei valori
        '''

        self.ingest = prediction_input_ingestor()

    def keys_controller_json(self, initial_body:dict) -> dict:
        
        '''
        la funzione per controllare l'esistenza delle chiavi
        perciò, controlla ogni livello è non accetta mancanza
        di nessun chiave in ingresso.
        le variabili le trova dal file config:
            variables_1st_layer, variables_user_layer, 
            variables_behaviour_layer, variables_genericinfo_layer, 
            variables_job_layer, variables_finance_layer, 
            variables_balance_layer, variables_cumsum_layer, 
            variables_eop_layer, variables_totalloans_layer
        '''

        # control vars
        flag, code, error = False, 200, ""

        # 1)
        for variable in variables_1st_layer:
            
            if not variable in initial_body.keys():
                
                flag, code, error = True, 400, 'variable {} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}
        
        # 2)
        for variable in variables_user_layer:

            if not variable in initial_body["User"].keys():

                flag, code, error = True, 400, 'variable User_{} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 3)
        for variable in variables_behaviour_layer:
            
            if not variable in initial_body["User"]["Behaviour"].keys():
                
                flag, code, error = True, 400, 'variable User_Behaviour_{} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}
        
        # 4)
        for variable in variables_genericinfo_layer:
            
            if not variable in initial_body["User"]["GenericInfo"].keys():
                
                flag, code, error = True, 400, 'variable User_GenericInfo_{} is missing in input, please send a valid request'.format(variable)
   
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 5)
        for variable in variables_job_layer:

            if not variable in initial_body["User"]["Job"].keys():

                flag, code, error = True, 400, 'variable User_Job_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 6)
        for variable in variables_finance_layer:

            if not variable in initial_body["User"]["Finance"].keys():

                flag, code, error = True, 400, 'variable User_Finance_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 7)
        for variable in variables_balance_layer:

            if not variable in initial_body["User"]["Finance"]["Balance"].keys():

                flag, code, error = True, 400, 'variable User_Finance_Balance_{} is missing in input, please send a valid request'.format(variable)
 
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 8)
        for variable in variables_cumsum_layer:

            if not variable in initial_body["User"]["Finance"]["Cumsum"].keys():

                flag, code, error = True, 400, 'variable User_Finance_Cumsum_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 9)
        for variable in variables_eop_layer:

            if not variable in initial_body["User"]["Finance"]["EoP"].keys():

                flag, code, error = True, 400, 'variable User_Finance_EoP_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 10)
        for variable in variables_totalloans_layer:

            if not variable in initial_body["User"]["Finance"]["TotalLoans"].keys():

                flag, code, error = True, 400, 'variable User_Finance_TotalLoans_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def type_check_int(self, body:dict):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere INTEGER
        le variabili le trova dal file config: 
            int_variables
        '''

        # check 
        flag, code, error = False, 200, ""
        
        for variable in int_variables:
            
            x = body[variable]
            if not type(x) in [int]:

                flag, code, error = True, 422, 'variable {} should be a positive integer number, please send a valid request'.format(variable)
                break

            elif x < 0 :
                
                flag, code, error = True, 422, 'variable {} should be a positive integer number, please send a valid request'.format(variable)
                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
        
    def type_check_float(self, body:dict):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere FLOAT ma va bene anche L'INTEGER
        le variabili le trova dal file config: 
            float_variables
        '''
                
        # check
        flag, code, error = False, 200, ""
        for variable in float_variables:
            
            x = body[variable]
            if not type(x) in [int, float]:

                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

            elif x < 0 :
                
                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

        return {"flag" : flag, "response" : error, "response_code" : code}
    
    def type_check_bool(self, body:dict):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere BOOL
        le variabili le trova dal file config: 
            boolean_variables
        '''
  
        # check
        flag, code, error = False, 200, ""
        for variable in boolean_variables:
            x = body[variable]

            if not type(x) in [bool]:

                flag, code, error = True, 422, 'variable {} should be a boolean number, please send a valid request'.format(variable)

                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
        
    def type_check_str(self, body:dict):
        
        '''
        controlla le variabili per cui il tipo di valore presente 
        in JSON deve essere STR
        le variabili le trova dal file config: 
            string_variables
        '''
  
        # check
        flag, code, error = False, 200, ""
        for variable in string_variables:
            x = body[variable]

            if not type(x) in [str]:

                flag, code, error = True, 422, 'variable {} should be a boolean number, please send a valid request'.format(variable)

                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
        
    def value_check_encoded(self, body:dict):
        
        '''
        controlla le variabili che sono codificate
        le variabili le trova dal file config: 
            encoded_variables
        '''
                
        # check
        flag, code, error = False, 200, ""

        for variable, limit in encoded_variables.items():
            
            if body[variable] > limit["upper"] or body[variable] < limit["lower"]:

                flag, code, error = True, 422, '''not expected values for variable {},please send a valid request with an integer number in this range: [{}, {}]'''.format(variable, limit["lower"], limit["upper"])

                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_job(self, body:dict):
        
        '''
        la funzione controlla la variabile User_Job_Employed
        contro la variabile User_Job_Position 
        che devono corrispondere
        '''

        flag, code, error = False, 200, ""

        # check user_job and User_Job_Position
        if body["User_Job_Employed"] == False and body["User_Job_Position"] != 7:

                flag, code, error = True, 422, 'not expected values for variable User_Job_Position, please insert: 7 while User_Job_Employed is false'

                return {"flag" : flag, "response" : error, "response_code" : code}
        
        elif body["User_Job_Employed"] == True and body["User_Job_Position"] == 7:
                
                flag, code, error = True, 422, 'not expected values for variable User_Job_Position, please insert: [1, 6] while User_Job_Employed is True'
                
                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_japan_date_time(self, body:dict):
        
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


        # 1) check User_GenericInfo_Birth, and User_Behaviour_Lifetime
        variables = ["User_GenericInfo_Birth", "User_Behaviour_Lifetime"]
        for variable in variables:
            
            value = str(body[variable])

            if not len(value) == 8:
                
                flag, code, error = True, 422, 'not expected values for variable {}, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[0:4]) > 2022) | (int(value[0:4]) < 1900):
                
                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for year, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[4:6]) > 12) | (int(value[4:6]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for month, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[6:8]) > 31) | (int(value[6:8]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for day, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 2) check User_Behaviour_RegistrationDatetime
        variable = "User_Behaviour_RegistrationDatetime"
        value = str(body[variable])

        if not len(value) == 6:

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a value with 6 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[0:2]) > 24) | (int(value[0:2]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for hours, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[2:4]) > 60) | (int(value[2:4]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for minutes, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[4:6]) > 60) | (int(value[4:6]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for seconds, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}
        
        return {"flag" : flag, "response" : error, "response_code" : code}

    def run(self, body:dict):

        # 0)
        result = self.keys_controller_json(body)
        if result["flag"] == True: return result

        body = self.ingest.body_flatener(body)

        # 2)
        result = self.type_check_int(body)
        if result["flag"] == True: return result

        # 3)
        result = self.type_check_float(body)
        if result["flag"] == True: return result

        # 4)
        result = self.type_check_bool(body)
        if result["flag"] == True: return result

        # 5)
        result = self.type_check_str(body)
        if result["flag"] == True: return result

        # 6)
        result = self.value_check_encoded(body)
        if result["flag"] == True: return result

        # 7)
        result = self.value_check_japan_date_time(body)
        if result["flag"] == True: return result

        # 8)
        result = self.value_check_job(body)
        if result["flag"] == True: return result

        return {"flag" : False, "response" : '', "response_code" : 200}


