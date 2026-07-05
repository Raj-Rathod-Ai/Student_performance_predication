# 🎓 Student GPA Predictor

An interactive, premium-designed Streamlit application that forecasts a student's Grade Point Average (GPA) using a pre-trained **K-Nearest Neighbors (KNN) Regression** model and scaler.

🔗 **Live Application URL**: [student-performance-predication.streamlit.app](https://student-performance-predication.streamlit.app/)

---

## ✨ Features

- **Interactive Q&A Questionnaire**: Friendly step-by-step form using text, select boxes, and radios instead of standard sliders.
- **Dual Scale Results**: Displays the predicted GPA on both the **4.0 Scale** and **10.0 Scale** (calculated as $GPA_{10} = GPA_{4} \times 2.5$).
- **What-If Optimization Analysis**: Dynamically calculates and displays potential GPA improvements if the student optimizes their study hours or eliminates absences.
- **Actionable Insights & Recommendations**: Renders personalized academic tips (e.g. tutoring support, target study hours) based on user inputs.
- **Premium Glassmorphic Design**: Clean dark theme utilizing HSL-tailored colors, smooth input hover/focus glow animations, and polished card layouts.

---

## 🛠️ Input Features used for Prediction

The ML model processes the following student attributes:
1. **Study Time Weekly**: Continuous numeric value representing hours spent studying per week.
2. **Absences**: Number of school absences (0 to 30 days).
3. **Tutoring Support**: Binary choice indicating whether the student receives external tutoring.
4. **Parental Support Level**: Level of parental involvement (None/Low/Medium/High/Very High).
5. **Extracurricular Activities**: Binary choice for extracurricular participation.
6. **Sports**: Binary choice indicating sports involvement.
7. **Music**: Binary choice for music activity participation.
8. **Grade Class**: Categorical grade level category (Class 0 to Class 4).

---

## 🚀 Local Installation & Running

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Raj-Rathod-Ai/Student_performance_predication.git
   cd Student_performance_predication
   ```

2. **Install dependencies**:
   Make sure you have python installed (Python 3.8+ recommended), then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Streamlit app**:
   ```bash
   python -m streamlit run app.py
   ```

---

## 📁 Repository Structure

- `app.py`: Main Streamlit app logic, layout, CSS injection, and predictive pipeline.
- `requirements.txt`: Package dependencies required to deploy/run the application.
- `knn_model.pkl`: Pre-trained K-Nearest Neighbors Regressor.
- `scaler.pkl`: Pre-trained StandardScaler used to normalize numerical features.
- `Student_performance_data.csv`: Source dataset used for training the model.
- `KNN_Reg_Que.ipynb`: Jupyter notebook containing model training and experimentation.
- `.gitignore`: Specifying untracked file configurations.
