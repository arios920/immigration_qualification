1. Model Evaluation

    -- prepare datasets correctly labeled high/medium/low for O1A visa qualification
    -- use Cross Entropy as loss function during training (add class weights to handle data imbalance)
    -- observe performance on Accuracy, Recall, Precision, and F1 score
    -- perform Cross-Validation to ensure stability and robustness of the model


2. App Evaluation

    -- Functionality
        -- successful upload or not?
        -- text extraction works or not?
        -- classification result matches scores/probabilities or not?
        -- UI/UX: just for customer experience improvement
    
    -- Performance Testing
        -- Response time: currently a problem for this project due to lack of compute and technical resources
        -- Scalability: the app should support multiple concurrent users and their accesses

