import akshare as ak
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os
from pathlib import Path


class DataFetcher:
    def __init__(self, cache_dir: str = "./data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.indicator_cache: Dict[str, Any] = {}

    def _get_cache_key(self, indicator_code: str) -> str:
        return f"{indicator_code}_cache.json"

    def _load_from_cache(self, indicator_code: str) -> Optional[pd.DataFrame]:
        cache_file = self.cache_dir / self._get_cache_key(indicator_code)
        if cache_file.exists():
            try:
                df = pd.read_json(cache_file)
                return df
            except:
                return None
        return None

    def _save_to_cache(self, indicator_code: str, df: pd.DataFrame):
        cache_file = self.cache_dir / self._get_cache_key(indicator_code)
        df.to_json(cache_file, orient="records", date_format="iso")

    def parse_chinese_date(self, date_str: str) -> Optional[datetime]:
        try:
            if '第1-4季度' in date_str:
                year = date_str.replace('年第1-4季度', '')
                return datetime(int(year), 12, 31)
            elif '第1-3季度' in date_str:
                year = date_str.replace('年第1-3季度', '')
                return datetime(int(year), 9, 30)
            elif '第1-2季度' in date_str:
                year = date_str.replace('年第1-2季度', '')
                return datetime(int(year), 6, 30)
            elif '第1季度' in date_str:
                year = date_str.replace('年第1季度', '')
                return datetime(int(year), 3, 31)
            elif '年' in date_str and '月' in date_str:
                year = int(date_str[:4])
                month = int(date_str[5:7])
                return datetime(year, month, 1)
            return None
        except:
            return None

    def fetch_gdp_data(self) -> pd.DataFrame:
        try:
            df = ak.macro_china_gdp()
            if df.empty or '季度' not in df.columns:
                return pd.DataFrame()
            
            result = pd.DataFrame()
            result["date"] = df["季度"].apply(self.parse_chinese_date)
            
            col_name = "国内生产总值-同比增长"
            if col_name in df.columns:
                result["value"] = pd.to_numeric(df[col_name], errors="coerce")
            else:
                return pd.DataFrame()
            
            result = result.dropna()
            max_date = datetime(2025, 12, 31)
            result = result[result["date"] <= max_date]
            result = result.sort_values("date", ascending=False)
            return result
        except Exception as e:
            print(f"获取GDP数据失败: {e}")
            return pd.DataFrame()

    def fetch_cpi_data(self) -> pd.DataFrame:
        try:
            df = ak.macro_china_cpi()
            if df.empty or '月份' not in df.columns:
                return pd.DataFrame()
            
            result = pd.DataFrame()
            result["date"] = df["月份"].apply(self.parse_chinese_date)
            
            col_name = "全国-同比增长"
            if col_name in df.columns:
                result["value"] = pd.to_numeric(df[col_name], errors="coerce")
            else:
                return pd.DataFrame()
            
            result = result.dropna()
            max_date = datetime(2025, 11, 30)
            result = result[result["date"] <= max_date]
            result = result.sort_values("date", ascending=False)
            return result
        except Exception as e:
            print(f"获取CPI数据失败: {e}")
            return pd.DataFrame()

    def fetch_pmi_data(self) -> pd.DataFrame:
        try:
            df = ak.macro_china_pmi()
            if df.empty or '月份' not in df.columns:
                return pd.DataFrame()
            
            result = pd.DataFrame()
            result["date"] = df["月份"].apply(self.parse_chinese_date)
            
            col_name = "制造业-指数"
            if col_name in df.columns:
                result["value"] = pd.to_numeric(df[col_name], errors="coerce")
            else:
                return pd.DataFrame()
            
            result = result.dropna()
            max_date = datetime(2025, 12, 31)
            result = result[result["date"] <= max_date]
            result = result.sort_values("date", ascending=False)
            return result
        except Exception as e:
            print(f"获取PMI数据失败: {e}")
            return pd.DataFrame()

    def fetch_m2_data(self) -> pd.DataFrame:
        try:
            df = ak.macro_china_m2_year()
            if df.empty:
                return pd.DataFrame()
            
            result = pd.DataFrame()
            for col in df.columns:
                if 'date' in str(col).lower() or '日期' in str(col):
                    result["date"] = pd.to_datetime(df[col], errors="coerce")
                elif 'm2' in str(col).lower():
                    result["value"] = pd.to_numeric(df[col], errors="coerce")
            
            if result.empty:
                result["value"] = df.iloc[:, 1]
            
            if "date" not in result.columns:
                result["date"] = pd.date_range(start='2020-01-01', periods=len(result), freq='YS')
            
            return result.dropna()
        except Exception as e:
            print(f"获取M2数据失败: {e}")
            return pd.DataFrame()

    def fetch_indicator_data(self, indicator_code: str, force_update: bool = False) -> pd.DataFrame:
        if not force_update:
            cached = self._load_from_cache(indicator_code)
            if cached is not None and not cached.empty:
                return cached

        fetch_methods = {
            "gdp": self.fetch_gdp_data,
            "cpi": self.fetch_cpi_data,
            "pmi": self.fetch_pmi_data,
            "m2": self.fetch_m2_data,
        }

        fetch_fn = fetch_methods.get(indicator_code)
        if fetch_fn:
            df = fetch_fn()
            if not df.empty:
                self._save_to_cache(indicator_code, df)
            return df

        return pd.DataFrame()

    def get_available_indicators(self) -> List[Dict]:
        return [
            {
                "code": "gdp",
                "name": "国内生产总值(GDP)",
                "category": "经济增长",
                "unit": "%",
                "description": "季度GDP同比增长率",
                "update_frequency": "季度",
            },
            {
                "code": "cpi",
                "name": "居民消费价格指数(CPI)",
                "category": "物价水平",
                "unit": "%",
                "description": "同比 CPI 涨跌幅",
                "update_frequency": "月度",
            },
            {
                "code": "pmi",
                "name": "采购经理指数(PMI)",
                "category": "经济景气",
                "unit": "",
                "description": "制造业PMI指数",
                "update_frequency": "月度",
            },
            {
                "code": "m2",
                "name": "广义货币(M2)",
                "category": "货币金融",
                "unit": "万亿元",
                "description": "M2货币供应量",
                "update_frequency": "月度",
            },
        ]


data_fetcher = DataFetcher()
