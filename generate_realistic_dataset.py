"""
Script tao bo du lieu sinh vien "thuc te"
Quy tac logic dua tren dac diem sinh vien de de xuat khoa hoc phu hop
"""

import pandas as pd
import numpy as np
import random
import uuid

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================
# DINH NGHIA CAC GIA TRI
# ============================================================

INTEREST_FIELDS = ['AI/Data', 'Web', 'Mobile App', 'Game', 'IOT', 'Office']
CAREER_GOALS = ['Company', 'Freelancer', 'Startup', 'Competition']
STUDY_TIMES = ['< 2h', '2-5h', '5-10h', '> 10h']
CURRENT_LEVELS = ['Beginner', 'Intermediate', 'Advanced']

# Cac khoa hoc co the de xuat
COURSES = [
    # AI/Data courses
    'Python Basic',
    'Python for Data Science',
    
    # Web courses
    'Frontend (HTML/CSS/JS)',
    'Web Backend (PHP/Nodejs)',
    'Fullstack Web (MERN)',
    
    # Mobile App courses
    'Android Basic',
    'Flutter Cross-platform',
    
    # Game courses
    'Scratch for Beginners',
    'Game Design & Art',
    'Game Dev (Unity/C#)',
    
    # IOT courses
    'Arduino Basic',
    'C/C++ for IoT',
    
    # Office courses
    'Tin hoc van phong',
    
    # Competition
    'Competitive Programming (C++)'
]

# ============================================================
# QUY TAC LOGIC DE XUAT KHOA HOC
# ============================================================

def recommend_course(logic_score, math_score, art_score, english_score,
                     interest_field, career_goal, study_time, current_level):
    """
    De xuat khoa hoc dua tren cac dac diem cua sinh vien
    Quy tac duoc thiet ke de mo phong thuc te
    """
    
    # Tinh diem trung binh
    avg_score = (logic_score + math_score + art_score + english_score) / 4
    tech_score = (logic_score + math_score) / 2  # Diem ky thuat
    creative_score = (art_score + english_score) / 2  # Diem sang tao
    
    # Xac dinh muc do hoc tap
    is_beginner = current_level == 'Beginner'
    is_intermediate = current_level == 'Intermediate'
    is_advanced = current_level == 'Advanced'
    
    # Xac dinh thoi gian hoc
    has_little_time = study_time in ['< 2h', '2-5h']
    has_much_time = study_time in ['5-10h', '> 10h']
    
    # Xac dinh muc tieu nghe nghiep
    wants_competition = career_goal == 'Competition'
    wants_company = career_goal == 'Company'
    wants_freelance = career_goal == 'Freelancer'
    wants_startup = career_goal == 'Startup'
    
    # ============================================================
    # QUY TAC CHO TUNG LINH VUC QUAN TAM
    # ============================================================
    
    # ---- AI/Data ----
    if interest_field == 'AI/Data':
        if wants_competition and logic_score >= 7 and math_score >= 7:
            return 'Competitive Programming (C++)'
        elif is_advanced and math_score >= 7 and has_much_time:
            return 'Python for Data Science'
        elif is_intermediate and tech_score >= 6:
            return 'Python for Data Science'
        elif is_beginner or tech_score < 6:
            return 'Python Basic'
        else:
            return 'Python Basic'
    
    # ---- Web ----
    elif interest_field == 'Web':
        if wants_competition and logic_score >= 7:
            if math_score >= 7:
                return 'Competitive Programming (C++)'
            else:
                return 'Fullstack Web (MERN)'
        elif is_advanced and has_much_time:
            return 'Fullstack Web (MERN)'
        elif is_intermediate:
            if tech_score >= 6:
                return 'Web Backend (PHP/Nodejs)'
            else:
                return 'Frontend (HTML/CSS/JS)'
        elif is_beginner:
            if art_score >= 7:
                return 'Frontend (HTML/CSS/JS)'
            else:
                return 'Web Backend (PHP/Nodejs)'
        else:
            return 'Frontend (HTML/CSS/JS)'
    
    # ---- Mobile App ----
    elif interest_field == 'Mobile App':
        if wants_competition and logic_score >= 8 and math_score >= 7:
            return 'Competitive Programming (C++)'
        elif is_advanced or (is_intermediate and tech_score >= 6):
            return 'Flutter Cross-platform'
        elif is_beginner:
            if logic_score >= 5:
                return 'Flutter Cross-platform'
            else:
                return 'Android Basic'
        else:
            return 'Android Basic'
    
    # ---- Game ----
    elif interest_field == 'Game':
        if wants_competition and logic_score >= 8 and math_score >= 7:
            return 'Competitive Programming (C++)'
        elif is_advanced and tech_score >= 6:
            return 'Game Dev (Unity/C#)'
        elif is_intermediate:
            if art_score >= 7:
                return 'Game Design & Art'
            elif logic_score >= 6:
                return 'Game Dev (Unity/C#)'
            else:
                return 'Scratch for Beginners'
        elif is_beginner:
            if art_score >= 7 and creative_score >= 6:
                return 'Game Design & Art'
            elif logic_score >= 6:
                return 'Game Dev (Unity/C#)'
            else:
                return 'Scratch for Beginners'
        else:
            return 'Scratch for Beginners'
    
    # ---- IOT ----
    elif interest_field == 'IOT':
        if wants_competition and logic_score >= 8 and math_score >= 7:
            return 'Competitive Programming (C++)'
        elif is_advanced and tech_score >= 7:
            return 'C/C++ for IoT'
        elif is_intermediate:
            if logic_score >= 7 or tech_score >= 6:
                return 'C/C++ for IoT'
            else:
                return 'Arduino Basic'
        elif is_beginner:
            if logic_score >= 7:
                return 'C/C++ for IoT'
            else:
                return 'Arduino Basic'
        else:
            return 'Arduino Basic'
    
    # ---- Office ----
    elif interest_field == 'Office':
        if wants_competition and logic_score >= 8 and math_score >= 7:
            return 'Competitive Programming (C++)'
        else:
            return 'Tin hoc van phong'
    
    # Default
    return 'Python Basic'


def add_realistic_noise(course, interest_field, current_level, noise_level=0.15):
    """
    Them nhieu vao du lieu de mo phong thuc te
    Khong phai luc nao sinh vien cung chon khoa hoc toi uu
    """
    if random.random() > noise_level:
        return course
    
    # Cac khoa hoc thay the co the xay ra
    alternatives = {
        'AI/Data': ['Python Basic', 'Python for Data Science'],
        'Web': ['Frontend (HTML/CSS/JS)', 'Web Backend (PHP/Nodejs)', 'Fullstack Web (MERN)'],
        'Mobile App': ['Android Basic', 'Flutter Cross-platform'],
        'Game': ['Scratch for Beginners', 'Game Design & Art', 'Game Dev (Unity/C#)'],
        'IOT': ['Arduino Basic', 'C/C++ for IoT'],
        'Office': ['Tin hoc van phong']
    }
    
    # Chon ngau nhien tu cac khoa hoc cung linh vuc
    alt_courses = alternatives.get(interest_field, [course])
    return random.choice(alt_courses)


def generate_realistic_scores(interest_field, current_level):
    """
    Tao diem so thuc te hon dua tren linh vuc quan tam va trinh do
    """
    # Base scores dua tren level
    if current_level == 'Advanced':
        base_min, base_max = 5, 10
    elif current_level == 'Intermediate':
        base_min, base_max = 3, 9
    else:  # Beginner
        base_min, base_max = 1, 8
    
    # Tao diem co xu huong dua tren linh vuc
    if interest_field == 'AI/Data':
        logic_score = np.random.randint(max(base_min, 4), base_max + 1)
        math_score = np.random.randint(max(base_min, 4), base_max + 1)
        art_score = np.random.randint(base_min, min(base_max, 8))
        english_score = np.random.randint(base_min, base_max + 1)
    
    elif interest_field == 'Web':
        logic_score = np.random.randint(base_min, base_max + 1)
        math_score = np.random.randint(base_min, base_max + 1)
        art_score = np.random.randint(max(base_min, 3), base_max + 1)
        english_score = np.random.randint(base_min, base_max + 1)
    
    elif interest_field == 'Mobile App':
        logic_score = np.random.randint(max(base_min, 3), base_max + 1)
        math_score = np.random.randint(base_min, base_max + 1)
        art_score = np.random.randint(base_min, base_max + 1)
        english_score = np.random.randint(base_min, base_max + 1)
    
    elif interest_field == 'Game':
        logic_score = np.random.randint(base_min, base_max + 1)
        math_score = np.random.randint(base_min, base_max + 1)
        art_score = np.random.randint(max(base_min, 4), base_max + 1)  # Game can art
        english_score = np.random.randint(base_min, base_max + 1)
    
    elif interest_field == 'IOT':
        logic_score = np.random.randint(max(base_min, 3), base_max + 1)
        math_score = np.random.randint(max(base_min, 3), base_max + 1)
        art_score = np.random.randint(base_min, min(base_max, 7))
        english_score = np.random.randint(base_min, base_max + 1)
    
    else:  # Office
        logic_score = np.random.randint(base_min, base_max + 1)
        math_score = np.random.randint(base_min, base_max + 1)
        art_score = np.random.randint(base_min, base_max + 1)
        english_score = np.random.randint(base_min, base_max + 1)
    
    return logic_score, math_score, art_score, english_score


def generate_realistic_dataset(n_samples=10000, noise_level=0.15):
    """
    Tao bo du lieu thuc te
    """
    print("=" * 60)
    print("TAO BO DU LIEU SINH VIEN THUC TE")
    print("=" * 60)
    print(f"So luong mau: {n_samples}")
    print(f"Muc do nhieu: {noise_level * 100}%")
    
    data = []
    
    # Phan bo linh vuc quan tam (khong deu)
    interest_weights = {
        'AI/Data': 0.20,      # 20% quan tam AI/Data
        'Web': 0.18,          # 18% quan tam Web
        'Mobile App': 0.15,   # 15% quan tam Mobile
        'Game': 0.17,         # 17% quan tam Game
        'IOT': 0.12,          # 12% quan tam IOT
        'Office': 0.18        # 18% quan tam Office
    }
    
    # Phan bo career goal (khong deu)
    career_weights = {
        'Company': 0.35,      # 35% muon lam o cong ty
        'Freelancer': 0.25,   # 25% muon freelance
        'Startup': 0.25,      # 25% muon startup
        'Competition': 0.15   # 15% muon thi dau
    }
    
    # Phan bo thoi gian hoc (khong deu)
    time_weights = {
        '< 2h': 0.25,
        '2-5h': 0.35,
        '5-10h': 0.25,
        '> 10h': 0.15
    }
    
    # Phan bo trinh do (khong deu)
    level_weights = {
        'Beginner': 0.45,
        'Intermediate': 0.35,
        'Advanced': 0.20
    }
    
    for i in range(n_samples):
        # Tao ID
        student_id = str(uuid.uuid4())[:8]
        
        # Chon cac thuoc tinh theo phan bo trong so
        interest_field = random.choices(
            list(interest_weights.keys()), 
            weights=list(interest_weights.values())
        )[0]
        
        career_goal = random.choices(
            list(career_weights.keys()),
            weights=list(career_weights.values())
        )[0]
        
        study_time = random.choices(
            list(time_weights.keys()),
            weights=list(time_weights.values())
        )[0]
        
        current_level = random.choices(
            list(level_weights.keys()),
            weights=list(level_weights.values())
        )[0]
        
        # Tao diem so thuc te
        logic_score, math_score, art_score, english_score = generate_realistic_scores(
            interest_field, current_level
        )
        
        # De xuat khoa hoc dua tren quy tac logic
        recommended_course = recommend_course(
            logic_score, math_score, art_score, english_score,
            interest_field, career_goal, study_time, current_level
        )
        
        # Them nhieu de mo phong thuc te
        final_course = add_realistic_noise(
            recommended_course, interest_field, current_level, noise_level
        )
        
        data.append({
            'id': student_id,
            'logic_score': logic_score,
            'math_score': math_score,
            'art_score': art_score,
            'english_score': english_score,
            'interest_field': interest_field,
            'career_goal': career_goal,
            'study_time_per_week': study_time,
            'current_level': current_level,
            'Target_Course': final_course
        })
    
    df = pd.DataFrame(data)
    
    # In thong ke
    print("\n" + "-" * 60)
    print("THONG KE DU LIEU")
    print("-" * 60)
    
    print("\n[1] Phan bo linh vuc quan tam:")
    for field, count in df['interest_field'].value_counts().items():
        print(f"    {field}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n[2] Phan bo muc tieu nghe nghiep:")
    for goal, count in df['career_goal'].value_counts().items():
        print(f"    {goal}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n[3] Phan bo trinh do hien tai:")
    for level, count in df['current_level'].value_counts().items():
        print(f"    {level}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n[4] Phan bo thoi gian hoc/tuan:")
    for time, count in df['study_time_per_week'].value_counts().items():
        print(f"    {time}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n[5] Phan bo khoa hoc duoc de xuat:")
    for course, count in df['Target_Course'].value_counts().items():
        print(f"    {course}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\n[6] Thong ke diem so:")
    print(df[['logic_score', 'math_score', 'art_score', 'english_score']].describe())
    
    return df


def validate_dataset(df):
    """
    Kiem tra tinh hop le cua du lieu
    """
    print("\n" + "=" * 60)
    print("KIEM TRA TINH HOP LE CUA DU LIEU")
    print("=" * 60)
    
    # Kiem tra missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("[WARN] Co missing values:")
        print(missing[missing > 0])
    else:
        print("[OK] Khong co missing values")
    
    # Kiem tra diem so trong khoang hop le
    for col in ['logic_score', 'math_score', 'art_score', 'english_score']:
        min_val = df[col].min()
        max_val = df[col].max()
        if min_val >= 1 and max_val <= 10:
            print(f"[OK] {col}: {min_val} - {max_val}")
        else:
            print(f"[WARN] {col}: {min_val} - {max_val} (ngoai khoang 1-10)")
    
    # Kiem tra cac gia tri categorical
    print(f"\n[OK] interest_field: {df['interest_field'].nunique()} gia tri")
    print(f"[OK] career_goal: {df['career_goal'].nunique()} gia tri")
    print(f"[OK] study_time_per_week: {df['study_time_per_week'].nunique()} gia tri")
    print(f"[OK] current_level: {df['current_level'].nunique()} gia tri")
    print(f"[OK] Target_Course: {df['Target_Course'].nunique()} gia tri")
    
    return True


def main():
    """
    Main function
    """
    # Tao du lieu voi 15% nhieu (giau dong thuc te)
    df = generate_realistic_dataset(n_samples=10000, noise_level=0.15)
    
    # Kiem tra tinh hop le
    validate_dataset(df)
    
    # Luu file
    output_path = 'dataset_10000_students_realistic.csv'
    df.to_csv(output_path, index=False)
    print(f"\n[SAVED] Da luu du lieu vao: {output_path}")
    
    # Tao them 1 file backup cua du lieu cu
    print("\n[INFO] Luu y: Du lieu cu da duoc giu nguyen tai 'dataset_10000_students.csv'")
    
    return df


if __name__ == "__main__":
    df = main()
    print("\n[DONE] Hoan tat tao bo du lieu!")
