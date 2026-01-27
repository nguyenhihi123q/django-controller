"""
Decision Tree Model Training Script
Xu ly du lieu sinh vien va train mo hinh Decision Tree
voi 5-fold cross validation, tinh toan cac metrics va ve bieu do
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, roc_curve, precision_recall_curve, auc
)
from sklearn.preprocessing import label_binarize
import joblib
import warnings
import os
from datetime import datetime
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

warnings.filterwarnings('ignore')

# Tao thu muc luu model va ket qua
OUTPUT_DIR = 'model_output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_preprocess_data(filepath):
    """
    Load va tien xu ly du lieu
    """
    print("=" * 60)
    print("BUOC 1: LOAD VA TIEN XU LY DU LIEU")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(filepath)
    print(f"\n[OK] Da load du lieu: {len(df)} mau")
    
    # Hien thi thong tin du lieu
    print(f"\nCac cot trong dataset:")
    for col in df.columns:
        print(f"  - {col}: {df[col].dtype}")
    
    # Loai bo cot id neu co
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
        print("\n[OK] Da loai bo cot 'id'")
    
    # Kiem tra missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\n[WARN] Missing values detected:")
        print(missing[missing > 0])
        df = df.dropna()
        print(f"[OK] Da loai bo missing values. Con lai: {len(df)} mau")
    else:
        print("\n[OK] Khong co missing values")
    
    # Tach features va target
    feature_cols = ['logic_score', 'math_score', 'art_score', 'english_score',
                    'interest_field', 'career_goal', 'study_time_per_week', 'current_level']
    target_col = 'Target_Course'
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    print(f"\n[OK] Features: {feature_cols}")
    print(f"[OK] Target: {target_col}")
    print(f"[OK] So luong classes: {y.nunique()}")
    print(f"\nPhan bo Target:")
    for idx, (cls, count) in enumerate(y.value_counts().items()):
        print(f"  {idx+1}. {cls}: {count} ({count/len(y)*100:.1f}%)")
    
    return X, y, feature_cols

def encode_features(X, y, feature_cols):
    """
    Encode cac features categorical
    """
    print("\n" + "=" * 60)
    print("BUOC 2: ENCODE FEATURES")
    print("=" * 60)
    
    # Xac dinh cac cot categorical va numerical
    categorical_cols = ['interest_field', 'career_goal', 'study_time_per_week', 'current_level']
    numerical_cols = ['logic_score', 'math_score', 'art_score', 'english_score']
    
    # Tao cac encoder
    encoders = {}
    X_encoded = X.copy()
    
    for col in categorical_cols:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
        encoders[col] = le
        print(f"\n[OK] Encoded '{col}':")
        for idx, cls in enumerate(le.classes_):
            print(f"    {cls} -> {idx}")
    
    # Encode target
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    encoders['target'] = target_encoder
    
    print(f"\n[OK] Encoded Target Classes:")
    for idx, cls in enumerate(target_encoder.classes_):
        print(f"    {idx}: {cls}")
    
    return X_encoded, y_encoded, encoders

def calculate_multiclass_metrics(y_true, y_pred, y_proba, class_names):
    """
    Tinh toan cac metrics cho multi-class classification
    """
    metrics = {}
    
    # Basic metrics
    metrics['Accuracy'] = accuracy_score(y_true, y_pred)
    metrics['Precision (Macro)'] = precision_score(y_true, y_pred, average='macro')
    metrics['Precision (Weighted)'] = precision_score(y_true, y_pred, average='weighted')
    metrics['Recall (Macro)'] = recall_score(y_true, y_pred, average='macro')
    metrics['Recall (Weighted)'] = recall_score(y_true, y_pred, average='weighted')
    metrics['F1-Score (Macro)'] = f1_score(y_true, y_pred, average='macro')
    metrics['F1-Score (Weighted)'] = f1_score(y_true, y_pred, average='weighted')
    
    # AUC va AUPRC cho multi-class (One-vs-Rest)
    n_classes = len(class_names)
    y_true_bin = label_binarize(y_true, classes=range(n_classes))
    
    # Macro AUC (ROC)
    try:
        if n_classes == 2:
            metrics['AUC-ROC (OvR)'] = roc_auc_score(y_true, y_proba[:, 1])
        else:
            metrics['AUC-ROC (OvR)'] = roc_auc_score(y_true_bin, y_proba, average='macro', multi_class='ovr')
    except Exception as e:
        metrics['AUC-ROC (OvR)'] = np.nan
    
    # Weighted AUC
    try:
        if n_classes == 2:
            metrics['AUC-ROC (Weighted)'] = roc_auc_score(y_true, y_proba[:, 1])
        else:
            metrics['AUC-ROC (Weighted)'] = roc_auc_score(y_true_bin, y_proba, average='weighted', multi_class='ovr')
    except Exception as e:
        metrics['AUC-ROC (Weighted)'] = np.nan
    
    # AUPRC (Average Precision)
    try:
        if n_classes == 2:
            metrics['AUPRC (Macro)'] = average_precision_score(y_true_bin, y_proba[:, 1])
        else:
            metrics['AUPRC (Macro)'] = average_precision_score(y_true_bin, y_proba, average='macro')
    except Exception as e:
        metrics['AUPRC (Macro)'] = np.nan
    
    try:
        if n_classes == 2:
            metrics['AUPRC (Weighted)'] = average_precision_score(y_true_bin, y_proba[:, 1], average='weighted')
        else:
            metrics['AUPRC (Weighted)'] = average_precision_score(y_true_bin, y_proba, average='weighted')
    except Exception as e:
        metrics['AUPRC (Weighted)'] = np.nan
    
    return metrics

def train_with_kfold(X, y, encoders, n_folds=5, random_state=42):
    """
    Train model voi K-fold cross validation
    """
    print("\n" + "=" * 60)
    print(f"BUOC 3: TRAINING VOI {n_folds}-FOLD CROSS VALIDATION")
    print("=" * 60)
    
    class_names = encoders['target'].classes_
    n_classes = len(class_names)
    
    # Khoi tao StratifiedKFold
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    
    # Luu tru ket qua
    all_metrics = []
    fold_roc_data = []  # Luu ROC curves cho tung fold
    fold_pr_data = []   # Luu PR curves cho tung fold
    
    # Luu predictions cho toan bo dataset
    all_y_true = []
    all_y_pred = []
    all_y_proba = []
    
    print(f"\nBat dau training...")
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"\n{'-' * 40}")
        print(f"Fold {fold}/{n_folds}")
        print(f"{'-' * 40}")
        
        # Chia du lieu
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        print(f"  Train size: {len(X_train)}, Validation size: {len(X_val)}")
        
        # Tao va train model
        model = DecisionTreeClassifier(
            criterion='gini',
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state
        )
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_val)
        y_proba = model.predict_proba(X_val)
        
        # Luu predictions
        all_y_true.extend(y_val)
        all_y_pred.extend(y_pred)
        all_y_proba.extend(y_proba)
        
        # Tinh metrics
        fold_metrics = calculate_multiclass_metrics(y_val, y_pred, y_proba, class_names)
        fold_metrics['Fold'] = fold
        all_metrics.append(fold_metrics)
        
        # In ket qua fold
        print(f"\n  Ket qua Fold {fold}:")
        print(f"    * Accuracy:      {fold_metrics['Accuracy']:.4f}")
        print(f"    * F1 (Macro):    {fold_metrics['F1-Score (Macro)']:.4f}")
        print(f"    * AUC-ROC:       {fold_metrics['AUC-ROC (OvR)']:.4f}")
        print(f"    * AUPRC:         {fold_metrics['AUPRC (Macro)']:.4f}")
        
        # Tinh ROC curve va PR curve cho tung class
        y_val_bin = label_binarize(y_val, classes=range(n_classes))
        
        roc_curves = {}
        pr_curves = {}
        
        for i in range(n_classes):
            # ROC
            fpr, tpr, _ = roc_curve(y_val_bin[:, i], y_proba[:, i])
            roc_auc = auc(fpr, tpr)
            roc_curves[class_names[i]] = {'fpr': fpr, 'tpr': tpr, 'auc': roc_auc}
            
            # PR
            precision, recall, _ = precision_recall_curve(y_val_bin[:, i], y_proba[:, i])
            pr_auc = auc(recall, precision)
            pr_curves[class_names[i]] = {'precision': precision, 'recall': recall, 'auc': pr_auc}
        
        fold_roc_data.append(roc_curves)
        fold_pr_data.append(pr_curves)
    
    return all_metrics, fold_roc_data, fold_pr_data, np.array(all_y_true), np.array(all_y_pred), np.array(all_y_proba)

def create_metrics_table(all_metrics):
    """
    Tao bang tong hop metrics
    """
    print("\n" + "=" * 60)
    print("BUOC 4: BANG TONG HOP KET QUA")
    print("=" * 60)
    
    # Tao DataFrame
    metrics_df = pd.DataFrame(all_metrics)
    
    # Sap xep lai cot
    cols = ['Fold', 'Accuracy', 'Precision (Macro)', 'Precision (Weighted)', 
            'Recall (Macro)', 'Recall (Weighted)', 'F1-Score (Macro)', 'F1-Score (Weighted)',
            'AUC-ROC (OvR)', 'AUC-ROC (Weighted)', 'AUPRC (Macro)', 'AUPRC (Weighted)']
    metrics_df = metrics_df[cols]
    
    # Them dong Mean va Std
    mean_row = metrics_df.mean(numeric_only=True)
    mean_row['Fold'] = 'Mean'
    std_row = metrics_df.std(numeric_only=True)
    std_row['Fold'] = 'Std'
    
    metrics_df = pd.concat([metrics_df, pd.DataFrame([mean_row, std_row])], ignore_index=True)
    
    # In bang
    print("\n" + "-" * 100)
    print(metrics_df.to_string(index=False, float_format='%.4f'))
    print("-" * 100)
    
    # Save to CSV
    output_path = os.path.join(OUTPUT_DIR, 'metrics_results.csv')
    metrics_df.to_csv(output_path, index=False)
    print(f"\n[OK] Da luu ket qua vao: {output_path}")
    
    return metrics_df

def plot_auc_across_folds(fold_roc_data, fold_pr_data, class_names):
    """
    Ve bieu do AUC va AUPRC qua 5 folds (duong cong)
    """
    print("\n" + "=" * 60)
    print("BUOC 5: VE BIEU DO AUC VA AUPRC")
    print("=" * 60)
    
    n_folds = len(fold_roc_data)
    
    # Tinh macro AUC va AUPRC cho moi fold
    fold_auc_values = []
    fold_auprc_values = []
    for fold_idx in range(n_folds):
        aucs = [fold_roc_data[fold_idx][cls]['auc'] for cls in class_names]
        auprcs = [fold_pr_data[fold_idx][cls]['auc'] for cls in class_names]
        fold_auc_values.append(np.mean(aucs))
        fold_auprc_values.append(np.mean(auprcs))
    
    folds = list(range(1, n_folds + 1))
    fold_labels = [f'Fold {i}' for i in folds]
    
    # === Plot 1: AUC-ROC Line Chart across folds ===
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    
    # Ve duong cong AUC-ROC
    ax1.plot(folds, fold_auc_values, 'o-', color='#2E86AB', linewidth=3, markersize=12, 
             markerfacecolor='white', markeredgewidth=3, label='AUC-ROC per Fold')
    ax1.fill_between(folds, fold_auc_values, alpha=0.3, color='#2E86AB')
    
    # Them gia tri len moi diem
    for i, val in enumerate(fold_auc_values):
        ax1.annotate(f'{val:.4f}', (folds[i], val), textcoords="offset points", 
                     xytext=(0, 15), ha='center', fontsize=11, fontweight='bold', color='#2E86AB')
    
    # Duong Mean
    mean_auc = np.mean(fold_auc_values)
    ax1.axhline(y=mean_auc, color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {mean_auc:.4f}')
    
    # Vung +/- std
    std_auc = np.std(fold_auc_values)
    ax1.fill_between(folds, [mean_auc - std_auc]*n_folds, [mean_auc + std_auc]*n_folds,
                     alpha=0.15, color='red', label=f'Std: +/-{std_auc:.4f}')
    
    ax1.set_xlabel('Fold', fontsize=14)
    ax1.set_ylabel('Macro AUC-ROC', fontsize=14)
    ax1.set_title('AUC-ROC Score Across 5 Folds', fontsize=16, fontweight='bold')
    ax1.set_xticks(folds)
    ax1.set_xticklabels(fold_labels, fontsize=12)
    ax1.set_ylim(min(fold_auc_values) - 0.05, 1.02)
    ax1.legend(fontsize=11, loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    plt.tight_layout()
    
    output_path1 = os.path.join(OUTPUT_DIR, 'auc_roc_across_folds.png')
    plt.savefig(output_path1, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu bieu do AUC-ROC: {output_path1}")
    
    # === Plot 2: AUPRC Line Chart across folds ===
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    
    # Ve duong cong AUPRC
    ax2.plot(folds, fold_auprc_values, 's-', color='#A23B72', linewidth=3, markersize=12,
             markerfacecolor='white', markeredgewidth=3, label='AUPRC per Fold')
    ax2.fill_between(folds, fold_auprc_values, alpha=0.3, color='#A23B72')
    
    # Them gia tri len moi diem
    for i, val in enumerate(fold_auprc_values):
        ax2.annotate(f'{val:.4f}', (folds[i], val), textcoords="offset points",
                     xytext=(0, 15), ha='center', fontsize=11, fontweight='bold', color='#A23B72')
    
    # Duong Mean
    mean_auprc = np.mean(fold_auprc_values)
    ax2.axhline(y=mean_auprc, color='red', linestyle='--', linewidth=2,
                label=f'Mean: {mean_auprc:.4f}')
    
    # Vung +/- std
    std_auprc = np.std(fold_auprc_values)
    ax2.fill_between(folds, [mean_auprc - std_auprc]*n_folds, [mean_auprc + std_auprc]*n_folds,
                     alpha=0.15, color='red', label=f'Std: +/-{std_auprc:.4f}')
    
    ax2.set_xlabel('Fold', fontsize=14)
    ax2.set_ylabel('Macro AUPRC', fontsize=14)
    ax2.set_title('AUPRC Score Across 5 Folds', fontsize=16, fontweight='bold')
    ax2.set_xticks(folds)
    ax2.set_xticklabels(fold_labels, fontsize=12)
    ax2.set_ylim(min(fold_auprc_values) - 0.05, 1.02)
    ax2.legend(fontsize=11, loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    
    output_path2 = os.path.join(OUTPUT_DIR, 'auprc_across_folds.png')
    plt.savefig(output_path2, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu bieu do AUPRC: {output_path2}")
    
    # === Plot 3: Combined AUC & AUPRC Line Plot ===
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    
    ax3.plot(folds, fold_auc_values, 'o-', color='#2E86AB', linewidth=3, markersize=12,
             markerfacecolor='white', markeredgewidth=3, label=f'AUC-ROC (Mean: {mean_auc:.4f})')
    ax3.plot(folds, fold_auprc_values, 's-', color='#A23B72', linewidth=3, markersize=12,
             markerfacecolor='white', markeredgewidth=3, label=f'AUPRC (Mean: {mean_auprc:.4f})')
    
    ax3.fill_between(folds, fold_auc_values, alpha=0.2, color='#2E86AB')
    ax3.fill_between(folds, fold_auprc_values, alpha=0.2, color='#A23B72')
    
    # Them gia tri
    for i in range(n_folds):
        ax3.annotate(f'{fold_auc_values[i]:.3f}', (folds[i], fold_auc_values[i]), 
                     textcoords="offset points", xytext=(0, 12), ha='center', fontsize=10, color='#2E86AB')
        ax3.annotate(f'{fold_auprc_values[i]:.3f}', (folds[i], fold_auprc_values[i]), 
                     textcoords="offset points", xytext=(0, -18), ha='center', fontsize=10, color='#A23B72')
    
    ax3.set_xlabel('Fold', fontsize=14)
    ax3.set_ylabel('Score', fontsize=14)
    ax3.set_title('AUC-ROC vs AUPRC Across 5 Folds', fontsize=16, fontweight='bold')
    ax3.set_xticks(folds)
    ax3.set_xticklabels(fold_labels, fontsize=12)
    ax3.set_ylim(min(min(fold_auc_values), min(fold_auprc_values)) - 0.05, 1.02)
    ax3.legend(fontsize=12, loc='lower right')
    ax3.grid(True, alpha=0.3)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    plt.tight_layout()
    
    output_path3 = os.path.join(OUTPUT_DIR, 'auc_auprc_combined.png')
    plt.savefig(output_path3, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu bieu do combined: {output_path3}")
    
    # === Plot 4: ROC Curves for All Classes ===
    fig4, ax4 = plt.subplots(figsize=(12, 10))
    
    colors = plt.cm.tab20(np.linspace(0, 1, len(class_names)))
    
    for idx, cls in enumerate(class_names):
        # Tinh mean ROC curve tu tat ca folds
        mean_auc_cls = np.mean([fold_roc_data[f][cls]['auc'] for f in range(n_folds)])
        fpr = fold_roc_data[-1][cls]['fpr']
        tpr = fold_roc_data[-1][cls]['tpr']
        ax4.plot(fpr, tpr, color=colors[idx], linewidth=2, 
                label=f'{cls} (AUC={mean_auc_cls:.3f})')
    
    ax4.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Random (AUC=0.500)')
    ax4.set_xlabel('False Positive Rate', fontsize=14)
    ax4.set_ylabel('True Positive Rate', fontsize=14)
    ax4.set_title('ROC Curves for All Classes', fontsize=16, fontweight='bold')
    ax4.legend(loc='lower right', fontsize=9, ncol=2)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim([-0.01, 1.01])
    ax4.set_ylim([-0.01, 1.01])
    plt.tight_layout()
    
    output_path4 = os.path.join(OUTPUT_DIR, 'roc_curves_all_classes.png')
    plt.savefig(output_path4, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu ROC curves: {output_path4}")
    
    # === Plot 5: Precision-Recall Curves for All Classes ===
    fig5, ax5 = plt.subplots(figsize=(12, 10))
    
    for idx, cls in enumerate(class_names):
        mean_auc_cls = np.mean([fold_pr_data[f][cls]['auc'] for f in range(n_folds)])
        precision = fold_pr_data[-1][cls]['precision']
        recall = fold_pr_data[-1][cls]['recall']
        ax5.plot(recall, precision, color=colors[idx], linewidth=2, 
                label=f'{cls} (AUPRC={mean_auc_cls:.3f})')
    
    ax5.set_xlabel('Recall', fontsize=14)
    ax5.set_ylabel('Precision', fontsize=14)
    ax5.set_title('Precision-Recall Curves for All Classes', fontsize=16, fontweight='bold')
    ax5.legend(loc='best', fontsize=9, ncol=2)
    ax5.grid(True, alpha=0.3)
    ax5.set_xlim([-0.01, 1.01])
    ax5.set_ylim([-0.01, 1.01])
    plt.tight_layout()
    
    output_path5 = os.path.join(OUTPUT_DIR, 'pr_curves_all_classes.png')
    plt.savefig(output_path5, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu PR curves: {output_path5}")
    
    # === Plot 6: Macro-Average ROC Curves Across 5 Folds ===
    fig6, ax6 = plt.subplots(figsize=(12, 10))
    
    fold_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Interpolate ROC curves de tinh mean
    mean_fpr = np.linspace(0, 1, 100)
    all_tprs = []
    
    for fold_idx in range(n_folds):
        # Tinh macro-average ROC cho fold nay
        fold_tprs = []
        for cls in class_names:
            fpr = fold_roc_data[fold_idx][cls]['fpr']
            tpr = fold_roc_data[fold_idx][cls]['tpr']
            # Interpolate
            interp_tpr = np.interp(mean_fpr, fpr, tpr)
            interp_tpr[0] = 0.0
            fold_tprs.append(interp_tpr)
        
        # Macro average cho fold
        macro_tpr = np.mean(fold_tprs, axis=0)
        all_tprs.append(macro_tpr)
        
        # Ve duong cong cho tung fold
        fold_auc = fold_auc_values[fold_idx]
        ax6.plot(mean_fpr, macro_tpr, color=fold_colors[fold_idx], linewidth=2, alpha=0.7,
                label=f'Fold {fold_idx+1} (AUC = {fold_auc:.4f})')
    
    # Tinh mean va std cua tat ca folds
    mean_tpr = np.mean(all_tprs, axis=0)
    mean_tpr[-1] = 1.0
    std_tpr = np.std(all_tprs, axis=0)
    
    # Ve mean ROC curve
    ax6.plot(mean_fpr, mean_tpr, color='navy', linewidth=3,
            label=f'Mean ROC (AUC = {mean_auc:.4f} +/- {std_auc:.4f})')
    
    # Ve vung +/- 1 std
    tpr_upper = np.minimum(mean_tpr + std_tpr, 1)
    tpr_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax6.fill_between(mean_fpr, tpr_lower, tpr_upper, color='grey', alpha=0.3,
                     label='+/- 1 std. dev.')
    
    # Baseline (random classifier)
    ax6.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Baseline (Random, AUC = 0.5)')
    
    ax6.set_xlabel('False Positive Rate', fontsize=14)
    ax6.set_ylabel('True Positive Rate', fontsize=14)
    ax6.set_title('Macro-Average ROC Curves Across 5 Folds', fontsize=16, fontweight='bold')
    ax6.legend(loc='lower right', fontsize=10)
    ax6.grid(True, alpha=0.3)
    ax6.set_xlim([-0.02, 1.02])
    ax6.set_ylim([-0.02, 1.02])
    plt.tight_layout()
    
    output_path6 = os.path.join(OUTPUT_DIR, 'roc_curves_5folds.png')
    plt.savefig(output_path6, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu ROC curves 5 folds: {output_path6}")
    
    # === Plot 7: Macro-Average Precision-Recall Curves Across 5 Folds ===
    fig7, ax7 = plt.subplots(figsize=(12, 10))
    
    # Interpolate PR curves de tinh mean
    mean_recall = np.linspace(0, 1, 100)
    all_precisions = []
    
    # Tinh baseline (random classifier) = proportion of positive class
    # Cho multi-class, baseline la 1/n_classes
    baseline_precision = 1.0 / len(class_names)
    
    for fold_idx in range(n_folds):
        # Tinh macro-average PR cho fold nay
        fold_precisions = []
        for cls in class_names:
            precision = fold_pr_data[fold_idx][cls]['precision']
            recall = fold_pr_data[fold_idx][cls]['recall']
            # Interpolate (reverse vi PR curve di tu phai sang trai)
            interp_precision = np.interp(mean_recall, recall[::-1], precision[::-1])
            fold_precisions.append(interp_precision)
        
        # Macro average cho fold
        macro_precision = np.mean(fold_precisions, axis=0)
        all_precisions.append(macro_precision)
        
        # Ve duong cong cho tung fold
        fold_auprc = fold_auprc_values[fold_idx]
        ax7.plot(mean_recall, macro_precision, color=fold_colors[fold_idx], linewidth=2, alpha=0.7,
                label=f'Fold {fold_idx+1} (AUPRC = {fold_auprc:.4f})')
    
    # Tinh mean va std cua tat ca folds
    mean_precision = np.mean(all_precisions, axis=0)
    std_precision = np.std(all_precisions, axis=0)
    
    # Ve mean PR curve
    ax7.plot(mean_recall, mean_precision, color='darkgreen', linewidth=3,
            label=f'Mean PR (AUPRC = {mean_auprc:.4f} +/- {std_auprc:.4f})')
    
    # Ve vung +/- 1 std
    precision_upper = np.minimum(mean_precision + std_precision, 1)
    precision_lower = np.maximum(mean_precision - std_precision, 0)
    ax7.fill_between(mean_recall, precision_lower, precision_upper, color='grey', alpha=0.3,
                     label='+/- 1 std. dev.')
    
    # Baseline (random classifier)
    ax7.axhline(y=baseline_precision, color='k', linestyle='--', linewidth=2, 
                label=f'Baseline (Random, AUPRC = {baseline_precision:.3f})')
    
    ax7.set_xlabel('Recall', fontsize=14)
    ax7.set_ylabel('Precision', fontsize=14)
    ax7.set_title('Macro-Average Precision-Recall Curves Across 5 Folds', fontsize=16, fontweight='bold')
    ax7.legend(loc='upper right', fontsize=10)
    ax7.grid(True, alpha=0.3)
    ax7.set_xlim([-0.02, 1.02])
    ax7.set_ylim([-0.02, 1.02])
    plt.tight_layout()
    
    output_path7 = os.path.join(OUTPUT_DIR, 'pr_curves_5folds.png')
    plt.savefig(output_path7, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu PR curves 5 folds: {output_path7}")
    
    plt.close('all')
    
    return fold_auc_values, fold_auprc_values

def train_final_model(X, y, encoders, random_state=42):
    """
    Train model cuoi cung tren toan bo du lieu va luu lai
    """
    print("\n" + "=" * 60)
    print("BUOC 6: TRAIN VA LUU MODEL CUOI CUNG")
    print("=" * 60)
    
    # Train model tren toan bo data
    final_model = DecisionTreeClassifier(
        criterion='gini',
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state
    )
    final_model.fit(X, y)
    
    # Luu model
    model_path = os.path.join(OUTPUT_DIR, 'decision_tree_model.joblib')
    joblib.dump(final_model, model_path)
    print(f"[OK] Da luu model: {model_path}")
    
    # Luu encoders
    encoders_path = os.path.join(OUTPUT_DIR, 'encoders.joblib')
    joblib.dump(encoders, encoders_path)
    print(f"[OK] Da luu encoders: {encoders_path}")
    
    # Luu thong tin feature columns
    feature_info = {
        'feature_columns': list(X.columns),
        'numerical_cols': ['logic_score', 'math_score', 'art_score', 'english_score'],
        'categorical_cols': ['interest_field', 'career_goal', 'study_time_per_week', 'current_level'],
        'target_col': 'Target_Course',
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'n_samples': len(X),
        'n_classes': len(encoders['target'].classes_),
        'classes': list(encoders['target'].classes_)
    }
    
    feature_info_path = os.path.join(OUTPUT_DIR, 'feature_info.joblib')
    joblib.dump(feature_info, feature_info_path)
    print(f"[OK] Da luu feature info: {feature_info_path}")
    
    # In thong tin tree
    print(f"\n[INFO] Thong tin Decision Tree:")
    print(f"  * So nodes: {final_model.tree_.node_count}")
    print(f"  * Do sau: {final_model.get_depth()}")
    print(f"  * So leaves: {final_model.get_n_leaves()}")
    
    # Feature importance
    print(f"\n[INFO] Feature Importance:")
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': final_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    for idx, row in importance_df.iterrows():
        print(f"  * {row['Feature']}: {row['Importance']:.4f}")
    
    # Luu feature importance
    importance_path = os.path.join(OUTPUT_DIR, 'feature_importance.csv')
    importance_df.to_csv(importance_path, index=False)
    print(f"\n[OK] Da luu feature importance: {importance_path}")
    
    return final_model

def plot_confusion_matrix(y_true, y_pred, class_names):
    """
    Ve confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_xlabel('Predicted', fontsize=14)
    ax.set_ylabel('Actual', fontsize=14)
    ax.set_title('Confusion Matrix (5-Fold Cross Validation)', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'confusion_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Da luu confusion matrix: {output_path}")
    plt.close()

def main():
    """
    Main function
    """
    print("\n" + "#" * 60)
    print("  DECISION TREE MODEL TRAINING - STUDENT COURSE RECOMMENDATION")
    print("#" * 60)
    
    # 1. Load va tien xu ly du lieu
    filepath = 'dataset_10000_students_realistic.csv'
    X, y, feature_cols = load_and_preprocess_data(filepath)
    
    # 2. Encode features
    X_encoded, y_encoded, encoders = encode_features(X, y, feature_cols)
    
    # 3. Train voi K-fold
    all_metrics, fold_roc_data, fold_pr_data, y_true_all, y_pred_all, y_proba_all = train_with_kfold(
        X_encoded, y_encoded, encoders, n_folds=5
    )
    
    # 4. Tao bang metrics
    metrics_df = create_metrics_table(all_metrics)
    
    # 5. Ve bieu do
    class_names = encoders['target'].classes_
    fold_auc_values, fold_auprc_values = plot_auc_across_folds(fold_roc_data, fold_pr_data, class_names)
    
    # 6. Ve confusion matrix
    plot_confusion_matrix(y_true_all, y_pred_all, class_names)
    
    # 7. Train va luu model cuoi cung
    final_model = train_final_model(X_encoded, y_encoded, encoders)
    
    # Summary
    print("\n" + "=" * 60)
    print("HOAN TAT!")
    print("=" * 60)
    print(f"\n[FILES] Cac file da duoc luu trong thu muc '{OUTPUT_DIR}':")
    for f in os.listdir(OUTPUT_DIR):
        print(f"   * {f}")
    
    print(f"\n[RESULT] Ket qua tong hop (Mean +/- Std):")
    mean_metrics = metrics_df[metrics_df['Fold'] == 'Mean'].iloc[0]
    std_metrics = metrics_df[metrics_df['Fold'] == 'Std'].iloc[0]
    
    print(f"   * Accuracy:     {mean_metrics['Accuracy']:.4f} +/- {std_metrics['Accuracy']:.4f}")
    print(f"   * F1 (Macro):   {mean_metrics['F1-Score (Macro)']:.4f} +/- {std_metrics['F1-Score (Macro)']:.4f}")
    print(f"   * AUC-ROC:      {mean_metrics['AUC-ROC (OvR)']:.4f} +/- {std_metrics['AUC-ROC (OvR)']:.4f}")
    print(f"   * AUPRC:        {mean_metrics['AUPRC (Macro)']:.4f} +/- {std_metrics['AUPRC (Macro)']:.4f}")
    
    print("\n[DONE] Script hoan tat thanh cong!")
    
    return final_model, encoders, metrics_df

if __name__ == "__main__":
    model, encoders, metrics = main()
