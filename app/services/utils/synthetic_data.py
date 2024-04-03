from sdv.lite import SingleTablePreset
from app.models.utils.data_gen import ZenithDataset

class SyntheticDataService:
    def __init__(self, real_data):
        self.synthesizer = SingleTablePreset(
            ZenithDataset,
            name='FAST_ML',
            locales=['en_US']
        )
        self.real_data = real_data

    def fit_synthesizer(self):
        self.synthesizer.fit(self.real_data)

    def generate_synthetic_data(self, num_rows:int=100):
        return self.synthesizer.sample(num_rows)