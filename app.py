import streamlit as st

st.set_page_config(page_title="美客多阿根廷全品类定价神器", page_icon="🇦🇷", layout="centered")

st.title("🇦🇷 Mercado Libre 阿根廷全品类精算定价器")
st.caption("2026最新美客多算法 · 动态匹配小件数码与大件重货双重物流矩阵")
st.write("---")

# 🌟 核心：在最上方增加商品类型切换
product_type = st.radio("🔮 请选择你要定价的商品类型：", ["📦 普通标准小件 (如：音箱、耳机、3C配件)", "🪑 大件/重货家具 (如：椅子、桌子、大件商品)"])
st.write("---")

# 1. 公共输入：产品入仓总成本
st.subheader("📦 第一步：输入核心成本参数")
cost_x = st.number_input("产品入仓总成本 (ARS $, 含头程海运清关税费)", min_value=0.0, value=15000.0, step=500.0)

# 2. 根据不同的商品类型，展示不同的物流计算逻辑
if product_type == "📦 普通标准小件 (如：音箱、耳机、3C配件)":
    st.info("💡 当前运行模式：标准小件模式。系统将根据最终售价自动匹配美客多小件固定费与免邮阶梯。")
    
    # 小件逻辑：根据进货价预测售价区间，锁定对应的固定费/运费 a
    if cost_x <= 5484.12:
        fixed_a = 1325.0  # 含税后的固定扣点
        tier = "预计售价 $0 - $15,999 档 (低价区固定费)"
    elif cost_x <= 7738.35:
        fixed_a = 2650.0
        tier = "预计售价 $16,000 - $25,999 档 (中价区固定费)"
    elif cost_x <= 10130.0:
        fixed_a = 3180.0
        tier = "预计售价 $25,000 - $33,000 档 (高价区固定费)"
    else:
        fixed_a = 7500.0  # 突破33000，免固定费，强制转为小件全阿包邮平均运费
        tier = "预计售价 ＞ $33,000 档 (强制免邮区)"

else:
    st.info("💡 当前运行模式：大件重货模式。系统将强制启用 Mercado Envíos Pesados 大件物流矩阵。")
    
    col_dim1, col_dim2 = st.columns(2)
    with col_dim1:
        shop_status = st.selectbox("你的店铺信誉等级（大件关键：决定运费折扣）", ["绿标/金牌卖家 (享受50%运费补贴)", "新店/无等级 (无补贴，全额负担)"])
        real_weight = st.number_input("产品打包后实际重量 (kg)", min_value=0.1, value=20.0, step=1.0)
    with col_dim2:
        v_length = st.number_input("外包装长 (cm)", min_value=1.0, value=80.0)
        v_width = st.number_input("外包装宽 (cm)", min_value=1.0, value=60.0)
        v_height = st.number_input("外包装高 (cm)", min_value=1.0, value=40.0)
    
    # 大件计费重量计算：实际重量 vs 体积重量 取大者
    volume_weight = (v_length * v_width * v_height) / 5000.0
    charge_weight = max(real_weight, volume_weight)
    
    # 2026最新大件阶梯基础运费
    if charge_weight <= 5:
        base_shipping = 6500.0
    elif charge_weight <= 15:
        base_shipping = 14000.0
    elif charge_weight <= 30:
        base_shipping = 26000.0
    elif charge_weight <= 50:
        base_shipping = 42000.0
    else:
        base_shipping = 65000.0
        
    # 根据店铺颜色看最终卖家出多少运费
    if "绿标" in shop_status:
        fixed_a = base_shipping * 0.5
    else:
        fixed_a = base_shipping * 1.0
        
    tier = f"大件计费重量 {charge_weight:.2f} kg (实际 {real_weight}kg / 体积折算 {volume_weight:.2f}kg)"

# 3. 核心精算公式统一输出 (锁定 25% 净毛利等式)
# 公式：Y = (X + 0.79 * a) / 0.404723
price_y = (cost_x + 0.79 * fixed_a) / 0.404723
target_profit = price_y * 0.25

# 4. 结果前端展示
st.write("---")
st.subheader("🎯 第二步：智能定价与利润分析")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="🎯 建议美客多最终售价 (Y)", value=f"$ {price_y:,.2f} ARS")
with col_res2:
    st.metric(label="💰 锁定 25% 纯利润落袋", value=f"$ {target_profit:,.2f} ARS")

st.success(f"📌 **当前物流判定明细**：{tier} \n\n平台单件扣费/实际承担运费 (a)：**$ {fixed_a:,.2f} ARS**")
