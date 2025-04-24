import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings 
warnings.filterwarnings("ignore")
df=pd.read_csv('D:/DA2025/Data for analysis/sales_data2703.csv')
#Printing top 10 rows of the dataset
print(df.head(10)) 
# Checking the size of the dataframe
print(df.shape)
#Printing the dataframe information
print(df.info())
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
#Checking the data type order date and ship date whether it has changed to datetime or not
print(df[['Order Date', 'Ship Date']].dtypes)
# Checkig the missing values (NaN or Null)
print(df.isnull().sum())
#output shows that Postal Code has 11 null values
print(df[df['Postal Code'].isnull()])

null_postal_data = df[df['Postal Code'].isnull()][['Region', 'Postal Code']]
print(null_postal_data)
#Let's assign the postal code to the missing region
df['Postal Code'] = df['Postal Code'].fillna(5401) 
#Checking if there are any null vlues or not
print(df.isnull().sum())
print(df.describe())

#Dropping the rowID column and setting the OrderDate as an Index
#rowID column duplicated the built-in Pandas Data Frame Index
df.drop('Row ID',axis = 1, inplace = True)
df.set_index("Order Date", inplace = True)
print(df.describe())

#ANALYSIS
# tOP 10 cities by sales
top_cities_bySales=df.groupby('City')['Sales'].sum().nlargest(10).reset_index()
print(top_cities_bySales)
plt.figure(figsize=(12, 8))  
ax = sns.barplot(x="Sales", y="City", data=top_cities_bySales, palette="flare_r", edgecolor="black", linewidth=0.4)  
ax.bar_label(ax.containers[0], 
             labels=[f"${x:,.2f}" for x in top_cities_bySales['Sales']],
             fontsize=8,
             padding=3)
plt.title("Top 10 Cities by Sales Performance", 
          fontsize=14, pad=20, fontweight='bold')
plt.xlabel("Total Revenue (USD)", fontsize=10, labelpad=10)
plt.ylabel("")  
plt.xticks(fontsize=9)
plt.yticks(fontsize=9) 
plt.tight_layout()
plt.show()

#Top 10 states by Sales
top_states_bySales=df.groupby('State')['Sales'].sum().nlargest(10).reset_index()
print(top_states_bySales)
plt.figure(figsize=(12, 8))  
ax = sns.barplot(x="Sales", y="State", data=top_states_bySales, palette="rocket", edgecolor="black", linewidth=0.4)  
ax.bar_label(ax.containers[0], 
             labels=[f"${x:,.2f}" for x in top_states_bySales['Sales']],
             fontsize=8,
             padding=3)
plt.title("Top 10 States by Sales Performance", 
          fontsize=14, pad=20, fontweight='bold')
plt.xlabel("Total Revenue (USD)", fontsize=10, labelpad=10)
plt.ylabel("")  
plt.xticks(fontsize=9)
plt.yticks(fontsize=9) 
plt.tight_layout()
plt.show()

#Revenue sales by category
revenue_by_category=df.groupby('Category')['Sales'].sum()
print(revenue_by_category)
plt.figure(figsize=(8,8))
wedges, texts, autotexts = plt.pie(
    revenue_by_category,
    labels=revenue_by_category.index,
     autopct=lambda p: f'${p*sum(revenue_by_category)/100:,.0f}\n({p:.1f}%)',
    startangle=90,
    explode=(0.03, 0.03, 0.03),  # Slight separation
    textprops={'fontsize': 10}
)
plt.axis('equal')
plt.title('Revenue Distribution by Product Category', 
          fontsize=16, pad=20, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
legend_labels = [f'{cat}: ${val:,.0f}' 
                for cat, val in zip(revenue_by_category.index, revenue_by_category)]
plt.legend(wedges, legend_labels,
           title="Total Revenue",
           loc="center left",
           bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.show()

#Revenue by sub-category
revenue_by_subcategory=df.groupby('Sub-Category')['Sales'].sum().nlargest(10).reset_index()
print(revenue_by_subcategory)
plt.figure(figsize=(12, 8))  
ax = sns.barplot(x="Sales", y="Sub-Category", data=revenue_by_subcategory, palette="crest_r", edgecolor="black", linewidth=0.4)  
ax.bar_label(ax.containers[0], 
             labels=[f"${x:,.2f}" for x in revenue_by_subcategory['Sales']],
             fontsize=8,
             padding=3)
plt.title("Top 10 Sub-categories by Sales Performance", 
          fontsize=14, pad=20, fontweight='bold')
plt.xlabel("Total Revenue (USD)", fontsize=10, labelpad=10)
plt.ylabel("Sub-Category")  
plt.xticks(fontsize=9)
plt.yticks(fontsize=9) 
plt.tight_layout()
plt.show()

#Top 5 sub-categories by sales in any one state , say Alabama
print('Top 5 sub-categories by sales in Alabama state')
Top5_SubcategorySales_Alabama = (
    df[df['State'] == 'Alabama']  # Filter for Alabama only
    .groupby('Sub-Category')['Sales']
    .sum()
    .reset_index()
    .sort_values('Sales', ascending=False)
    .head(5)
)
print(Top5_SubcategorySales_Alabama)


# Let's find the total yearly sales
print('Total Sales per Year')
yearly_sales = df['Sales'].resample('Y').sum()
yearly_sales.index = yearly_sales.index.year
print(yearly_sales)
plt.figure(figsize=(10,8))
yearly_sales.plot(kind='bar',color='blue')
plt.title('Total Sales by Year', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.tight_layout()
plt.show()

#Monthly sales for any particular year, let's say 2018
monthly_sales_2018=df['Sales'].loc['2018'].resample('m').sum()
monthly_sales_2018.index = monthly_sales_2018.index.strftime('%B')
print(monthly_sales_2018)

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales_2018.index, monthly_sales_2018.values, marker='o', linestyle='-', color='b')

plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Monthly Sales for 2018")
plt.xticks(rotation=45)  
plt.grid(True)
plt.tight_layout()
plt.show()

#sale of any specific sub-category over the months in a specific year
#sale of phones per month in the year 2017
print('Monthly phone sales in the year 2017')
phones_2017 = df[(df['Sub-Category'] == 'Phones') & (df.index.year == 2017)]
monthly_phones_sales_2017 = phones_2017['Sales'].resample('M').sum()
monthly_phones_sales_2017.index = monthly_phones_sales_2017.index.strftime('%B')
print(monthly_phones_sales_2017)
plt.figure(figsize=(10, 5))
plt.plot(monthly_phones_sales_2017.index, monthly_phones_sales_2017.values, marker='o', color='green')
plt.title('Monthly Sales of Phones in 2017')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()