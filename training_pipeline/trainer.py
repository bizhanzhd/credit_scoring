
from training_pipeline.input_ingestor import train_input_ingestion

import json
import pandas as pd
import numpy as np
from config import one_hot_encode
from sklearn.metrics import balanced_accuracy_score, average_precision_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import OneHotEncoder


class trainer:

    def __init__(self) -> None:

        '''
        questa classe ha le funzioni adatti per preprocessing
        e crea diversi modelli nella funzione run
        e li salva nella cartella:
            /built_models
        '''

        self.ingestor = train_input_ingestion()

    def encoder(self, df:pd.DataFrame) -> pd.DataFrame:
        
        '''
        questa funzione trasforma le variabili di natura categorica
        in variabili booleani rappresentando ogni categoria con una
        nuova variabile 

        le variabili le trova in fil config:
            one_hot_encode

        il metodo utilizzato:
            OneHotEncoder
        '''

        encoder = OneHotEncoder(handle_unknown='ignore')
        encoder.fit(df[one_hot_encode])
        pickle.dump(encoder, open("built_models/encoder.pkl", "wb"))

        transformed_df = encoder.transform(df[one_hot_encode]).toarray()
        transformed_df = pd.DataFrame(transformed_df, columns=encoder.get_feature_names_out(one_hot_encode))

        df.drop(labels=one_hot_encode, inplace=True, axis=1)
        df[encoder.get_feature_names_out(one_hot_encode)] = transformed_df

        return df
    
    def metrics_calculator(self, y_true:pd.Series, y_pred:pd.Series) -> dict:

        '''
        questa funzione ha le funzionalità per calcolare diverse
        metriche dei modelli ML
        '''

        metrics = {
            "precision" : np.round(average_precision_score(y_true, y_pred), 2),
            "f1_score" : np.round(f1_score(y_true, y_pred), 2),
            "bacc" : np.round(balanced_accuracy_score(y_true, y_pred), 2)
        }

        return metrics
    
    def ml_logistic_regression(self):
        
        '''
        questa funzione addestra un modello ML
        
        soluzione:
            Classificatore
        
        modello:
            LogisticRegression
        
        splitto dati:
            StratifiedKFold
        '''

        X = self.X
        y = self.y

        cumsum_f1 = 0

        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)
        # l1 : manhatan distance : pesi a zero, molto robusto per outliers
        # l2 : somma dei quadrati dei pesi : molti bassi ma non zero
        model = LogisticRegression(class_weight='balanced', solver="saga", penalty="l2")

        # enumerate the splits
        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X.loc[train_ix, :]
            X_test = X.loc[test_ix, :]
            
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
            cumsum_precision = metrics["precision"]
            cumsum_balanced_accuracy = metrics["bacc"]

        mean_f1 = np.round(cumsum_f1 / 3, 2)

        model_details = {
            "precision" : np.round(cumsum_precision / 3, 2),
            "f1_score" : mean_f1,
            "bacc" : np.round(cumsum_balanced_accuracy / 3, 2)
        }

        return (model, mean_f1, model_details)

    def ml_complement_nb(self) -> tuple:
        
        '''
        questa funzione addestra un modello ML

        soluzione:
            Classificatore
        
        modello:
            ComplementNB
        
        splitto dati:
            StratifiedKFold
        '''
                
        X = self.X
        y = self.y

        cumsum_f1 = 0

        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)
        model = ComplementNB(fit_prior=True)

        # enumerate the splits
        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X.loc[train_ix, :]
            X_test = X.loc[test_ix, :]
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
            cumsum_precision = metrics["precision"]
            cumsum_balanced_accuracy = metrics["bacc"]

        mean_f1 = np.round(cumsum_f1 / 3, 2)

        model_details = {
            "precision" : np.round(cumsum_precision / 3, 2),
            "f1_score" : mean_f1,
            "bacc" : np.round(cumsum_balanced_accuracy / 3, 2)
        }

        return (model, mean_f1, model_details)

    def ml_svc(self) -> tuple:

        '''
        questa funzione addestra un modello ML
        
        soluzione:
            Classificatore
        
        modello:
            SVC
        
        splitto dati:
            StratifiedKFold
        '''

        # enumerate the splits
        X = self.X
        y = self.y

        model = SVC(class_weight='balanced', probability=True, random_state=42)
        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)

        cumsum_f1 = 0

        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X.loc[train_ix, :]
            X_test = X.loc[test_ix, :]
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
            cumsum_precision = metrics["precision"]
            cumsum_balanced_accuracy = metrics["bacc"]

        mean_f1 = np.round(cumsum_f1 / 3, 2)

        model_details = {
            "precision" : np.round(cumsum_precision / 3, 2),
            "f1_score" : mean_f1,
            "bacc" : np.round(cumsum_balanced_accuracy / 3, 2)
        }

        return (model, mean_f1, model_details)

    def label_preparer(self, df:pd.DataFrame) -> pd.DataFrame:
        
        '''
        per i modelli del tipo OUTLIER DETECTOR
        come:
            isolation forest, one class svm
        
        si deve modificare [0:good payer, 1:bad payer] a [-1, 1] rispettivamente
        '''

        for idx, row in df.iterrows():
            
            # bad payer
            if row["target"] == 1:
                df.loc[idx, "target"] = 1
            
            # good payer
            elif row["target"] == 0:
                df.loc[idx, "target"] = -1

        return df

    def pollution_cleaner(self, df:pd.DataFrame) -> pd.DataFrame:
       
        '''
        per i modelli del tipo OUTLIER DETECTOR
        come:
            isolation forest, one class svm
        
        si deve eliminare -1:bad payer
        '''

        df_clean = df[df["target"] == +1]
        df_pollution = df[df["target"] == -1]
       
        return df_clean, df_pollution

    def ml_isolation_forest(self) -> tuple:

        '''
        questa funzione addestra un modello ML
        
        soluzione:
            rilevamento delle anomalie
        
        modello:
            IsolationForest
        
        splitto dati:
            la funzione pollution_cleaner
        '''

        # instantiate the model
        model = IsolationForest(contamination=0.01, max_features=6, random_state=1)

        # prepare the label for outlier detector
        df = self.label_preparer(self.df)

        # split the data to train and test
        df_train, df_test = train_test_split(df, test_size=0.3, random_state=42)

        # clean train data, encode, and fit the model
        df_train_clean, df_train_pollution = self.pollution_cleaner(df_train)
        X_train = df_train_clean.loc[:, df_train_clean.columns != "target"]

        model.fit(X_train)

        # make the test set and predict
        df_test = pd.concat([df_test, df_train_pollution])
        X_test = df_test.loc[:, df.columns != "target"]
        y_test = df_test.loc[:, "target"]
        y_pred = model.predict(X_test)

        # test the model
        model_details = self.metrics_calculator(y_test, y_pred)
        f1 = model_details["f1_score"]
        
        return (model, f1, model_details)
    
    def ml_oneclass_svm(self) -> tuple:

        '''
        questa funzione addestra un modello ML
        
        soluzione:
            rilevamento delle anomalie
        
        modello:
            OneClassSVM
        
        splitto dati:
            la funzione pollution_cleaner
        '''

        # instantiate the model
        model = OneClassSVM(kernel="rbf", nu=0.01, gamma="auto")

        # prepare the label for outlier detector
        df = self.label_preparer(self.df)

        # split the data to train and test
        df_train, df_test = train_test_split(df, test_size=0.3, random_state=42)

        # clean train data and fit the model
        df_train_clean, df_train_pollution = self.pollution_cleaner(df_train)
        X_train = df_train_clean.loc[:, df_train_clean.columns != "target"]

        model.fit(X_train)

        # make the test set and predict
        df_test = pd.concat([df_test, df_train_pollution])
        X_test = df_test.loc[:, df.columns != "target"]
        y_test = df_test.loc[:, "target"]
        y_pred = model.predict(X_test)

        # test the model
        model_details = self.metrics_calculator(y_test, y_pred)
        f1 = model_details["f1_score"]
        
        return (model, f1, model_details)

    def run(self, df:pd.DataFrame) -> pd.DataFrame:
        
        ingested_df = self.ingestor.ml_df_builder(df)

        self.df = self.encoder(ingested_df)

        self.X = self.df.loc[:, self.df.columns != "target"]
        self.y = self.df["target"]

        model, f1_score, model_details = self.ml_logistic_regression()

        with open('report/model_logistic_regression.json', "w") as outfile: 
            json.dump(model_details, outfile, indent=4)
        
        with open('built_models/model_logistic_regression.pkl', "wb") as outfile: 
            pickle.dump(model, outfile)


        model, f1_score, model_details = self.ml_complement_nb()

        with open('report/model_complement_naive_bayes.json', "w") as outfile: 
            json.dump(model_details, outfile, indent=4)
        
        with open('built_models/model_complement_naive_bayes.pkl', "wb") as outfile: 
            pickle.dump(model, outfile)


        model, f1_score, model_details = self.ml_svc()

        with open('report/model_svc.json', "w") as outfile: 
            json.dump(model_details, outfile, indent=4)

        with open('built_models/model_svc.pkl', "wb") as outfile: 
            pickle.dump(model, outfile)

        
        model, f1_score, model_details = self.ml_isolation_forest()

        with open('report/model_isolation_forest.json', "w") as outfile: 
            json.dump(model_details, outfile, indent=4)

        with open('built_models/model_isolation_forest.pkl', "wb") as outfile: 
            pickle.dump(model, outfile)


        model, f1_score, model_details = self.ml_oneclass_svm()

        with open('report/model_oneclass_svm.json', "w") as outfile: 
            json.dump(model_details, outfile, indent=4)

        with open('built_models/model_oneclass_svm.pkl', "wb") as outfile: 
            pickle.dump(model, outfile)

        return "the training was executed completely"