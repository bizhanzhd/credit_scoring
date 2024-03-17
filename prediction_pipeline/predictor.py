import pickle
import numpy as np
import pandas as pd
from prediction_pipeline.input_ingestor import prediction_input_ingestor
from config import one_hot_encode
import json
class predictor:

    def __init__(self):

        '''
        questa classe interroga i diversi algoritmi 
        utilizzando i JSON preparati in input_ingestion
        il run della classe aggrega la predizione
        di tutti i modelli
        '''

        # make ingestion object
        self.ingest = prediction_input_ingestor()

        # read model of prior
        self.prior_model = pickle.load(open('prior_default_probability_loans/output_model/prior_p_regressor.pkl', 'rb'))

        # read ml model: Complement NB
        self.cnb = pickle.load(open('built_models/model_complement_naive_bayes.pkl', 'rb'))

        # read ml model: SVC
        self.svc = pickle.load(open('built_models/model_svc.pkl', 'rb'))

        # read ml model: Logistic Regression
        self.lr = pickle.load(open('built_models/model_logistic_regression.pkl', 'rb'))

        # read ml model: Isolation Forest
        self.isf = pickle.load(open('built_models/model_isolation_forest.pkl', 'rb'))

        # read ml model: Oneclass svm
        self.ocs = pickle.load(open('built_models/model_oneclass_svm.pkl', 'rb'))

        # read the Encoder
        self.encoder = pickle.load(open("built_models/encoder.pkl", 'rb'))

    def build_beta_binomial_distribution(self, sample_mean:float, sample_power:int) -> list:
        
        '''
        questa funzione intende a creare una distribuzione beta binomiale
        da un valore e una deviazione standard predefinito,
        preparandola per l'aggregazione
        '''
        
        alpha = sample_power * sample_mean
        beta = sample_power - alpha
        return [alpha, beta]

    def prior_calculator(self, data:dict) -> float:
        
        '''
        questa funzione interroga il modello addestrato 
        sui dati pubblici (Banca d'italia)
        i documenti e il codice sono presenti nella cartella:
            /prior_default_probability_loans
        '''
        
        age = data["age_id"]
        gender = data["gender_id"]
        location = data["region_id"]
        profession = data["profession_id"]
        education = data["education_id"]

        # prior:
        X = pd.DataFrame( [(age, gender, location, education, profession)],
            columns=["age_id", "gender_id", "region_id", "education_id", "profession_id"])
        prior = self.prior_model.predict(X)

        max_prior = 0.062
        prior = prior[0] / max_prior

        print("Prior: ", prior)
        return prior

    def score_calculator(self, data:dict) -> float:

        '''
        questa funzione interroga il modello BI costruito da wealthype
        '''

        # anagraphical data
        job = data["User_Job_Employed"]
        profession = data["User_Job_Position"]
        
        # transactional data
        outflow = data["User_Finance_Cumsum_Out"]
        avg_balance = data["User_Finance_Balance_Avg"]
        salary_on_acc = data["User_Finance_TotalLoans_Salary"]
        active_rids = data["User_Finance_RID"]
        deposits = data["User_Finance_EoP_Deposit"]
        investments = data["User_Finance_EoP_Investments"]
        other_loans = data["User_Finance_EoP_Loans"]
        other_mortgages = data["User_Finance_EoP_Mortgages"]

        # scindo db
        scindo_number_of_loans = data["User_Finance_TotalLoans_Number"]
        scindo_default = data["User_Behaviour_Default"]
        
        weight = {
            "employment" : 0.25,
            "job_position" : 0.15,
            "completed_loans" : 0.15,
            "salary_on" : 0.25,
            "active_rids" : 0.15,
            "avg_balance" : 0.15,
            "outflow" : 0.15,
            "out/avg" : 0.15,
            "investments" : 0.15,
            "other_loans" : 0.15,
            "other_mortgages" : 0.15,
            "deposits" : 0.15
        }
        sign = {
            "employment" : 1 if job in [True, 1] else 0,
            "job_position" : 1 if not profession in [1, 2, 5, 7] else 0,
            "completed_loans" : 1 if scindo_number_of_loans >= 1 else 0,
            "salary_on" : 1 if salary_on_acc == 1 else 0,
            "active_rids" : 1 if active_rids >= 5 else 0,
            "avg_balance" : 1 if avg_balance >= 1000 else 0,
            "outflow" : 1 if (outflow >= 1000) & (outflow <= 5000)else 0,
            "out/avg" : 1 if outflow/(avg_balance+100) <= 30 else 0,
            "investments" : 1 if investments >= 1000 else 0,
            "other_loans" : 1 if (other_loans <= 10000) & (other_loans >= 1000) else 0,
            "other_mortgages" : 1 if (other_mortgages <= 100000) & (other_mortgages >= 1000) else 0,
            "deposits" : 1 if deposits >= 1000 else 0
        }

        # calculate on main domain then scale

        # main domain
        min_score = 0
        max_score = 2

        credit_score = 0

        # calculate credit score
        for k, v in sign.items(): credit_score += sign[k] * weight[k]
        for k, v in sign.items():  sign[k] = 0

        # scale the score to [0, 1.6] domain
        credit_score = credit_score + np.abs(min_score)

        # calculate the credit score
        if scindo_default == 1: credit_score = 0

        # calculate score in [0,1] domain
        credit_score = credit_score / max_score
        if credit_score <= 0: credit_score = 0

        # default probability calculation
        c1 = 0.0095
        c2 = 0.05
        c3 = 0.005
        x = credit_score

        probability_of_default = c1  * ((1 - x)/(c2 + x)) # - c3

        max_score = 0.2
        probability_of_default = probability_of_default / max_score
        print("Scorecard: ", probability_of_default)

        return probability_of_default

    def ml_calculator(self, data:dict) -> float:

        '''
        questa funzione prepara interroga i modelli ML costruiti da wealthype
        i modelli li prende dalla cartella:
            /built_models

        prima di interrogare i modelli, le variabili di natura categorica
        devono essere trasformati in variabili booleani rappresentando ogni categoria con una
        nuova variabile.

        il modello "encoder", si trova nella cartella:
            /built_models

        le variabili le trova in fil config:
            one_hot_encode
            
        '''

        df = pd.DataFrame(data, index=[0])
        
        transformed_df = self.encoder.transform(df[one_hot_encode]).toarray()
        transformed_df = pd.DataFrame(transformed_df, columns=self.encoder.get_feature_names_out(one_hot_encode))

        df.drop(labels=one_hot_encode, inplace=True, axis=1)
        df[self.encoder.get_feature_names_out(one_hot_encode)] = transformed_df

        # predict and aggregate the result
        prediction_weights = {}
        prediction_weights["cnb_f1"] = json.load(open("report/model_complement_naive_bayes.json", "r"))
        prediction_weights["svc_f1"] = json.load(open("report/model_svc.json", "r"))
        prediction_weights["lr_f1"] = json.load(open("report/model_logistic_regression.json", "r"))
        prediction_weights["isf_f1"] = json.load(open("report/model_isolation_forest.json", "r"))
        prediction_weights["ocs_f1"] = json.load(open("report/model_oneclass_svm.json", "r"))

        predictions = {}

        sum = 0
        for key, value in prediction_weights.items():

            # modelli con f1 < 0.5 non contribuiscono al prediction
            if value["f1_score"] > 0:
                sum += value["f1_score"] 
            else:
                continue
            
            if key == "cnb_f1":
                predictions["cnb_prediction"] = self.cnb.predict(df) * value["f1_score"] 
        
            elif key == "svc_f1":
                predictions["svc_prediction"] = self.svc.predict(df) * value["f1_score"] 
            
            elif key == "lr_f1":
                predictions["lr_prediction"] = self.lr.predict(df) * value["f1_score"] 

            elif key == "isf_f1":
                predict = self.isf.predict(df)
                print("isf: ", predict)
                print("---------------")
                if predict == 1:
                    predictions["isf_prediction"] = 0 * value["f1_score"] 
                elif predict == -1:
                    predictions["isf_prediction"] = 1 * value["f1_score"] 

            elif key == "ocs_f1":
                predict = self.ocs.predict(df)
                print("ocf: ", predict)
                print("---------------")
                if predict == 1:
                    predictions["ocs_prediction"] = 0 * value["f1_score"] 
                elif predict == -1:
                    predictions["ocs_prediction"] = 1 * value["f1_score"] 


        result = np.sum(list(predictions.values())) / sum

        print("ML: ", result)

        return round(result[0], 2)

    def run(self, data:dict) -> float:
        
        '''
        questa funzione aggrega linearmente le diverse predizioni
        accompagnati dai pesi predefiniti.
        una soglia sulla probabilità di default conclude il giro
        risposte:
            1 : non erogare il prestito
            0 : puoi erogare il prestito
        '''

        # render the body to flat format
        data = self.ingest.body_flatener(data)

        # prior
        p1 = self.prior_calculator(self.ingest.prior_body_builder(data))
        beta1 = self.build_beta_binomial_distribution(p1, 10)
        print("beta-prior: ", beta1)

        # score
        p2 = self.score_calculator(self.ingest.scorecard_body_builder(data))
        beta2 = self.build_beta_binomial_distribution(p2, 85)
        print("beta-score: ", beta2)

        # ml
        p3 = self.ml_calculator(self.ingest.ml_body_builder(data))
        beta3 = self.build_beta_binomial_distribution(p3, 5)
        print("beta-ml: ", beta3)

        # mix them up
        alpha = beta1[0] + beta2[0] + beta3[0]
        beta = beta1[1] + beta2[1] + beta3[1]
        peak_of_distribution = alpha / (alpha + beta)

        # threshould : 0.0475 on Pd
        threshould = 0.0475
        probability_of_default = peak_of_distribution

        if  probability_of_default >= threshould:
            default = 1
        else:
            default = 0
        
        if probability_of_default <= 0: probability_of_default = 0

        return { "UserID": data["UserID"], "default_probability" : round(probability_of_default, 4), "sign" : default}
        



        
