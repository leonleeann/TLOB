# Title of the paper
This is the official repository for the paper ...

# Getting Started 
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisities
This project requires Python and Conda. If you don't have them installed, please do so first. It is possible to do it using pip, but in that case you are on you own.   

## Installing
To set up the environment for this project, follow these steps:

1. Clone the repository:
```sh
git clone <repository_url>
```
2. Navigate to the project directory
3. Create a new Conda environment using the environment.yml file:
```sh
conda env create -f environment.yml
```
4. Activate the new Conda environment:
```sh
conda activate deepmarket
```

# Training
If your objective is to train a TLOB or MLPLOB model or implement your model you should follow those steps. 

## Data 
If you have some LOBSTER data you can follow those steps:
1. The format of the data should be the same of LOBSTER: f"{year}-{month}-{day}_34200000_57600000_{type}" and the data should be saved in f"data/{stock_name}/{stock_name}_{year}-{start_month}-{start_day}_{year}-{end_month}-{end_day}". Type can be or message or orderbook.
2. Inside the config file, you need to set the name of the training stock and the testing stocks, and also the dataset to LOBSTER. Currently you can add only one for the training but several for testing. 
3. You need to start the pre-processing step, to do so set config.is_data_preprocessed to False and run python main.py

Otherwise, if you want to train and test the model with the Benchmark dataset FI-2010 you can follow these steps:
1. Download the dataset from the [official website](https://etsin.fairdata.fi/dataset/73eb48d7-4dbc-4a10-a52a-da745b47a649/data).
2. Unzip the data 
3. Create a folder FI-2010 inside your repository
4. Copy these four files in the folder: "Test_Dst_NoAuction_ZScore_CF_7.txt", "Test_Dst_NoAuction_ZScore_CF_8.txt", "Test_Dst_NoAuction_ZScore_CF_9", "Train_Dst_NoAuction_ZScore_CF_7.txt" you can delete the other files.
5. Finally, inside the config file, you need to set Dataset to FI-2010 and set the horizons to 1, 2, 5, or 10. 
Note that the horizons in the paper are an order of magnitude higher because in the paper the value represent the horizons before the sampling process of the dataset. In fact, the dataset is sampled every 10 events. 

## Implementing and Training a new model 
To train a new model, follow these steps:
1. Implement your model class in the models/ directory. Your model class will take in input an input of dimension [batch_size, seq_len, num_features], and should output a tensor of dimension [batch_size, 3].
2. add your model to pick_model in utils_models.
3. Update the config file to include your model and its hyperparameters. If you are using the FI-2010 dataset, It is suggested to set the hidden dim to 40 and the hp all_features to false if you want to use only the LOB as input or if you want to use the LOB and market features the hidden dim should be 144 and all features true. If you are using LOBSTER data, it is suggested to set the hidden dim to 46 and all features to true to use LOB and orders, while if you want to use only the LOB set all features to False. 
4. Add your model with cs.store, similar to the other models
5. Run the training script:
```sh
python main.py +model={your_model_name} hydra.job.chdir=False
```
6. You can set whatever configuration using the hydra style of prompt.
7. A checkpoint will be saved in data/checkpoints/ 

Optionally you can also log the run with wandb or run a sweep, changing the config experiment options.


## Training a TLOB, MLPLOB, DeepLOB or BiNCTABL Model 
To train a TLOB, MLPLOB, DeepLOB or BiNCTABL Model, you need to run this command:
```sh
python main.py +model={model_name} hydra.job.chdir=False
```
you can see all the model names in the config file. 