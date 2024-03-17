# Scindo Delivery

###### - versione di python: 3.8.0
###### - altre dipendenze: [requirements](https://github.com/bizhanzahedi/scindo_final_delivery/blob/main/requirements.txt)
#### il progetto è stato sviluppato per ottenere due api endpoint:

# 1) training pipeline

#### training_pipeline consiste di 3 classi che fanno i prassi della creazione di modelli.
####   - input_controller: controlla l'esistenza e correttezza del file CSV [input](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/input)
####   - input_ingestor: consiste la preparazione di un pandas dataframe pronto per addestrare modelli ML
####   - trainer: addestra e salva i modelli nella cartella [built_models](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/built_models)
####    le metriche reportistiche del modello viene salvato nella cartella [report](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/report) 
####    l'input è un file csv con le seguenti colonne:
    UserID,User_GenericInfo_Birth,User_Job_Education,User_GenericInfo_Address,User_Job_Position,User_GenericInfo_Gender,User_Job_Sector,
    User_Behaviour_Device,User_Finance_TotalLoans_Salary,User_Job_Employed,User_Finance_Balance_Withdrawls,User_Finance_AvarageAccountSpending,
    User_Finance_RID,User_Finance_AvarageCreditSpending,User_Finance_AvarageTransactionsAmount,User_Behaviour_RegistrationDatetime,
    User_Behaviour_OnboardingTime,User_Behaviour_WeeklyVisitNumber,User_Behaviour_Lifetime,User_Finance_TotalLoans_Amount,
    User_Finance_TotalLoans_Number,User_GenericInfo_Type,User_Finance_Balance_Min,User_Finance_Balance_Max,User_Finance_Balance_Avg,
    User_Finance_Cumsum_In,User_Finance_Cumsum_Out,User_Finance_EoP_Loans,User_Finance_EoP_Mortgages,User_Finance_EoP_Deposit,
    User_Finance_EoP_Investments,User_Behaviour_Default


# 2) prediction pipeline
#### prediction pipeline consiste di 3 classi che fanno i prassi dell'utilizzo di modelli.
####   - input_controller: controlla l'esistenza e correttezza delle chiavi e valori del file JSON [input](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/input)
####   - input_ingestor: consiste la preparazione di un JSON pronto per modelli ML e BI
####   - predictor: interroga gli algoritmi di ML ([built_models](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/built_models)), di prior ([prior](https://github.com/bizhanzahedi/scindo_final_delivery/tree/main/prior_default_probability_loans/output_model)), e di BI 

####    l'input è un JSON del tipo:
    {
        "UserID": 1,
        "User": {
            "Behaviour": {
                "Default": false,
                "Device": 1,
                "Lifetime": 20220708,
                "OnboardingTime": 70,
                "RegistrationDatetime": "165353",
                "WeeklyVisitNumber": 1
            },
            "Finance": {
                "AvarageAccountSpending": 1,
                "AvarageCreditSpending": 1,
                "AvarageTransactionsAmount": 1.5,
                "RID" : 1,
                "Balance": {
                    "Avg": 1.5,
                    "Max": 1.5,
                    "Min": 1.5,
                    "Withdrawls": 1.5
                },
                "Cumsum": {
                    "In": 1.5,
                    "Out": 1.5
                },
                "EoP": {
                    "Deposit": 1.5,
                    "Investments": 1.5,
                    "Loans": 1.5,
                    "Mortgages": 1.5
                },
                "TotalLoans": {
                    "Amount": 1.5,
                    "Number": 1,
                    "Salary": false
                }
            },
            "GenericInfo": {
                "Address": 1,
                "Birth": 19900607,
                "Gender": 1,
                "Type": 1
            },
            "Job": {
                "Education": 3,
                "Employed": true,
                "Position": 6,
                "Sector": 18
            }
        }
    }
####    l'output è un JSON del tipo:
    {
        'UserID': 1, 
        'default_probability': 0.0855, 
        'sign': 1
    }

##### sign è la decisione finale aggregata di algoritmi:
     sign =  {
         1 : non erogare il prestito
         0 : puoi erogare il prestito
     }

# nota su input
#### - le attuali pipeline non gestiscono valori NaN.
#### - questo vale sia per il pipeline di prediction che il pipeline di training.
#### - si deve utilizzare un DEFAULT per ogni campo.

# config file
##### config file contiene le variabili utilizzati nelle classi [config](https://github.com/bizhanzahedi/scindo_final_delivery/blob/main/config.py)

##### 1) le mappe:
######   sia il pipeline di training che il pipeline di prediction si aspettano valori codificati per evitare stringhe nelle file CSV e JSON
       map_Address, map_Gender, map_Position, map_Education, map_Sector, map_Device
######   i valori codificati vengono ulteriormente controllati
       encoded_variables


##### 2) le chiavi del JSON:
######   il pipeline di prediction si aspetta chiavi predefiniti, questo viene controllato
       variables_1st_layer, variables_user_layer, variables_behaviour_layer, variables_genericinfo_layer, variables_job_layer
       variables_finance_layer, variables_balance_layer, variables_cumsum_layer, variables_eop_layer, variables_totalloans_layer

##### 3) le colonne del CSV:
######   il pipeline di training si aspetta chiavi predefiniti, questo viene controllato
       all_variables

##### 4) la tipologia dei valori:
######   sia il pipeline di training che il pipeline di prediction si aspettano valori di un certo tipo predefinito, questo viene controllato
       string_variables, int_variables, float_variables, boolean_variables

##### 5) le variabili di natura numericha vengono scalati
       norm_vector

##### 5) le variabili di natura categorica vengono codificati (trasformati in bool)
       one_hot_encode

# ulteriori modifiche all'input:
#### nel caso in cui servisse eliminare un campo di input:
##### 1) si parte con aggiustamento del file config: si elimina (o si commenta) il campo in tutti i dizionari e in tutte le liste
##### 2) si commenta ogni riga del codice sia nel training pipeline che nel prediction pipeline, che contiene quel campo (cerca semplicemente il nome del campo e commenta la riga del codice)
##### 3) avvia il training pipeline (al fine di training si salva i modelli nuovi/giusti)
##### 4) avvia la prediction
       
