from config import norm_vector, map_Gender, map_Address, map_Device, map_Education, map_Position, map_Sector

import numpy as np
import datetime

class prediction_input_ingestor:

    def __init__(self):      
        
        '''
        questa classe prepara dei JSON adatti
        per utilizzare i modelli
        '''

        self.date = datetime.datetime.now()
    
    def body_flatener(self, initial_body:dict) -> dict:

        '''
        questa funzione crea un JSON appiattito
        dal JSON in albero
        '''

        flatened_body = {
            "UserID" : initial_body["UserID"],
            "User_GenericInfo_Birth" : initial_body["User"]["GenericInfo"]["Birth"],
            "User_Job_Education" : initial_body["User"]["Job"]["Education"],
            "User_GenericInfo_Address" : initial_body["User"]["GenericInfo"]["Address"],
            "User_Job_Position" : initial_body["User"]["Job"]["Position"],
            "User_GenericInfo_Gender" : initial_body["User"]["GenericInfo"]["Gender"],
            "User_Job_Sector" : initial_body["User"]["Job"]["Sector"],
            "User_GenericInfo_Type" : initial_body["User"]["GenericInfo"]["Type"],
            "User_Behaviour_Device" : initial_body["User"]["Behaviour"]["Device"],

            "User_Finance_TotalLoans_Salary" : initial_body["User"]["Finance"]["TotalLoans"]["Salary"],
            "User_Job_Employed" : initial_body["User"]["Job"]["Employed"],
            "User_Behaviour_Default" : initial_body["User"]["Behaviour"]["Default"],

            "User_Finance_Balance_Withdrawls" : initial_body["User"]["Finance"]["Balance"]["Withdrawls"],
            "User_Finance_AvarageAccountSpending" : initial_body["User"]["Finance"]["AvarageAccountSpending"],
            "User_Finance_RID" : initial_body["User"]["Finance"]["RID"],
            "User_Finance_AvarageCreditSpending" : initial_body["User"]["Finance"]["AvarageCreditSpending"],
            "User_Finance_AvarageTransactionsAmount" : initial_body["User"]["Finance"]["AvarageTransactionsAmount"],
            "User_Behaviour_RegistrationDatetime" : initial_body["User"]["Behaviour"]["RegistrationDatetime"],
            "User_Behaviour_OnboardingTime" : initial_body["User"]["Behaviour"]["OnboardingTime"],
            "User_Behaviour_WeeklyVisitNumber" : initial_body["User"]["Behaviour"]["WeeklyVisitNumber"],
            "User_Behaviour_Lifetime" : initial_body["User"]["Behaviour"]["Lifetime"],
            "User_Finance_TotalLoans_Amount" : initial_body["User"]["Finance"]["TotalLoans"]["Amount"],
            "User_Finance_TotalLoans_Number" : initial_body["User"]["Finance"]["TotalLoans"]["Number"],
            
            "User_Finance_Balance_Max" : initial_body["User"]["Finance"]["Balance"]["Max"],
            "User_Finance_Balance_Min" : initial_body["User"]["Finance"]["Balance"]["Min"],
            "User_Finance_Balance_Avg" : initial_body["User"]["Finance"]["Balance"]["Avg"],
            "User_Finance_Cumsum_In" : initial_body["User"]["Finance"]["Cumsum"]["In"],
            "User_Finance_Cumsum_Out" : initial_body["User"]["Finance"]["Cumsum"]["Out"],

            "User_Finance_EoP_Loans" : initial_body["User"]["Finance"]["EoP"]["Loans"],
            "User_Finance_EoP_Mortgages" : initial_body["User"]["Finance"]["EoP"]["Mortgages"],
            "User_Finance_EoP_Deposit" : initial_body["User"]["Finance"]["EoP"]["Deposit"],
            "User_Finance_EoP_Investments" : initial_body["User"]["Finance"]["EoP"]["Investments"]  
        }

        return flatened_body

    def japan_date_to_days(self, date_int:int) -> int:
        
        '''
        questa funzione trasforma le due variabili della data in giornate
        le variabili saranno:
            User_GenericInfo_Birth, User_Behaviour_Lifetime
        
        '''

        date_int = str(date_int)
        year_ = int(date_int[0:4])
        month_ = int(date_int[4:6])
        day_ = int(date_int[6:8])

        year = (self.date.year - year_) * 365
        month = (self.date.month - month_) * 30
        day = (self.date.day - day_)
        total_days = year + month + day

        return total_days

    def japan_datetime_to_hour(self, value:str) -> int:

        '''
        questa funzione trasforma la variabile della ora
        dell'iscrizione in ore 
        le variabili saranno:
            User_Behaviour_RegistrationDatetime
        ''' 

        value = str(value)
        
        hour_ = int(value[0:2])
        # min_ = int(value[2:4])
        # sec_ = int(value[4:6])

        return hour_

    def normaliser(self, body:dict) -> dict:

        '''
        questa funzione normalizza le variabili scalari tra 0 e 1
        le variabili le trova dal file config: 
            norm_vector
        '''
        
        for variable in norm_vector.keys():
            if body[variable] <= norm_vector[variable]["min"] + norm_vector[variable]["eps"]:
                body[variable] = norm_vector[variable]["min"] + norm_vector[variable]["eps"]

            elif body[variable] > norm_vector[variable]["max"]:
                body[variable] = norm_vector[variable]["max"]

            body[variable] = np.round((body[variable] - norm_vector[variable]["min"]) / (norm_vector[variable]["max"]), 2)

        return body

    def prior_body_builder(self, body:dict) -> dict:

        '''
        questa funzione prepara un JSON adatto per interrogare
        il modello addestrato sui dati pubblici (Banca d'italia)
        i documenti e il codice sono presenti nella cartella:
            /prior_default_probability_loans
        '''
                
        body_prior = {
            "age_id" : np.round(self.japan_date_to_days(body["User_GenericInfo_Birth"]) / 365, 2),
            "region_id" : body["User_GenericInfo_Address"],
            "gender_id" : body["User_GenericInfo_Gender"],
            "profession_id" : body["User_Job_Position"],
            "education_id" : body["User_Job_Education"]
        }

        return body_prior

    def scorecard_body_builder(self, body:dict) -> dict:

        '''
        questa funzione prepara un JSON adatto per interrogare
        il modello BI di wealthype
        '''
        
        body_scorecard = {
            "User_Job_Employed" : body["User_Job_Employed"],
            "User_Job_Position" : body["User_Job_Position"],
            "User_Finance_Cumsum_Out" : body["User_Finance_Cumsum_Out"],
            "User_Finance_Balance_Avg" : body["User_Finance_Balance_Avg"],
            "User_Finance_TotalLoans_Number" : body["User_Finance_TotalLoans_Number"],
            "User_Finance_TotalLoans_Salary" : body["User_Finance_TotalLoans_Salary"],
            "User_Finance_RID" : body["User_Finance_RID"],
            "User_Behaviour_Default" : body["User_Behaviour_Default"],
            "User_Finance_EoP_Loans": body["User_Finance_EoP_Loans"],
            "User_Finance_EoP_Mortgages": body["User_Finance_EoP_Mortgages"],
            "User_Finance_EoP_Deposit": body["User_Finance_EoP_Deposit"],
            "User_Finance_EoP_Investments": body["User_Finance_EoP_Investments"]
        }

        return body_scorecard

    def ml_body_builder(self, body:dict) -> dict:
        
        '''
        questa funzione prepara un JSON adatto per interrogare
        il modello ML di wealthype
        '''

        # scale the values
        body = self.normaliser(body)

        body_ml = {
            "User_GenericInfo_Birth" : np.round(self.japan_date_to_days(body["User_GenericInfo_Birth"]) / 365, 2),
            "User_Job_Education" : map_Education[body["User_Job_Education"]],
            "User_GenericInfo_Address" : map_Address[body["User_GenericInfo_Address"]],
            "User_Job_Position" : map_Position[body["User_Job_Position"]],
            "User_GenericInfo_Gender" : map_Gender[body["User_GenericInfo_Gender"]],
            "User_Job_Sector" : map_Sector[body["User_Job_Sector"]],
            "User_Behaviour_Device" : map_Device[body["User_Behaviour_Device"]],

            "User_Finance_TotalLoans_Salary" : body["User_Finance_TotalLoans_Salary"],
            "User_Job_Employed" : body["User_Job_Employed"],
            "User_Behaviour_Default" : body["User_Behaviour_Default"],

            "User_Finance_Balance_Withdrawls" : body["User_Finance_Balance_Withdrawls"],
            "User_Finance_AvarageAccountSpending" : body["User_Finance_AvarageAccountSpending"],
            "User_Finance_RID" : body["User_Finance_RID"],
            "User_Finance_AvarageCreditSpending" : body["User_Finance_AvarageCreditSpending"],
            "User_Finance_AvarageTransactionsAmount" : body["User_Finance_AvarageTransactionsAmount"],
            "User_Behaviour_RegistrationDatetime" : np.round(self.japan_datetime_to_hour(body["User_Behaviour_RegistrationDatetime"]) / 24, 0),
            "User_Behaviour_OnboardingTime" : body["User_Behaviour_OnboardingTime"],
            "User_Behaviour_WeeklyVisitNumber" : body["User_Behaviour_WeeklyVisitNumber"],
            "User_Behaviour_Lifetime" : np.round(self.japan_date_to_days(body["User_Behaviour_Lifetime"]) / 30, 2),
            "User_Finance_TotalLoans_Amount" : body["User_Finance_TotalLoans_Amount"],
            "User_Finance_TotalLoans_Number" : body["User_Finance_TotalLoans_Number"],
            
            "max_min_index" : np.abs(body["User_Finance_Balance_Max"] - body["User_Finance_Balance_Min"]),
            "income_debt_index" : body["User_Finance_Cumsum_In"] / (body["User_Finance_EoP_Loans"] + body["User_Finance_EoP_Mortgages"]),
            "wealth_debt_index" : (body["User_Finance_Balance_Avg"] + body["User_Finance_EoP_Deposit"] + body["User_Finance_EoP_Investments"]) / (body["User_Finance_EoP_Loans"] + body["User_Finance_EoP_Mortgages"]),
            "in_out_index" : body["User_Finance_Cumsum_In"] / body["User_Finance_Cumsum_Out"]
        }

        return body_ml