
from config import norm_vector, map_Gender, map_Address, map_Device, map_Education, map_Position, map_Sector

import numpy as np
import pandas as pd
import datetime

class train_input_ingestion:

    def __init__(self):    
        
        '''
        questa classe prepara dei DF adatti
        per utilizzare i modelli
        '''

    def japan_date_to_days(self, seires:pd.Series) -> pd.Series:
        
        '''
        questa funzione trasforma le due variabili della data in giornate
        le variabili saranno:
            User_GenericInfo_Birth, User_Behaviour_Lifetime
        
        '''
                
        new_series = pd.Series()

        for idx, value in seires.items():
        
            value = str(value)
            
            year_ = int(value[0:4])
            month_ = int(value[4:6])
            day_ = int(value[6:8])
            
            referencing_date = pd.to_datetime(f"{year_}/{month_}/{day_}")
            now = pd.to_datetime(datetime.datetime.now())

            days = pd.Timedelta(now - referencing_date).days

            new_series.loc[idx] = days

        return new_series

    def japan_datetime_to_hour(self, seires:pd.Series) -> pd.Series:

        '''
        questa funzione trasforma la variabile della ora
        dell'iscrizione in ore 
        le variabili saranno:
            User_Behaviour_RegistrationDatetime
        '''     
           
        new_series = pd.Series()

        for idx, value in seires.items():
        
            value = str(value)
            
            hour_ = int(value[0:2])
            # min_ = int(value[2:4])
            # sec_ = int(value[4:6])
            
            new_series.loc[idx] = hour_

        return new_series

    def normaliser(self, df:pd.DataFrame) -> pd.DataFrame:
        
        '''
        questa funzione normalizza le variabili scalari tra 0 e 1
        le variabili le trova dal file config: 
            norm_vector
        '''

        for idx, row in df.iterrows():

            for variable in norm_vector.keys():
                
                if df.loc[idx, variable] <= norm_vector[variable]["min"] + norm_vector[variable]["eps"]:
                    df.loc[idx, variable] = norm_vector[variable]["min"] + norm_vector[variable]["eps"]

                elif df.loc[idx, variable] > norm_vector[variable]["max"]:
                    df.loc[idx, variable] = norm_vector[variable]["max"]

                df.loc[idx, variable] = np.round((df.loc[idx, variable] - norm_vector[variable]["min"]) / (norm_vector[variable]["max"]), 2)

        return df

    def ml_df_builder(self, df:pd.DataFrame) -> pd.DataFrame:
        
        '''
        questa funzione prepara un DF adatto per costruire
        il modello ML di wealthype
        '''

        df_ml = pd.DataFrame()

        # scale the values
        df = self.normaliser(df)

        df_ml["User_GenericInfo_Birth"] = np.round(self.japan_date_to_days(df["User_GenericInfo_Birth"]) / 365, 0)
        df_ml["User_Job_Education"] = df["User_Job_Education"].map(map_Education)
        df_ml["User_GenericInfo_Address"] = df["User_GenericInfo_Address"].map(map_Address)
        df_ml["User_Job_Position"] = df["User_Job_Position"].map(map_Position)
        df_ml["User_GenericInfo_Gender"] = df["User_GenericInfo_Gender"].map(map_Gender)
        df_ml["User_Job_Sector"] = df["User_Job_Sector"].map(map_Sector)
        df_ml["User_Behaviour_Device"] = df["User_Behaviour_Device"].map(map_Device)
        df_ml["User_Finance_TotalLoans_Salary"] = df["User_Finance_TotalLoans_Salary"]
        df_ml["User_Job_Employed"] = df["User_Job_Employed"]
        df_ml["User_Behaviour_Default"] = df["User_Behaviour_Default"]
        df_ml["User_Finance_Balance_Withdrawls"] = df["User_Finance_Balance_Withdrawls"]
        df_ml["User_Finance_AvarageAccountSpending"] = df["User_Finance_AvarageAccountSpending"]
        df_ml["User_Finance_RID"] = df["User_Finance_RID"]
        df_ml["User_Finance_AvarageCreditSpending"] = df["User_Finance_AvarageCreditSpending"]
        df_ml["User_Finance_AvarageTransactionsAmount"] = df["User_Finance_AvarageTransactionsAmount"]
        df_ml["User_Behaviour_RegistrationDatetime"] = np.round(self.japan_datetime_to_hour(df["User_Behaviour_RegistrationDatetime"]) / 24, 0)
        df_ml["User_Behaviour_OnboardingTime"] = df["User_Behaviour_OnboardingTime"]
        df_ml["User_Behaviour_WeeklyVisitNumber"] = df["User_Behaviour_WeeklyVisitNumber"]
        df_ml["User_Behaviour_Lifetime"] = np.round(self.japan_date_to_days(df["User_Behaviour_Lifetime"]) / 30, 0)
        df_ml["User_Finance_TotalLoans_Amount"] = df["User_Finance_TotalLoans_Amount"]
        df_ml["User_Finance_TotalLoans_Number"] = df["User_Finance_TotalLoans_Number"]
        df_ml["max_min_index"] = np.abs(df["User_Finance_Balance_Max"] - df["User_Finance_Balance_Min"])
        df_ml["income_debt_index"] = df["User_Finance_Cumsum_In"] / (df["User_Finance_EoP_Loans"] + df["User_Finance_EoP_Mortgages"])
        df_ml["wealth_debt_index"] = (df["User_Finance_Balance_Avg"] + df["User_Finance_EoP_Deposit"] + df["User_Finance_EoP_Investments"]) / (df["User_Finance_EoP_Loans"] + df["User_Finance_EoP_Mortgages"])
        df_ml["in_out_index"] = df["User_Finance_Cumsum_In"] / df["User_Finance_Cumsum_Out"]
        df_ml["target"] = df["User_Behaviour_Default"].map(
            {
                False : 0,
                True : 1
            }
        )

        return df_ml