# 🐛 Issue: MLflow Model Logging Warnings

## Açıklama
Evaluation stage sırasında MLflow modeli başarıyla logluyor, ancak aşağıdaki uyarılar görülüyor:

```
WARNING mlflow.tensorflow: You are saving a TensorFlow Core model or Keras model without a signature.
Inference with mlflow.pyfunc.spark_udf() will not work unless the model's pyfunc representation accepts pandas DataFrames as inference inputs.

WARNING mlflow.models.model: Model logged without a signature and input example.
Please set `input_example` parameter when logging the model to auto infer the model signature.
```

Bu, modelin loglandığını ancak **signature** (girdi/çıktı formatı) ve **örnek giriş (input_example)** bilgisinin eksik olduğunu gösteriyor.

---

## Etki
- Model DagsHub/MLflow arayüzünde görünüyor ama hangi input shape’i beklediği net değil.  
- Spark UDF veya `mlflow.pyfunc` kullanımı için uygun değil.  
- Uzun vadede reproducibility ve deployment süreçlerinde sorun çıkarabilir.  

---

## Çözüm Önerisi
`Evaluation.log_into_mlflow()` fonksiyonunda modeli loglarken **signature** ve **input_example** eklenmeli.

### Önerilen kod değişikliği:
```python
import numpy as np
from mlflow.models.signature import infer_signature

# Örnek input (tek bir batch, image_size ile)
example_input = np.random.rand(1, *self.config.params_image_size)

# Model çıktısını al
example_output = self.model.predict(example_input)

# Signature çıkar
signature = infer_signature(example_input, example_output)

with mlflow.start_run():
    mlflow.log_params(dict(self.config.all_params))
    mlflow.log_metrics({"loss": self.score[0], "accuracy": self.score[1]})
    
    mlflow.keras.log_model(
        self.model,
        "model",
        signature=signature,
        input_example=example_input,
        registered_model_name="VGG16Model"
    )
```

---

## Yapılacaklar
- [ ] `Evaluation.log_into_mlflow()` içine signature + input_example desteği eklenmeli  
- [ ] Mevcut `evaluation.py` güncellenmeli  
- [ ] Pipeline çalıştırılarak MLflow üzerinde input/output metadata doğrulanmalı  

---

### Labels
`enhancement`, `mlflow`, `model-logging`
