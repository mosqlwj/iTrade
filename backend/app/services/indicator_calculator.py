import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.services.data_fetcher import data_fetcher


class IndicatorCalculator:
    def calculate_ma(self, data: List[float], window: int = 7) -> Optional[float]:
        if len(data) < window:
            return None
        return float(np.mean(data[-window:]))

    def calculate_change_percent(self, data: List[float]) -> float:
        if len(data) < 2:
            return 0.0
        current = data[-1]
        previous = data[-2]
        if previous == 0:
            return 0.0
        return float((current - previous) / previous * 100)

    def analyze_trend(self, data: List[float]) -> str:
        if len(data) < 3:
            return "insufficient_data"
        
        recent = data[-7:] if len(data) >= 7 else data
        first_half = recent[:len(recent)//2]
        second_half = recent[len(recent)//2:]
        
        avg_first = np.mean(first_half)
        avg_second = np.mean(second_half)
        
        if avg_second > avg_first * 1.02:
            return "uptrend"
        elif avg_second < avg_first * 0.98:
            return "downtrend"
        else:
            return "stable"

    def simple_prediction(self, data: List[float], days: int = 7) -> Dict:
        if len(data) < 10:
            return {"predicted": None, "confidence": "low"}
        
        df = pd.DataFrame({"value": data})
        df["ma7"] = df["value"].rolling(window=7).mean()
        df["ma30"] = df["value"].rolling(window=30).mean()
        
        recent_ma7 = df["ma7"].iloc[-1]
        recent_ma30 = df["ma30"].iloc[-1]
        
        if pd.isna(recent_ma7) or pd.isna(recent_ma30):
            return {"predicted": None, "confidence": "low"}
        
        trend = "up" if recent_ma7 > recent_ma30 else "down"
        
        growth_rate = (recent_ma7 - recent_ma30) / recent_ma30 * 100
        
        predicted = recent_ma7 * (1 + growth_rate / 100 * days / 30)
        
        return {
            "predicted": float(predicted),
            "trend": trend,
            "confidence": "medium" if len(data) >= 30 else "low"
        }

    def calculate_volatility(self, data: List[float]) -> float:
        if len(data) < 2:
            return 0.0
        return float(np.std(data))

    def get_indicator_trend(self, indicator_code: str) -> Dict:
        df = data_fetcher.fetch_indicator_data(indicator_code)
        
        if df.empty:
            return {
                "indicator_code": indicator_code,
                "trend": "no_data",
                "change_percent": 0.0,
                "ma_7": None,
                "ma_30": None,
                "prediction": None
            }
        
        if "date" in df.columns:
            values = df["value"].tolist() if "value" in df.columns else df.iloc[:, 1].tolist()
        else:
            values = df.iloc[:, 0].tolist()
        
        change_percent = self.calculate_change_percent(values)
        trend = self.analyze_trend(values)
        ma_7 = self.calculate_ma(values, 7)
        ma_30 = self.calculate_ma(values, 30)
        prediction = self.simple_prediction(values)
        volatility = self.calculate_volatility(values)
        
        return {
            "indicator_code": indicator_code,
            "trend": trend,
            "change_percent": change_percent,
            "ma_7": ma_7,
            "ma_30": ma_30,
            "prediction": prediction,
            "volatility": volatility,
            "latest_value": values[0] if values else None
        }

    def compare_indicators(self, codes: List[str], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        results = {}
        for code in codes:
            df = data_fetcher.fetch_indicator_data(code)
            if not df.empty:
                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]
                results[code] = {
                    "data": df.to_dict(orient="records"),
                    "latest_value": float(df["value"].iloc[0]) if "value" in df.columns else float(df.iloc[0, 1])
                }
        return results


indicator_calculator = IndicatorCalculator()
