from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.model_trainer import Training
from cnnClassifier import logger



STAGE_NAME = "Training"



class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        training.train_valid_generator()
        training.train()



if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
        
from cnnClassifier import logger
from cnnClassifier.components.model_trainer import Training
from cnnClassifier.config.configuration import ConfigurationManager


STAGE_NAME = "Model Training"


class ModelTrainingPipeline:
    """Pipeline to train the updated base model on the prepared dataset."""

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        config = ConfigurationManager()
        training_config = config.get_training_config()

        trainer = Training(config=training_config)
        trainer.get_base_model()
        trainer.train_valid_generator()
        trainer.train()


if __name__ == "__main__":
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelTrainingPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
