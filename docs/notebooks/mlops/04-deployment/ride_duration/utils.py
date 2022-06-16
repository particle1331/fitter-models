import pandas as pd
import warnings
import uuid

from pathlib import Path
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin


# Config variables
package_dir = Path(__file__).parent.resolve()


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def load_training_dataframe(file_path, y_min=1, y_max=60):
    """Load data from disk and preprocess for training."""
    
    # Load data from disk
    data = pd.read_parquet(file_path)

    # Create target column and filter outliers
    data['duration'] = data.lpep_dropoff_datetime - data.lpep_pickup_datetime
    data['duration'] = data.duration.dt.total_seconds() / 60
    data = data[(data.duration >= y_min) & (data.duration <= y_max)]

    # Create uuids
    data['ride_id'] = generate_uuids(len(data))

    return data


def prepare_features(input):
    """Prepare features for dict vectorizer."""

    X = pd.DataFrame(input)
    X['PU_DO'] = X['PULocationID'].astype(str) + '_' + X['DOLocationID'].astype(str)
    X = X[['PU_DO', 'trip_distance']].to_dict(orient='records')
    
    return X