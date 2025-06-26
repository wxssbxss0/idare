flowchart TD
  A[Start\nLoad cleaned data (df_clean)] --> B[Feature Filtering]
  B --> B1[Numeric features only]
  B1 --> B2[Drop low-variance features (~5% removed)]
  B2 --> B3[Compute Pearson vs. Mutual Information]
  B3 --> B4[Top MI but low Pearson:\nAvg_CCS1_WHCO2InjPs_psi,\nAvg_VW1_Z06D6632Ps_psi,…]
  B4 --> B5[Create rolling features:\n6h, 12h, 24h ⇒ mean, std, min, max]
  B5 --> C[Define target y = change in CO₂ injection rate\n(inj_diff)]

  C --> D[IQR Spike Detection]
  D --> D1[Compute Q1/Q3 of inj_diff]
  D1 --> D2[Threshold = Q3 + 1.5·IQR]
  D2 --> D3[Label is_spike = |inj_diff| > threshold]

  D3 --> E[Hold out 500 rows for final evaluation]
  E --> F[Split remaining 80/20 into Train/Test]

  F --> G[Stage 1: Spike‐Classifier]
  G --> G1[Model: RandomForestClassifier]
  G1 --> G2[Train on X_train, y=is_spike]
  G2 --> G3[Output s_pred (0 = normal / 1 = spike)]
  
  G3 --> H[Stage 2: Two Regressors]
  H --> H1[Non-spikes (s_train==0): Ridge(Reg) on StandardScaler(X)]
  H --> H2[Spikes    (s_train==1): HistGradientBoostingRegressor(loss="absolute_error")]

  H1 & H2 --> I[Predict on Test Set]
  I --> I1[y_pred = if s_pred==1 → H2.predict, else H1.predict]

  I1 --> J[Compute metrics on Test]
  J --> J1[🔹 Spike accuracy: 0.914]
  J --> J2[🔹 Test MAE: 0.4759 (CO₂ units/hr)]
  J --> J3[🔹 Test MAEP: 203,580.97% (inflated if inj_diff≈0)]
  J --> J4[🔹 Test R²: 0.7640 (variance explained)]

  J --> K[Predict on 500-Row Holdout]
  K --> K1[🔹 Holdout MAE: 0.5332]
  K --> K2[🔹 Holdout MAEP: 132,680.32%]
  K --> K3[🔹 Holdout R²: 0.7705]

  K --> L[End]
