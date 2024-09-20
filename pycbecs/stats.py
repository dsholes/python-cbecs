from statsmodels.stats.weightstats import DescrStatsW
import pandas as pd

DEFAULT_QUANTILE_MAP = {0.25: "q1", 0.5: "median", 0.75: "q3"}


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def describe_weighted(
        df: pd.DataFrame,
        describe_col: str,
        weights_col: str,
        quantile_map: dict = DEFAULT_QUANTILE_MAP,
    ) -> pd.Series:
        if quantile_map != DEFAULT_QUANTILE_MAP:
            if not isinstance(quantile_map, dict):
                raise ValueError("`quantile_map` must be of type `dict`")
            else:
                quantile_map.update(DEFAULT_QUANTILE_MAP)
        wq = DescrStatsW(data=df[describe_col], weights=df[weights_col])
        quant = wq.quantile(list(quantile_map.keys())).rename(
            index=quantile_map
        )
        iqr = quant["q3"] - quant["q1"]
        lower_fence = max(quant["q1"] - 1.5 * iqr, 0)
        upper_fence = quant["q3"] + 1.5 * iqr
        beginning = pd.Series(
            {
                "count": len(df),
                "n_obs": wq.nobs,
                "mean": wq.mean,
                "std": wq.std,
                "lower_fence": lower_fence,
                "min": df[describe_col].min(),
            }
        )
        end = pd.Series(
            {
                "max": df[describe_col].max(),
                "upper_fence": upper_fence,
            }
        )
        return pd.concat([beginning, quant, end])
