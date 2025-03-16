import pandas as pd
import matplotlib.pyplot as plt

# file paths
file_paths = [
    #"/Users/suxinwan/Downloads/NGS数据/20240617-TSN20240617-0571-00019/ref1-3243/4.SNP_Analysis/2.all_sample/D6.csv",
    #"/Users/suxinwan/Downloads/NGS数据/20240617-TSN20240617-0571-00019/ref1-3243/4.SNP_Analysis/2.all_sample/D7.csv",
    #"/Users/suxinwan/Downloads/NGS数据/20240617-TSN20240617-0571-00019/ref1-3243/4.SNP_Analysis/2.all_sample/C5.csv"
    #"/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/C8.csv"
    "/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/B1.csv",
    "/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/B2.csv",
    "/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/B3.csv",
    "/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/B4.csv",
    "/Users/suxinwan/Downloads/NGS数据/20240718-TSN0571-00022PCR分析/ref1-3243/Customer_Result/4.SNP_Analysis/2.all_sample/B5.csv"
]

# Initialization DataFrame
combined_data = pd.DataFrame()

# combine data
for file_path in file_paths:
    data = pd.read_csv(file_path, header=1)  # setting header
    combined_data = pd.concat([combined_data, data], ignore_index=True)  # combine

# calculation frequency
def calculate_ratio(row):
    m_value, d_value, i_value = 0, 0, 0 
    
    for item in row['ratio'].split(";"):
        if item.startswith('M:'):
            m_values = item.split(":")[1].split(",")  
            m_value = sum([float(x) for x in m_values if x])
        elif item.startswith('D:'):
            d_values = item.split(":")[1].split(",")  
            d_value = sum([float(x) for x in d_values if x])
        elif item.startswith('I:'):
            i_values = item.split(":")[1].split(",")  
            i_value = sum([float(x) for x in i_values if x])
    
    return m_value + d_value + i_value  # 计算总和


combined_data['ratio'] = combined_data.apply(calculate_ratio, axis=1) * 100

# filter
filtered_data = combined_data[combined_data['ratio'] >= 0.001]


def convert_to_relative_location(original_location):
    return (original_location + 3112) 

filtered_data['relative_location'] = filtered_data['location'].apply(convert_to_relative_location)

# setting color
def color_code(row):
    if row['relative_location'] == 3243:
        return 'red'  # 3243 position
    else:
        return 'gray'  # color gray

filtered_data['color'] = filtered_data.apply(color_code, axis=1)

# plot PDF
plt.figure(figsize=(6, 3))
plt.scatter(
    filtered_data['relative_location'], 
    filtered_data['ratio'], 
    c=filtered_data['color'], 
    alpha=0.8, 
    #s=12, 
    edgecolors='none'  
)

ax = plt.gca()
ax.spines['top'].set_visible(False) 
ax.spines['right'].set_visible(False) 
plt.ylim(0, 110)
plt.xlabel('Position in the mitochondrial genome')
plt.ylabel('SNV frequency (%)')
plt.title('RMTS')

# save PDF
plt.savefig("0718-3243-RMTS.pdf", format="pdf", bbox_inches="tight", dpi=300)

#plt.show()