import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination)
        self.is_trained = False
    
    def train(self, X):
        """Train the anomaly detection model"""
        self.model.fit(X)
        self.is_trained = True
    
    def detect(self, data_point):
        """Detect if a data point is an anomaly"""
        if not self.is_trained:
            raise Exception("Model not trained")
        
        prediction = self.model.predict([data_point])
        return prediction[0] == -1
    
    def evaluate_sensor_data(self, data):
        """Evaluate sensor data for anomalies"""
        features = np.array([
            data.get('value', 0),
            data.get('variance', 0),
            data.get('timestamp', 0) % 86400  # Time of day
        ])
        return self.detect(features)