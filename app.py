import streamlit as st

st.set_page_config(page_title="阿根廷美客多本地店定价神器", page_icon="🇦🇷", layout="centered")

st.title("🇦🇷 Mercado Libre 阿根廷本地店定价计算器")
st.caption("基于高级合规抵税模型 · 确保 25% 稳健净毛利")
st.write("---")

# 1. 输入部分
st.subheader("📦 第一步：输入产品进货底价")
cost_x = st.number_input("请输入产品的单件进货成本 (ARS $, 不含税)", min_value=0.0, value=5000.0, step=500.0)

# 2. 核心计算逻辑 (完全遵循 ML成本核算.xlsx 的阶梯阀值映射)
# 阀值判定
if cost_x <= 5484.12:
    fixed_a = 1255.0
    price_y = (cost_x + 991.45) / 0.404723
    tier = "售价 0 - 15999 档 (低价区)"
elif cost_x <= 7738.35:
    fixed_a = 2500.0
    price_y = (cost_x + 1975.0) / 0.404723
    tier = "售价 16000 - 23999 档 (中价区)"
elif cost_x <= 10962.16:
    fixed_a = 3030.0
    price_y = (cost_x + 2393.7) / 0.404723
    tier = "售价 24000 - 33000 档 (高价区)"
else:
    fixed_a = 7500.0
    price_y = (cost_x + 5925.0) / 0.404723
    tier = "售价 ＞ 33000 档 (强包邮区)"

# 3. 成本与税费细节拆解
ml_commission = price_y * 0.15
withholding_tax = price_y * 0.08
monthly_tax = price_y * 0.06
net_invoice_cost = (price_y / 1.21 * 0.105) - 0.21 * (ml_commission + fixed_a)
target_profit = price_y * 0.25

# 4. 结果展示
st.subheader("🎯 第二步：智能定价与利润分析")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="🎯 建议美客多最终售价 (Y)", value=f"$ {price_y:,.2f} ARS")
with col2:
    st.metric(label="💰 预计每单净利润 (25%)", value=f"$ {target_profit:,.2f} ARS")

st.info(f"📌 **系统匹配物流档位**：{tier} | **固定操作费 (a)**：$ {fixed_a:,.2f} ARS")

# 5. 扣费明细账单
st.subheader("📊 第三步：每单扣费与税务预估明细")
st.write("当买家以此价格付款后，你的资金流动拆解如下：")

st.markdown(f"""
* 🛒 **平台基础扣费**：
    * **美客多销售佣金 (按15%估算)**：$ {ml_commission:,.2f} ARS
    * **平台固定操作/运费 (a)**：$ {fixed_a:,.2f} ARS
* 🏛️ **阿根廷实时税务预扣**：
    * **美客多后台实时预扣税 (8%)**：$ {withholding_tax:,.2f} ARS
    * **月末省市税务申报预留 (6%)**：$ {monthly_tax:,.2f} ARS
    * **抵扣后的净发票成本 (会计核算)**：$ {net_invoice_cost:,.2f} ARS
* 🔄 **最终资金回流**：
    * 扣除所有平台费、综合税负以及 **$ {cost_x:,.2f} ARS** 的进货本金后，你手里的纯利润刚好为售价的 **25%**。
""")

st.warning("⚠️ 提示：本工具默认你进货时能从供应商处取得合规的 Factura A 发票。如无法取得，进项税无法抵扣，利润将大幅下滑。")
