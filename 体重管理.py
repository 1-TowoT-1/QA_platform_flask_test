import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# 读取或创建 CSV 数据
DATA_FILE = "fitness_data.csv"
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["date", "weight", "exercise", "calories_burned", "food", "calories_intake"])

# 应用标题
st.title("🏋️ 个人健身管理工具")

# 体重记录
st.header("📉 体重管理")
weight = st.number_input("输入今日体重 (kg)", min_value=30.0, max_value=150.0, step=0.1)
if st.button("记录体重"):
    new_data = pd.DataFrame({"date": [date.today()], "weight": [weight], "exercise": [""], "calories_burned": [0], "food": [""], "calories_intake": [0]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ 体重已记录！")

# 运动记录
st.header("🏃‍♂️ 运动记录")
exercise = st.text_input("输入运动类型 (如: 跑步, 健身)")
calories_burned = st.number_input("消耗卡路里 (kcal)", min_value=0, step=10)
if st.button("记录运动"):
    new_data = pd.DataFrame({"date": [date.today()], "weight": [None], "exercise": [exercise], "calories_burned": [calories_burned], "food": [""], "calories_intake": [0]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ 运动已记录！")

# 饮食记录
st.header("🍚 饮食记录")
food = st.text_input("输入食物名称")
calories_intake = st.number_input("摄入卡路里 (kcal)", min_value=0, step=10)
if st.button("记录饮食"):
    new_data = pd.DataFrame({"date": [date.today()], "weight": [None], "exercise": [""], "calories_burned": [0], "food": [food], "calories_intake": [calories_intake]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ 饮食已记录！")

# 数据可视化
st.header("📊 数据趋势")
df.dropna(subset=["weight"], inplace=True)
if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["weight"], marker="o", linestyle="-")
    plt.xlabel("date")
    plt.ylabel("weight (kg)")
    plt.title("Weight change trend")
    st.pyplot(plt)
