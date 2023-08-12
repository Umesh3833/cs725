CS 725 (Autumn 2022): Programming Assignment
Implementation of a Feedforward Neural Network (FNN) using Python

Group Details
Roll No.   Name
22M2116 Dhruv Kudale
22M2118 Ameya Srivastava
22M2122 Kishan Maharaj
22M1078 Umeshraja N


The assignment consists of four parts. 
This repository is a consolidated submission for all the parts.

Part 1
Implementing a FNN using Python

    Part 1A
        Running mini-batch gradient descent on Mean Squared Error (MSE) loss function.
        The corresponding code is present in 'nn_1.py' file
        
        Instructions for running nn_1.py:
            
            > python3 nn_1.py

            Using this command will start the training and epoch-wise losses for both the training set and dev set are printed.
            
            Default Hyperparameters recommended for the same are as follows:
            	max_epochs = 20
	            batch_size = 32
	            learning_rate = 0.00075
	            num_layers = 4
	            num_units = 8
	            lamda = 0.1 
            You can make changes to the relevant values in the main function. 


    Part 1B
        Plotting graphs showing the training loss (regularized MSE) and dev set loss (RMSE) after each epoch.
        This is done for each of the batch sizes: 32 and 64, for the first 100 epochs.
        The relevant graphs are present in 'plots_1b' folder.

Part 2
Evaluation of network's performance on given test data

    Predictions on test data are submitted on the relevant Kaggle competition in a CSV file of the required format.
    Kaggle Competition https://www.kaggle.com/competitions/cs725-2022-assignment-regression

    The corresponding code for testing is present in 'nn_2.py' file
    A few enhancements used in Part 2 include Feature Scaling and Early Stopping

     Instructions for running nn_2.py:
            
            > python3 nn_2.py

            Using this command will start the training and epoch-wise losses for both the training set and dev set are printed.
            After training is completed, the model is used to perform test set predictions
            All the predicted years are written into a single-column CSV file named 'preds.csv'

    Newly Introduced Early Stopping Hyperparameters:
        patience: The number of past epochs to consider in evaluating whether the dev loss value is improving or not.
        min_delta: The minimum difference in values of consecutive dev RMSE loss to be considered as an 'improvement'

    A two-column CSV file named 'part_2.csv' is present which contains the hyperparameter values used for testing.
    You can make the changes in the relevant values in the main function on nn_2.py

Part 3
Perform Feature Selection

    The file 'nn_3.py' contains the implementation for feature selection.
    We have implemented Pearson Correlation-Based Feature Selection to shortlist 75 features from the existing feature set.

    Instructions for running nn_3.py:
            
            > python3 nn_3.py

            Using this command will start the training and epoch-wise losses for both the training set and dev set are printed.
            After training is completed, the model is used to perform test set predictions
            All the predicted years are written into a single-column CSV file named 'preds.csv'
    
    A two-column CSV file named 'part_3.csv' is present which contains the hyperparameter values used for testing.
    You can make the changes in the relevant values in the main function on nn_3.py
    There are no new hyperparameters introduced in this Part3. 
    Please refer to the description of hyperparameters in Part 2 for the same. 
    
    The 'features.csv' file has a single column enlisting the features that are present after feature selection.

Part 4
Classification task to predict a label among ("Very Old", "Old", "New" and "Recent")
https://www.kaggle.com/competitions/cs-725-autumn-2022-assignment-classification/overview

    The submission for this part is present in the 'classification' sub-folder
        The file 'nn_classification.py' contains the implementation for the same.
        The 'params.csv' file describes the hyperparameters used in this task.
        You can make the changes in the relevant values in the main function on nn_classification.py

    Instructions for running nn_classification.py:
            
        > python3 nn_classification.py

        Using this command will start the training and epoch-wise losses for both the training set and dev set are printed.
        After training is completed, the model is used to perform test set predictions
        All the predicted classes are written into a single column CSV file named 'preds.csv'


NOTE: 
    1. The dataset for running the code smoothly should be present in the following path:
        <your_roll_number>/classification/data/ or <your_roll_number>/regression/data/

    2. The dataset (train.csv, dev.csv, and test.csv) is not present in this submission directory.
    
    3. Predictions for Part 2 and Part 4 are submitted on corresponding Kaggle-hosted competition  