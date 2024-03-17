
#######################
# - input maps        #
#######################

map_Address = {
    1 : 'piemonte',
    2 : 'valle daosta',
    3 : 'lombardia',
    4 : 'trentino alto adige',
    5 : 'veneto',
    6 : 'friuli venezia giulia',
    7 : 'liguria',
    8 : 'emilia romagna',
    9 : 'toscana',
    10 : 'umbria',
    11 : 'marche',
    12 : 'lazio',           
    13 : 'abruzzo',
    14 : 'molise',
    15 : 'campania',
    16 : 'puglia',
    17 : 'basilicata',
    18 : 'calabria',
    19 : 'sicilia',
    20 : 'sardegna'
}

map_Gender = {
    1 : "m",
    2 : "f",
    3 : "o"
}

map_Position = {
    1 : "dipendente a tempo determinato",
    2 : "dipendente a tempo indeterminato",
    3 : "imprenditore",
    4 : "libero professionista",
    5 : "consulente con partita IVA",
    6 : "pensionato",
    7 : "non occupato"
}

map_Education = {
    1 : "none",
    2 : "scuola primaria",
    3 : "scuola secondaria di I grado",
    4 : "scuola professionale",
    5 : "scuola secondaria di II grado",
    6 : "laurea",
    7 : "master di II livello e PHD"
}

map_Sector = {
    1 : "istruzione e formazione",
    2 : "industria manufatturiera",
    3 : "banca assicurazione e servizi finanziari",
    4 : "tecnologia",
    5 : "servizi immobiliari",
    6 : "costruzioni",
    7 : "trasporti e logistica",
    8 : "turismo moda sport e tempo libero",
    9 : "consulenza e servizi manageriali",
    10 : "servizi medico sanitari",
    11 : "design architettura e arti creative",
    12 : "forze armate e forze dellordine",
    13 : "commercio al dettaglio",
    14 : "telecomunicazioni energia servizi di pubblica utilità",
    15 : "settore legale",
    16 : "servizi di assistenza sociale",
    17 : "agricoltura, silvicoltura, pesca",
    18 : "commercialisti e fiscalisti",
    19 : "altro"
}

map_Device = {
    1 : "samsung",
    2 : "apple",
    3 : "huawei",
    4 : "xiaomi",
    5 : "oppo",
    6 : "motorola",
    7 : "realme",
    8 : "onepluse",
    9 : "blackview",
    10 : "htc",
    11 : "nothing",
    12 : "razer",
    13 : "asus",
    14 : "acer",
    15 : "altro"
}

#######################
# - prediction JSON   #
#######################

variables_1st_layer = ["UserID", "User"]
variables_user_layer = ["Behaviour", "Finance", "GenericInfo", "Job"]
variables_behaviour_layer = ["Default", "Device", "Lifetime", "OnboardingTime", "RegistrationDatetime", "WeeklyVisitNumber"]
variables_genericinfo_layer = ["Address", "Birth", "Gender", "Type"]
variables_job_layer = ["Education", "Employed", "Position", "Sector"]
variables_finance_layer = ["AvarageAccountSpending", "AvarageCreditSpending", "AvarageTransactionsAmount", "RID", "Balance", "Cumsum", "EoP", "TotalLoans"]
variables_balance_layer = ["Avg", "Max", "Min", "Withdrawls"]
variables_cumsum_layer = ["In", "Out"]
variables_eop_layer = ["Deposit", "Investments", "Loans", "Mortgages"]
variables_totalloans_layer = ["Amount", "Number", "Salary"]


#######################
# - training columns  #
#######################

# all variables: 32
all_variables = [
    "UserID", "User_GenericInfo_Birth", "User_GenericInfo_Address", "User_GenericInfo_Gender", "User_GenericInfo_Type",
    "User_Job_Employed", "User_Job_Sector", "User_Job_Position", "User_Job_Education",
    "User_Behaviour_RegistrationDatetime", "User_Behaviour_OnboardingTime",
    "User_Behaviour_Device", "User_Behaviour_Lifetime", "User_Behaviour_WeeklyVisitNumber", "User_Behaviour_Default",
    "User_Finance_TotalLoans_Number", "User_Finance_TotalLoans_Amount", "User_Finance_TotalLoans_Salary",
    "User_Finance_RID", "User_Finance_AvarageCreditSpending", "User_Finance_AvarageTransactionsAmount",
    "User_Finance_AvarageAccountSpending", "User_Finance_Cumsum_In", "User_Finance_Cumsum_Out",
    "User_Finance_Balance_Avg", "User_Finance_Balance_Min", "User_Finance_Balance_Max", "User_Finance_Balance_Withdrawls",
    "User_Finance_EoP_Deposit", "User_Finance_EoP_Investments", "User_Finance_EoP_Loans", "User_Finance_EoP_Mortgages"
]

# integer variables: 1
string_variables = [
    "User_Behaviour_RegistrationDatetime"
]

# integer variables: 17
int_variables = [
    "UserID", "User_GenericInfo_Address", "User_GenericInfo_Gender", "User_GenericInfo_Type", "User_Job_Sector",
    "User_Job_Position", "User_Job_Education", "User_Behaviour_Device",
    "User_GenericInfo_Birth",  "User_Behaviour_OnboardingTime",
    "User_Behaviour_Lifetime", "User_Behaviour_WeeklyVisitNumber", "User_Finance_TotalLoans_Number", 
    "User_Finance_RID"
]

# float variables: 11
float_variables = [
    "User_Finance_TotalLoans_Amount", "User_Finance_AvarageTransactionsAmount",
    "User_Finance_Cumsum_In", "User_Finance_Cumsum_Out",
    "User_Finance_Balance_Avg", "User_Finance_Balance_Min", "User_Finance_Balance_Max", "User_Finance_Balance_Withdrawls",
    "User_Finance_EoP_Deposit", "User_Finance_EoP_Investments", "User_Finance_EoP_Loans", "User_Finance_EoP_Mortgages",
    "User_Finance_AvarageCreditSpending", "User_Finance_AvarageAccountSpending"
]

# bool variables: 3
boolean_variables = [
    "User_Job_Employed", "User_Behaviour_Default", "User_Finance_TotalLoans_Salary"
]

# encoded variables
encoded_variables = {
    "User_GenericInfo_Address" : {"lower": 1, "upper": 20},
    "User_GenericInfo_Gender" : {"lower": 1, "upper": 3},
    "User_GenericInfo_Type" : {"lower": 1, "upper": 2},
    "User_Job_Sector" : {"lower": 1, "upper": 19},
    "User_Job_Position" : {"lower": 1, "upper": 7},
    "User_Job_Education" : {"lower": 1, "upper": 7},
    "User_Behaviour_Device" : {"lower": 1, "upper": 15}
}

norm_vector = {

    'User_Behaviour_WeeklyVisitNumber' : {"min" : 1, "max" : 20, "eps" : 1},
    'User_Behaviour_OnboardingTime' : {"min" : 1, "max" : 20, "eps" : 1},

    'User_Finance_AvarageCreditSpending' : {"min" : 1, "max" : 100, "eps" : 1},
    'User_Finance_AvarageTransactionsAmount' : {"min" : 10, "max" : 1000, "eps" : 10},
    'User_Finance_AvarageAccountSpending' : {"min" : 1, "max" : 100, "eps" : 1},
    'User_Finance_RID' : {"min" : 1, "max" : 100, "eps" : 1},

    'User_Finance_Cumsum_In' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_Cumsum_Out' : {"min" : 100, "max" : 10000, "eps" : 100},

    'User_Finance_Balance_Min' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_Balance_Max' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_Balance_Avg' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_Balance_Withdrawls' : {"min" : 1, "max" : 20, "eps" : 1},

    'User_Finance_TotalLoans_Amount' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_TotalLoans_Number' : {"min" : 100, "max" : 10000, "eps" : 100},
    
    'User_Finance_EoP_Deposit' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_EoP_Investments' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_EoP_Loans' : {"min" : 100, "max" : 10000, "eps" : 100},
    'User_Finance_EoP_Mortgages' : {"min" : 100, "max" : 100000, "eps" : 100}
}

one_hot_encode = [
    "User_GenericInfo_Address", "User_GenericInfo_Gender", "User_Job_Sector", 
    "User_Job_Position", "User_Job_Education", "User_Behaviour_Device"
]
