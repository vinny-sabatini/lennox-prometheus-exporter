def extract_timestamp(metric_time):
    if metric_time is None:
        return 0
    return metric_time.timestamp()


def set_value_or_zero(metric) -> int:
    if metric is None:
        return 0
    return metric
