import pytest
import pandas as pd
import numpy as np
from backend.services.etl_pipeline import ETLPipeline


@pytest.fixture
def etl():
    return ETLPipeline()


def _make_df(values, entity="A"):
    """Helper to build a DataFrame with a single metric column."""
    n = len(values)
    return pd.DataFrame({
        "entity": [entity] * n,
        "date": pd.date_range("2023-01-01", periods=n, freq="MS"),
        "metric": values,
    })


class TestConfidenceScoring:
    def test_normal_values_get_high_confidence(self, etl):
        """All values within IQR should receive the default 0.95 score."""
        df = _make_df([100, 102, 98, 101, 99, 103, 97, 100])
        result = etl.standardize_to_decision_table(df, "entity", "date")
        assert (result["confidence_score"] == 0.95).all()

    def test_extreme_outlier_gets_low_confidence(self, etl):
        """A value far outside the IQR should receive 0.50 confidence."""
        normal = [100] * 10
        values = normal + [100000]  # extreme outlier
        df = _make_df(values)
        result = etl.standardize_to_decision_table(df, "entity", "date")

        outlier_row = result[result["metric_value"] == 100000]
        assert len(outlier_row) == 1
        assert outlier_row.iloc[0]["confidence_score"] == 0.50

        normal_rows = result[result["metric_value"] == 100]
        assert (normal_rows["confidence_score"] == 0.95).all()

    def test_mild_outlier_gets_medium_confidence(self, etl):
        """A value just outside 1.5*IQR but inside 3*IQR should get 0.70."""
        # With this data: Q1=100, Q3=110, IQR=10
        # Upper fence = 110 + 15 = 125, extreme upper = 110 + 30 = 140
        # 130 is between 125 (mild) and 140 (extreme) → mild outlier
        values = [90, 90, 100, 100, 110, 110, 100, 100,
                  130]
        df = _make_df(values)
        result = etl.standardize_to_decision_table(df, "entity", "date")

        outlier_row = result[result["metric_value"] == 130]
        assert len(outlier_row) == 1
        assert outlier_row.iloc[0]["confidence_score"] == 0.70

    def test_too_few_values_keeps_default(self, etl):
        """With fewer than 4 data points, IQR is unreliable — keep 0.95."""
        df = _make_df([100, 200, 300])
        result = etl.standardize_to_decision_table(df, "entity", "date")
        assert (result["confidence_score"] == 0.95).all()

    def test_identical_values_keeps_default(self, etl):
        """When all values are the same (IQR=0), keep 0.95."""
        df = _make_df([42] * 10)
        result = etl.standardize_to_decision_table(df, "entity", "date")
        assert (result["confidence_score"] == 0.95).all()

    def test_multiple_metrics_scored_independently(self, etl):
        """Each metric column should be scored using its own distribution."""
        df = pd.DataFrame({
            "entity": ["A"] * 8,
            "date": pd.date_range("2023-01-01", periods=8, freq="MS"),
            "stable_metric": [100, 100, 100, 100, 100, 100, 100, 100],
            "volatile_metric": [10, 10, 10, 10, 10, 10, 10, 10000],
        })
        result = etl.standardize_to_decision_table(df, "entity", "date")

        stable = result[result["metric_name"] == "stable_metric"]
        volatile = result[result["metric_name"] == "volatile_metric"]

        assert (stable["confidence_score"] == 0.95).all()
        # The 10000 outlier in volatile_metric should have lower confidence
        outlier = volatile[volatile["metric_value"] == 10000]
        assert outlier.iloc[0]["confidence_score"] < 0.95
