import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt



st.set_option('deprecation.showPyplotGlobalUse', False)
df = pd.read_csv("leaderboard.csv")
st.write(df)
# Create a copy of the data frame
df_comp = df.copy()

# Map the class values to their first letter
# df_comp["Class"] = df_comp["Class"].map(lambda x: x[0])

# Aggregate classes into class composition
sr_comp = df_comp.groupby("User_Addr")["Class"].apply(lambda x: x.sum())

# Convert series to dataframe
df_comp = pd.DataFrame(sr_comp)
df_comp = df_comp.reset_index()
df_comp["Class"] = df_comp["Class"].map(lambda x: ''.join(sorted(re.findall('[A-Z][^A-Z]*', x))))

# Show plot

plt.figure(figsize=(7, 6))
fig = df_comp["Class"].value_counts()[::-1].plot.barh(title="Top Team Compositions")
plt.show()
st.pyplot()


def top_card(df, cls):

    st.write("# Melhores cartas por classe")
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))


    df_class = df[df["Class"] == cls]
    df_class["Back"].value_counts()[::-1].plot.barh(title="Back (" + cls + ")", ax=axes[0,0])
    df_class["Mouth"].value_counts()[::-1].plot.barh(title="Mouth (" + cls + ")", ax=axes[0,1])
    df_class["Horn"].value_counts()[::-1].plot.barh(title="Horn (" + cls + ")", ax=axes[1,0])
    df_class["Tail"].value_counts()[::-1].plot.barh(title="Tail (" + cls + ")", ax=axes[1,1])
    plt.show()
    st.pyplot()
classes=["Aquatic","Beast","Plant","Bird","Bug","Mech","Dusk","Reptile"]
option = st.selectbox(
    'Escolha uma classe?',
    classes)



def visualize_combo(df, cls):
    fig, axes = plt.subplots(3, 2, figsize=(22, 15))
    st.write("# Melhores combos")
    df[df["Class"] == cls]["Back-Mouth"].value_counts()[5::-1].plot.barh(title="Back-Mouth (" + cls + ")", ax=axes[0,0])
    df[df["Class"] == cls]["Back-Horn"].value_counts()[5::-1].plot.barh(title="Back-Horn (" + cls + ")", ax=axes[0,1])
    df[df["Class"] == cls]["Back-Tail"].value_counts()[5::-1].plot.barh(title="Back-Tail (" + cls + ")", ax=axes[1,0])
    df[df["Class"] == cls]["Mouth-Horn"].value_counts()[5::-1].plot.barh(title="Mouth-Horn (" + cls + ")", ax=axes[1,1])
    df[df["Class"] == cls]["Mouth-Tail"].value_counts()[5::-1].plot.barh(title="Mouth-Tail (" + cls + ")", ax=axes[2,0])
    df[df["Class"] == cls]["Horn-Tail"].value_counts()[5::-1].plot.barh(title="Horn-Tail (" + cls + ")", ax=axes[2,1])
    plt.show()
    st.pyplot()

ability_cols = ["Back", "Mouth", "Horn", "Tail"]


def generate_card_pairs(row):
  for i in range(len(ability_cols)):
    for j in range(i + 1, len(ability_cols)):
      row[ability_cols[i] + "-" + ability_cols[j]] = row[ability_cols[i]] + " / " + row[ability_cols[j]]
  return row

def card_pairs(df):
  df = df.apply(generate_card_pairs, axis=1)
  df = df.drop(["Eyes", "Ears", "Back", "Mouth", "Horn", "Tail"], axis=1)
  return df

df_pairs = card_pairs(df)





def visualize_combo3(df, cls):
    st.write("# Top melhores 3 combos")
    fig, axes = plt.subplots(2, 2, figsize=(22, 10))

    df[df["Class"] == cls]["Back-Mouth-Horn"].value_counts()[5::-1].plot.barh(title="Back-Mouth-Horn (" + cls + ")", ax=axes[0,0])
    df[df["Class"] == cls]["Back-Mouth-Tail"].value_counts()[5::-1].plot.barh(title="Back-Mouth-Tail (" + cls + ")", ax=axes[0,1])
    df[df["Class"] == cls]["Back-Horn-Tail"].value_counts()[5::-1].plot.barh(title="Back-Horn-Tail (" + cls + ")", ax=axes[1,0])
    df[df["Class"] == cls]["Mouth-Horn-Tail"].value_counts()[5::-1].plot.barh(title="Mouth-Horn-Tail (" + cls + ")", ax=axes[1,1])
    plt.show()
    st.pyplot()

ability_cols = ["Back", "Mouth", "Horn", "Tail"]

def generate_card_combo(row):
  for i in range(len(ability_cols)):
    for j in range(i + 1, len(ability_cols)):
      for k in range(j + 1, len(ability_cols)):
        new_col = ability_cols[i] + "-" + ability_cols[j] + "-" + ability_cols[k]
        row[new_col] = row[ability_cols[i]] + " / " + row[ability_cols[j]] + " / " + row[ability_cols[k]]
  return row

def card_combo(df):
  df = df.apply(generate_card_combo, axis=1)
  df = df.drop(["Eyes", "Ears", "Back", "Mouth", "Horn", "Tail"], axis=1)
  return df

df_combo = card_combo(df)



def visualize_build(df):
    fig, axes = plt.subplots(7, 1, figsize=(13, 30))
    st.write("# Melhores builds")
    df[df["Class"] == "Aquatic"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Aquatic)", ax=axes[0])
    df[df["Class"] == "Beast"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Beast)", ax=axes[1])
    df[df["Class"] == "Plant"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Plant)", ax=axes[2])
    df[df["Class"] == "Bird"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Bird)", ax=axes[3])
    df[df["Class"] == "Bug"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Bug)", ax=axes[4])
    df[df["Class"] == "Reptile"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Reptile)", ax=axes[5])
    df[df["Class"] == "Dusk"]["Build"].value_counts()[10::-1].plot.barh(title="Build (Dusk)", ax=axes[6])
    plt.show()
    st.pyplot()
def generate_card_build(row):
  row["Build"] = row["Back"] + " / " + row["Mouth"] + " / " + row["Horn"] + " / " + row["Tail"]
  return row

def card_build(df):
  df = df.apply(generate_card_build, axis=1)
  df = df.drop(["Eyes", "Ears", "Back", "Mouth", "Horn", "Tail"], axis=1)
  return df

df_build = card_build(df)




top_card(df, option)
visualize_combo(df_pairs,option)
visualize_combo3(df_combo, option)
visualize_build(df_build)