# MLflow - TensorFlow Keras `__version__` Hatası Çözümü

## 1. Sorun Tanımı
TensorFlow (`tf.keras`) ile eğitilmiş bir modeli `mlflow.keras.log_model()` veya `mlflow.tensorflow.log_model()` ile loglamaya çalışırken şu hata alındı:

```
AttributeError: module 'tensorflow.keras' has no attribute '__version__'
```

## 2. Hatanın Kaynağı
- MLflow, modeli loglarken metadata dosyasına kullanılan Keras sürümünü eklemek ister.
- Bunun için `keras_module.__version__` çağırır.
- Ancak `tensorflow.keras`, bağımsız `keras` paketinden farklıdır ve `__version__` alanı bulunmaz.
- Bu nedenle `AttributeError` oluşur.

## 3. Uygulanan Çözüm (Patch)
Eksik olan `__version__` attribute'u **manuel olarak** ekledik.  
Böylece MLflow, `tensorflow.keras.__version__` istediğinde hata almadan TensorFlow versiyonunu görebildi.

## 4. Kod Örneği

```python
import tensorflow as tf
keras = tf.keras

# Eksik olan __version__ alanını ekle
keras.__version__ = tf.__version__       # alias için patch
tf.keras.__version__ = tf.__version__    # MLflow'un iç import'u için patch

# Artık sorunsuz loglama yapılabilir
import mlflow

mlflow.keras.log_model(
    keras_model, 
    "model", 
    registered_model_name="VGG16Model"
)
```

## 5. Neden Çalıştı?
- MLflow `import tensorflow.keras as keras_module` yaparak bu modülün `__version__` bilgisini okumaya çalışıyordu.
- Biz `tf.keras.__version__` alanını manuel ekleyince, MLflow artık geçerli bir değer buldu.
- Sonuç olarak model başarıyla loglandı.

## 6. Daha Stabil Hale Getirmek İçin Öneriler
Bu patch geçici bir çözümdür. Daha kalıcı ve stabil çözümler için:

1. **MLflow'u Güncelle**  
   - Yeni sürümlerde bu bug düzeltilmiş olabilir.  
   ```bash
   pip install --upgrade mlflow
   ```

2. **Bağımsız Keras Kullan**  
   - Eğer `pip install keras` ile bağımsız `keras` paketini kullanırsan, `keras.__version__` zaten mevcut olur.  
   - Ancak TensorFlow içindeki `tf.keras` yerine bağımsız `keras` ile çalışmak gerekir.

3. **MLflow’a Artifact Olarak Kaydet**  
   - Eğer Model Registry özelliklerine ihtiyacın yoksa, modeli `.h5` olarak kaydedip MLflow’a artifact olarak yükleyebilirsin:  
   ```python
   model.save("artifacts/training/trained_model.h5")
   mlflow.log_artifact("artifacts/training/trained_model.h5", artifact_path="model")
   ```

4. **Çevresel Tutarlılık Sağla**  
   - Conda veya venv içinde TensorFlow ve MLflow sürümlerini net şekilde sabitle (`requirements.txt` veya `environment.yml` kullanarak).  

---

📌 **Sonuç:**  
- Patch ile sorun hızlıca çözüldü.  
- Uzun vadede **MLflow sürüm güncellemesi** veya **bağımsız Keras ile çalışma** önerilir.  
