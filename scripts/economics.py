#!/usr/bin/env python3
"""Single-round contract arithmetic. No legal or enforceability conclusions."""
import argparse
import json
from decimal import Decimal, InvalidOperation, localcontext


def number(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("请输入有限十进制数。") from None
    if not result.is_finite():
        raise ValueError("不接受 NaN 或 Infinity。")
    return result


def nonnegative(value):
    result = number(value)
    if result < 0:
        raise ValueError("金额、利率和期间不能为负。")
    return result


def positive(value):
    result = nonnegative(value)
    if result == 0:
        raise ValueError("该参数必须大于零。")
    return result


def redemption(principal, rate, days, dividends=0, fees=0, penalty=0):
    """Actual unrecovered principal, simple ACT/365, agreed fee assumptions."""
    p, r, d, div, f, pen = map(
        nonnegative, (principal, rate, days, dividends, fees, penalty)
    )
    interest = p * r * d / Decimal(365)
    gross = p + interest + f + pen
    return {
        "principal": p, "simple_interest": interest,
        "fees_assumed": f, "penalty_assumed": pen, "deduction": div,
        "contract_claim_before_caps": max(Decimal(0), gross - div),
    }


def liquidation(investment, share, proceeds, multiple=1, participating=False):
    """Proceeds must already be net of creditors, taxes and deal costs."""
    p, s, v, m = map(nonnegative, (investment, share, proceeds, multiple))
    if not Decimal(0) < s <= Decimal(1):
        raise ValueError("持股比例必须大于 0 且不超过 1。")
    preference = min(v, p * m)
    ordinary = v * s
    if participating:
        investor = preference + (v - preference) * s
    else:
        investor = max(preference, ordinary)
    return {
        "preference_paid": preference,
        "as_converted_value": ordinary,
        "investor_distribution": investor,
        "other_shareholders_total": v - investor,
    }


def antidilution(old_price, existing_diluted_shares, new_money, new_price):
    """Broad-based weighted-average illustration; exact denominator is assumed."""
    old, a, cash, new = map(
        positive, (old_price, existing_diluted_shares, new_money, new_price)
    )
    b, c = cash / old, cash / new
    adjusted = old if new >= old else old * (a + b) / (a + c)
    return {
        "b_new_money_at_old_price": b, "c_actual_new_shares": c,
        "weighted_average_price": adjusted,
        "full_ratchet_price": min(old, new),
    }


def main():
    parser = argparse.ArgumentParser(
        description="单轮简化测算，金额使用同一币种；仅计算合同假设，不判断效力或执行。"
    )
    subs = parser.add_subparsers(dest="mode", required=True)
    red = subs.add_parser("redemption", help="单利回购；ACT/365，不支持复利和分批本金")
    red.add_argument("--principal", required=True, help="实际未回收本金")
    red.add_argument("--rate", required=True, help="小数年率，例如 0.08")
    red.add_argument("--days", required=True)
    red.add_argument("--dividends", default="0", help="约定扣减的已分红")
    red.add_argument("--fees", default="0", help="假设可计入的费用，不代表法院支持")
    red.add_argument("--penalty", default="0", help="仅在合同允许且不重复计算时输入")
    liq = subs.add_parser("liquidation", help="单轮清算分配；参与型无封顶，其他股东合计")
    liq.add_argument("--investment", required=True)
    liq.add_argument("--share", required=True, help="完全转换后持股比例，例如 0.2")
    liq.add_argument("--proceeds", required=True, help="扣债务税费后可分给股东的金额")
    liq.add_argument("--multiple", default="1")
    liq.add_argument("--participating", action="store_true")
    anti = subs.add_parser("antidilution", help="广义加权平均与完全棘轮价格对比")
    anti.add_argument("--old-price", required=True)
    anti.add_argument("--existing-diluted-shares", required=True)
    anti.add_argument("--new-money", required=True)
    anti.add_argument("--new-price", required=True)
    args = vars(parser.parse_args())
    mode = args.pop("mode")
    try:
        with localcontext() as ctx:
            ctx.prec = 40
            result = globals()[mode](**args)
    except (ValueError, InvalidOperation) as exc:
        parser.error(str(exc))
    print(json.dumps({
        "mode": mode,
        "basis": "single-round illustration; no enforceability opinion",
        "result": result,
    }, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
