import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualize(inputPath):
    data = pd.read_csv(inputPath)
    data.drop(["Var_1","Segmentation","ID"],axis=1,inplace=True)
    data.set_index=False
    data.drop(columns=data.columns[0],inplace=True)
    gender(data)
    age(data)
    graduation(data)
    spending(data)
    family(data)
    profession(data)
    Ever_Married(data)
    HeatmapOfCountOfSpendingScoreByAgeAndGender(data)
    HeatmapOfCountOfSpendingScoreByProfessionAndMarriage(data)
    mappingTransform(data)
    heatmapOfEntireData(data)
    heatmapForSomeAttributes(data)
    boxPlots(data)
    GraduatedHist(data)
    scatterAgeXProfession(data)
    scatterAgeXSpendingScore(data)
    HeatmapOfMeanSpendingScore(data)

def gender(data):
    male = data.loc[data['Gender']=='Male'].count()[0]
    female = data.loc[data['Gender']=='Female'].count()[0]

    #pie chart
    plt.pie([male,female],autopct='%.2f%%',labels=['male','female'])
    plt.savefig("A:\MegaProject\VisualizationFigures\genderPieChart.png")
    plt.clf()

    #bar graph
    plt.bar(["Male","Female"],[male,female])
    plt.savefig("A:\MegaProject\VisualizationFigures\genderBarChart.png")
    plt.close()

def Ever_Married(data):
    #pie chart
    marriage_counts = data['Ever_Married'].value_counts()
    plt.pie(marriage_counts, labels=marriage_counts.index, autopct='%1.1f%%')
    plt.title('Marriage Distribution')
    plt.savefig("A:\MegaProject\VisualizationFigures\Marriagepie.png")
    plt.clf()

    #Bar Chart
    marriage_counts = data['Ever_Married'].value_counts()
    plt.bar(marriage_counts.index,marriage_counts.values)
    plt.title('Marriage Distribution')
    plt.savefig("A:\MegaProject\VisualizationFigures\MarriageBarChart.png")
    plt.close()

def age(data):
    age = data['Age']
    young = data.loc[age<19].count()[0]
    youngadults = data.loc[(age>18) & (age<30)].count()[0]
    adults = data.loc[(age>30) & (age<45)].count()[0]
    middleaged = data.loc[(age>45) & (age<65)].count()[0]
    senior = data.loc[age>65].count()[0]
    ages = [young,adults,youngadults,middleaged,senior]
    label = ['young','adults','youngadults','middleaged','senior']
    explodes=[0.2,0,0,0,0.3]

    ##Age Pie Chart
    plt.pie(ages,autopct='%.2f%%',labels=label,explode=explodes)
    plt.savefig("A:\MegaProject\VisualizationFigures\AgePieChart.png")
    plt.clf()

    ##Age Bar Chart
    plt.bar(label,ages)
    plt.savefig("A:\MegaProject\VisualizationFigures\AgebarGraph.png")
    plt.clf()

    #Age Box Plot
    plt.boxplot(data["Age"])
    plt.savefig("A:\MegaProject\VisualizationFigures\AgeBoxPlot.png")
    plt.close()

def graduation(data):
    grads = data.loc[data['Graduated']=='Yes'].count()[0]
    notgrad = data.loc[data['Graduated']=='No'].count()[0]
    grad = [grads,notgrad]
    label = ['grads','notgrad']

    ##Graduation Pie Chart
    plt.pie(grad,autopct='%.2f%%',labels=label)
    plt.savefig("A:\MegaProject\VisualizationFigures\GraduationPieChart.png")
    plt.clf()

    ##Graduation Bar graph
    plt.bar(label,grad)
    plt.savefig("A:\MegaProject\VisualizationFigures\GraduationBargraph.png")
    plt.close()

def spending(data):
    low = data.loc[data['Spending_Score']=='Low'].count()[0]
    high = data.loc[data['Spending_Score']=='High'].count()[0]
    average = data.loc[data['Spending_Score']=='Average'].count()[0]

    spending = [low,average,high]
    label = ['low','average','high']

    ## Spending Pie
    plt.pie(spending,autopct='%.2f%%',labels=label)
    plt.savefig("A:\MegaProject\VisualizationFigures\SpendingPie.png")
    plt.clf()

    ##Spending Bar
    plt.bar(label,spending)
    plt.savefig("A:\MegaProject\VisualizationFigures\SpendingBar.png")
    plt.close()

def family(data):
    individual = data.loc[data['Family_Size']=='1'].count()[0]
    small = data.loc[(data['Family_Size']>1) & (data['Family_Size']<4)].count()[0]
    average = data.loc[(data['Family_Size']>=4) & (data['Family_Size']<7)].count()[0]
    large = data.loc[data['Family_Size']>=7].count()[0]

    familySizes = [individual,small,average,large]
    labels = ["Individual","Small","Average","Large"]

    ##Family Size Pie
    plt.pie(familySizes,autopct='%.2f%%',labels=labels)
    plt.savefig("A:\MegaProject\VisualizationFigures\FamilyPie.png")
    plt.clf()

    ##Family Size Bar chart
    plt.bar(labels,familySizes)
    plt.savefig("A:\MegaProject\VisualizationFigures\FamilyBarChart.png")
    plt.clf()

    ##Family size hist
    plt.hist(data['Family_Size'])
    plt.savefig("A:\MegaProject\VisualizationFigures\FamilyHist.png")
    plt.close()

def profession(data):
    #pie chart
    profession_counts = data['Profession'].value_counts()
    plt.pie(profession_counts, labels=profession_counts.index, autopct='%1.1f%%')
    plt.title('Profession Distribution')
    plt.savefig("A:\MegaProject\VisualizationFigures\ProfessionPieChart.png")
    plt.clf()

    profession_counts = data["Profession"].value_counts()
    
    ##Bar plot
    profession_counts.plot(kind="bar")
    plt.savefig("A:\MegaProject\VisualizationFigures\ProfessionBarPlot.png")
    plt.clf()
    plt.close()

def mappingTransform(data):
    #One Hot Encoding
    mapping = {"No": 0, "Yes": 1}
    data["Ever_Married"] = data["Ever_Married"].map(mapping)
    data["Graduated"] = data["Graduated"].map(mapping)

    mapping = {"Female": 0, "Male": 1}
    data["Gender"] = data["Gender"].map(mapping)

    profession_mapping = {
        "Healthcare": 0,
        "Artist": 1,
        "Lawyer": 2,
        "Entertainment": 3,
        "Engineer": 4,
        "Executive": 5,
        "Doctor": 6,
        "Homemaker": 7,
        "Marketing": 8,
        "nan": 9
    }
    data['Profession'] = data['Profession'].map(profession_mapping)

    score_mapping = {
        'Low': 0,
        'Average': 1,
        'High': 2
    }

    data['Spending_Score'] = data['Spending_Score'].map(score_mapping)


def heatmapOfEntireData(data):
    ##HeatMap
    corr_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

    plt.savefig("A:\MegaProject\VisualizationFigures\HeatmapOfEntireData.png")
    plt.clf()
    plt.close()
   
def heatmapForSomeAttributes(data):
    # Calculate the correlation matrix
    corr_matrix = data[['Age','Spending_Score','Work_Experience','Family_Size']].corr()

    # Create a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.savefig("A:\MegaProject\VisualizationFigures\HeatmapOfSomeFeature.png")
    plt.clf()
    plt.close()    

def boxPlots(data):
    #spending score 
    data["Spending_Score"].plot(kind="box")
    plt.yticks([i for i in range(3)], ['Low', 'Average', 'High'])
    plt.savefig("A:\MegaProject\VisualizationFigures\SpendingSCoreBoxplot.png")
    plt.clf()

    #work experience
    data["Work_Experience"].plot(kind="box")
    plt.savefig("A:\MegaProject\VisualizationFigures\WorkExperienceBoxplot.png")
    plt.clf()

    #FamilySize
    data["Family_Size"].plot(kind="box")
    plt.savefig("A:\MegaProject\VisualizationFigures\FamilySizeBoxplot.png")
    plt.clf()

    #Profession
    data["Profession"].plot(kind="box")
    plt.yticks([i for i in range(9)], ['Healthcare', 'Artist', 'Lawyer', 'Entertainment', 'Engineer', 'Executive', 'Doctor', 'Homemaker', 'Marketing'])
    plt.savefig("A:\MegaProject\VisualizationFigures\ProfessionBoxplot.png")
    plt.clf()

    #Graduated
    data["Graduated"].plot(kind="box")
    plt.yticks([i for i in range(2)], ['Not Graduated', 'Graduated'])
    plt.savefig("A:\MegaProject\VisualizationFigures\GraduatedBoxplot.png")
    plt.clf()
    plt.close()

def GraduatedHist(data):
    data["Graduated"].plot(kind="hist")
    plt.xticks([i for i in range(2)], ['Not Graduated', 'Graduated'])
    plt.savefig("A:\MegaProject\VisualizationFigures\GraduatedHistogram.png")
    plt.clf()
    plt.close()

def scatterAgeXProfession(data):
    plt.scatter(x=data["Age"],y=data["Profession"])
    plt.yticks([i for i in range(9)], ['Healthcare', 'Artist', 'Lawyer', 'Entertainment', 'Engineer', 'Executive', 'Doctor', 'Homemaker', 'Marketing'])
    plt.savefig("A:\MegaProject\VisualizationFigures\ScatterAgeXProfession.png")
    plt.clf()
    plt.close()

def scatterAgeXSpendingScore(data):
    plt.scatter(y=data["Age"],x=data["Spending_Score"])

def HeatmapOfMeanSpendingScore(data):
    plt.figure(figsize=(50,80)) 
    mean_spending = data.groupby(['Age', 'Profession'])['Spending_Score'].mean().reset_index()
    pivot_table = mean_spending.pivot(index='Age', columns='Profession', values='Spending_Score')
    sns.heatmap(pivot_table, annot=True, fmt=".1f", linewidths=.5, square=True, cbar_kws={"orientation": "vertical"}, cmap='YlGnBu')
    plt.title('Heatmap of Mean Spending Score by Age and Profession')
    plt.xticks([i for i in range(9)], ['Healthcare', 'Artist', 'Lawyer', 'Entertainment', 'Engineer', 'Executive', 'Doctor', 'Homemaker', 'Marketing'])
    plt.savefig("A:\MegaProject\VisualizationFigures\HeatmapOfMeanSpendingScore.png")
    plt.clf()
    plt.close()

def HeatmapOfCountOfSpendingScoreByAgeAndGender(data):
    dataL = data[data['Age']<75]
    # Calculate the count of 'Spending Score' for each combination of 'Gender' and 'Age'
    count_spending = dataL.groupby(['Gender', 'Age'])['Spending_Score'].count().reset_index()

    # Create the pivot table
    pivot_table = count_spending.pivot(index='Age', columns=['Gender'], values='Spending_Score')

    # Fill NaN values with 0
    pivot_table = pivot_table.fillna(0)

    # Create the heatmap
    plt.figure(figsize=(50,80)) # Set the figure size
    sns.heatmap(pivot_table, annot=True, fmt="d", linewidths=.5, square=True, cbar_kws={"orientation": "vertical"}, cmap='YlGnBu',annot_kws={"fontsize": 30})
    plt.title('Heatmap of Count of Spending Score by Age and Gender',fontsize=20)
    plt.tick_params(axis='both', labelsize=20)
    plt.savefig("A:\MegaProject\VisualizationFigures\HeatmapOfCountOfSpendingScoreByAgeAndGender.png")
    plt.clf()
    plt.close()

def HeatmapOfCountOfSpendingScoreByProfessionAndMarriage(data):
    # Calculate the count of 'Spending Score' for each combination of 'Gender' and 'Age'
    count_spending = data.groupby(['Ever_Married', 'Profession'])['Spending_Score'].count().reset_index()

    # Create the pivot table
    pivot_table = count_spending.pivot(index='Profession', columns=['Ever_Married'], values='Spending_Score')

    # Fill NaN values with 0
    pivot_table = pivot_table.fillna(0)

    # Create the heatmap
    plt.figure(figsize=(50,80)) # Set the figure size
    sns.heatmap(pivot_table, annot=True, fmt="d", linewidths=2, square=True, cbar_kws={"orientation": "vertical"}, cmap='YlGnBu',annot_kws={"fontsize": 30})
    plt.tick_params(axis='both', labelsize=20)
    plt.title('Heatmap of Count of Spending Score by Age and Gender',fontsize=20)
    plt.savefig("A:\MegaProject\VisualizationFigures\HeatmapOfCountOfSpendingScoreByProfessionAndMarriage.png")
    plt.clf()
    plt.close()

if __name__ == "__main__":
    visualize("A:\\MegaProject\\Segmentation\\Normal Segmentation\\data.csv")
