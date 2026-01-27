"""
Script để load model đã train và dự đoán trên dữ liệu mới
"""

import pandas as pd
import numpy as np
import joblib
import os

MODEL_DIR = 'model_output'

def load_model_and_encoders():
    """
    Load model và encoders đã lưu
    """
    print("=" * 50)
    print("LOAD MODEL VÀ ENCODERS")
    print("=" * 50)
    
    # Load model
    model_path = os.path.join(MODEL_DIR, 'decision_tree_model.joblib')
    model = joblib.load(model_path)
    print(f"✓ Đã load model từ: {model_path}")
    
    # Load encoders
    encoders_path = os.path.join(MODEL_DIR, 'encoders.joblib')
    encoders = joblib.load(encoders_path)
    print(f"✓ Đã load encoders từ: {encoders_path}")
    
    # Load feature info
    feature_info_path = os.path.join(MODEL_DIR, 'feature_info.joblib')
    feature_info = joblib.load(feature_info_path)
    print(f"✓ Đã load feature info từ: {feature_info_path}")
    
    print(f"\n📊 Thông tin model:")
    print(f"  • Training date: {feature_info['training_date']}")
    print(f"  • Số classes: {feature_info['n_classes']}")
    print(f"  • Classes: {feature_info['classes']}")
    
    return model, encoders, feature_info

def preprocess_new_data(df, encoders, feature_info):
    """
    Tiền xử lý dữ liệu mới
    """
    # Lấy các cột cần thiết
    feature_cols = feature_info['feature_columns']
    categorical_cols = feature_info['categorical_cols']
    
    X = df[feature_cols].copy()
    
    # Encode categorical features
    for col in categorical_cols:
        if col in encoders:
            # Xử lý các giá trị mới chưa thấy trong training
            known_values = set(encoders[col].classes_)
            X[col] = X[col].apply(lambda x: x if x in known_values else encoders[col].classes_[0])
            X[col] = encoders[col].transform(X[col])
    
    return X

def predict_single(model, encoders, feature_info, 
                   logic_score, math_score, art_score, english_score,
                   interest_field, career_goal, study_time_per_week, current_level):
    """
    Dự đoán cho một sinh viên
    """
    # Tạo DataFrame
    data = {
        'logic_score': [logic_score],
        'math_score': [math_score],
        'art_score': [art_score],
        'english_score': [english_score],
        'interest_field': [interest_field],
        'career_goal': [career_goal],
        'study_time_per_week': [study_time_per_week],
        'current_level': [current_level]
    }
    df = pd.DataFrame(data)
    
    # Preprocess
    X = preprocess_new_data(df, encoders, feature_info)
    
    # Predict
    pred_encoded = model.predict(X)[0]
    pred_proba = model.predict_proba(X)[0]
    
    # Decode prediction
    pred_class = encoders['target'].inverse_transform([pred_encoded])[0]
    
    # Top 3 predictions
    top3_idx = np.argsort(pred_proba)[::-1][:3]
    top3_classes = encoders['target'].inverse_transform(top3_idx)
    top3_proba = pred_proba[top3_idx]
    
    return pred_class, top3_classes, top3_proba

def predict_batch(model, encoders, feature_info, df):
    """
    Dự đoán cho nhiều sinh viên
    """
    # Preprocess
    X = preprocess_new_data(df, encoders, feature_info)
    
    # Predict
    preds_encoded = model.predict(X)
    preds_proba = model.predict_proba(X)
    
    # Decode predictions
    preds_decoded = encoders['target'].inverse_transform(preds_encoded)
    
    # Tạo DataFrame kết quả
    results = df.copy()
    results['Predicted_Course'] = preds_decoded
    results['Confidence'] = np.max(preds_proba, axis=1)
    
    return results

def demo():
    """
    Demo sử dụng model
    """
    print("\n" + "█" * 50)
    print("  DEMO: DỰ ĐOÁN KHÓA HỌC CHO SINH VIÊN")
    print("█" * 50)
    
    # Load model
    model, encoders, feature_info = load_model_and_encoders()
    
    # === Demo 1: Dự đoán cho 1 sinh viên ===
    print("\n" + "=" * 50)
    print("DEMO 1: Dự đoán cho 1 sinh viên")
    print("=" * 50)
    
    # Thông tin sinh viên mẫu
    student_info = {
        'logic_score': 9,
        'math_score': 8,
        'art_score': 5,
        'english_score': 7,
        'interest_field': 'AI/Data',
        'career_goal': 'Company',
        'study_time_per_week': '5-10h',
        'current_level': 'Intermediate'
    }
    
    print("\n📋 Thông tin sinh viên:")
    for key, value in student_info.items():
        print(f"  • {key}: {value}")
    
    pred, top3_classes, top3_proba = predict_single(
        model, encoders, feature_info, **student_info
    )
    
    print(f"\n🎯 Kết quả dự đoán:")
    print(f"  → Khóa học đề xuất: {pred}")
    print(f"\n  📊 Top 3 khóa học phù hợp nhất:")
    for i, (cls, prob) in enumerate(zip(top3_classes, top3_proba)):
        print(f"     {i+1}. {cls}: {prob*100:.2f}%")
    
    # === Demo 2: Dự đoán cho nhiều sinh viên ===
    print("\n" + "=" * 50)
    print("DEMO 2: Dự đoán cho nhiều sinh viên")
    print("=" * 50)
    
    # Tạo dữ liệu mẫu
    sample_data = pd.DataFrame({
        'logic_score': [9, 4, 7, 2, 10],
        'math_score': [8, 5, 9, 3, 7],
        'art_score': [5, 9, 6, 8, 3],
        'english_score': [7, 8, 5, 6, 9],
        'interest_field': ['AI/Data', 'Game', 'Web', 'Mobile App', 'IOT'],
        'career_goal': ['Company', 'Freelancer', 'Startup', 'Company', 'Competition'],
        'study_time_per_week': ['5-10h', '2-5h', '> 10h', '< 2h', '5-10h'],
        'current_level': ['Intermediate', 'Beginner', 'Advanced', 'Beginner', 'Advanced']
    })
    
    print("\n📋 Dữ liệu đầu vào:")
    print(sample_data.to_string(index=False))
    
    results = predict_batch(model, encoders, feature_info, sample_data)
    
    print(f"\n🎯 Kết quả dự đoán:")
    print(results[['interest_field', 'career_goal', 'current_level', 'Predicted_Course', 'Confidence']].to_string(index=False))
    
    print("\n✅ Demo hoàn tất!")
    
    return results

if __name__ == "__main__":
    demo()
