from hydra.core.config_store import ConfigStore
from dataclasses import dataclass, field
from constants import Dataset, ModelType
from omegaconf import MISSING, OmegaConf
#OmegaConf.register_new_resolver("Dataset", lambda x: Dataset[x])


@dataclass
class Model:
    hyperparameters_fixed: dict = MISSING
    hyperparameters_sweep: dict = MISSING
    type: ModelType = MISSING
    
    
@dataclass
class MLP(Model):
    hyperparameters_fixed: dict = field(default_factory=lambda: {"num_layers": 3, "hidden_dim": 144, "lr": 0.0003, "seq_size": 384, "all_features": True})
    hyperparameters_sweep: dict = field(default_factory=lambda: {"num_layers": [3, 6], "hidden_dim": [144, 128], "lr": [0.0003], "seq_size": [384]})
    type: ModelType = ModelType.MLP
    
    
@dataclass
class Transformer(Model):
    hyperparameters_fixed: dict = field(default_factory=lambda: {"num_layers": 4, "hidden_dim": 144, "num_heads": 1, "is_sin_emb": True, "lr": 0.0001, "seq_size": 128, "all_features": True})
    hyperparameters_sweep: dict = field(default_factory=lambda: {"num_layers": [4, 6], "hidden_dim": [144, 128, 256], "num_heads": [1], "is_sin_emb": [True], "lr": [0.0001], "seq_size": [128]})
    type: ModelType = ModelType.TRANSFORMER
    
@dataclass
class BiNCTABL(Model):
    hyperparameters_fixed: dict = field(default_factory=lambda: {"lr": 0.001, "seq_size": 10, "all_features": False})
    hyperparameters_sweep: dict = field(default_factory=lambda: {"lr": [0.001], "seq_size": [10]})
    type: ModelType = ModelType.BINCTABL

@dataclass
class DeepLOB(Model):
    hyperparameters_fixed: dict = field(default_factory=lambda: {"lr": 0.01, "seq_size": 100, "all_features": False})
    hyperparameters_sweep: dict = field(default_factory=lambda: {"lr": [0.01], "seq_size": [100]})
    type: ModelType = ModelType.DEEPLOB
    
@dataclass
class Experiment:
    is_data_preprocessed: bool = True
    is_wandb: bool = True
    is_sweep: bool = False
    type: list = field(default_factory=lambda: ["TRAINING"])
    is_debug: bool = False
    checkpoint_reference: str = "data/checkpoints/TRANSFORMER/val_loss=0.192_epoch=8_FI-2010_seq_size_128_horizon_10_num_layers_4_hidden_dim_144_num_heads_1_is_sin_emb_True_lr_0.0001_seq_size_128_all_features_True_type_TRANSFORMER_last.ckpt"
    dataset_type: Dataset = Dataset.LOBSTER
    sampling_type: str = "quantity"    #time or quantity
    sampling_time: str = ""   #seconds
    sampling_quantity: int = 500
    training_stocks: list = field(default_factory=lambda: ["INTC"])
    testing_stocks: list = field(default_factory=lambda: ["INTC"])
    seed: int = 42
    horizon: int = 100
    max_epochs: int = 10
    batch_size: int = 128
    filename_ckpt: str = "model.ckpt"
    optimizer: str = "Adam"
    
    
@dataclass
class Config:
    model: Model
    experiment: Experiment = field(default_factory=Experiment)


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="model", name="mlplob", node=MLP)
cs.store(group="model", name="tlob", node=Transformer)
cs.store(group="model", name="binctabl", node=BiNCTABL)
cs.store(group="model", name="deeplob", node=DeepLOB)
