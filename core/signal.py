from core.response import success
from strategies.indicators import get_indicators
from strategies.stage_engine import evaluate_stage


def signal(symbol):
    result = get_indicators(symbol)

    if not result["success"]:
        return result

    data = result["data"]
    stage_info = evaluate_stage(data)

    data["stage"] = stage_info["stage"]
    data["stage_label"] = stage_info["label"]
    data["direction"] = stage_info["direction"]
    data["checks"] = stage_info["checks"]

    return success(f"Signal for {data['symbol']}", data)
