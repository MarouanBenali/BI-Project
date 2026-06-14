"""
CUSTOMER SEGMENTATION USING K-MEANS CLUSTERING
AdventureWorks Data Warehouse
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine, text

# Add ETL_Project to path to access config
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "ETL_Project"))
from config import DATABASE_URI


def load_customer_data():
    """Load customer and sales data from data warehouse"""
    print("[1] Loading data from data warehouse...")
    engine = create_engine(DATABASE_URI)
    with engine.connect() as conn:
        # Load customers data
        customers = pd.read_sql(text("SELECT * FROM aw_customers_lookup"), conn)
        # Load sales data per customer
        customer_sales = pd.read_sql(text("""
            SELECT 
                CustomerKey,
                COUNT(*) AS TotalOrders,
                SUM(OrderQuantity) AS TotalQuantity
            FROM aw_sales
            GROUP BY CustomerKey
        """), conn)
    
    return customers, customer_sales


def prepare_features(customers, customer_sales):
    """Prepare features for clustering"""
    print("\n[2] Preparing features for clustering...")
    
    # Merge customers with their sales data
    df = customers.merge(customer_sales, on='CustomerKey', how='left')
    df['TotalOrders'] = df['TotalOrders'].fillna(0)
    df['TotalQuantity'] = df['TotalQuantity'].fillna(0)
    
    # Select features for clustering
    features = ['CurrentAge', 'TotalOrders', 'TotalQuantity']
    
    # Handle missing values
    df = df[features].dropna()
    
    return df


def find_optimal_clusters(X_scaled, max_k=10):
    """Use Elbow Method to find optimal number of clusters"""
    print("\n[3] Finding optimal number of clusters (Elbow Method)...")
    inertias = []
    K_range = range(1, max_k+1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    
    return inertias


def train_kmeans(X_scaled, n_clusters=4):
    """Train K-Means clustering model"""
    print(f"\n[4] Training K-Means model with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    return clusters, kmeans


def analyze_clusters(df, clusters):
    """Analyze the resulting clusters"""
    print("\n[5] Analyzing clusters...")
    df = df.copy()
    df['Cluster'] = clusters
    
    print("\nCluster Sizes:")
    print(df['Cluster'].value_counts().sort_index())
    
    print("\nCluster Statistics:")
    print(df.groupby('Cluster').mean().round(2))
    
    return df


def visualize_clusters(df, clusters, save_dir='ML/results'):
    """Visualize the clusters"""
    print("\n[6] Visualizing clusters...")
    os.makedirs(save_dir, exist_ok=True)
    df = df.copy()
    df['Cluster'] = clusters
    
    # Pair plot
    plt.figure(figsize=(12, 10))
    sns.pairplot(df, hue='Cluster', palette='viridis')
    plt.suptitle('Customer Segmentation - Pair Plot', y=1.02)
    plt.savefig(os.path.join(save_dir, 'customer_segmentation_pairplot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Cluster centroids (bar plot)
    cluster_means = df.groupby('Cluster').mean().round(2)
    cluster_means.plot(kind='bar', figsize=(14, 7))
    plt.title('Cluster Centroids - Mean Feature Values')
    plt.ylabel('Mean Value')
    plt.xticks(rotation=0)
    plt.savefig(os.path.join(save_dir, 'customer_segmentation_centroids.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualizations saved to {save_dir}")


def main():
    print("=" * 80)
    print("CUSTOMER SEGMENTATION - K-MEANS CLUSTERING")
    print("=" * 80)
    
    # Step 1: Load data
    customers, customer_sales = load_customer_data()
    
    # Step 2: Prepare features
    df = prepare_features(customers, customer_sales)
    
    # Step 3: Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    
    # Step 4: Find optimal clusters (optional, we'll use 4)
    inertias = find_optimal_clusters(X_scaled)
    
    # Step 5: Train K-Means
    clusters, kmeans = train_kmeans(X_scaled, n_clusters=4)
    
    # Step 6: Analyze
    df = analyze_clusters(df, clusters)
    
    # Step 7: Visualize
    visualize_clusters(df, clusters)
    
    print("\n" + "=" * 80)
    print("CUSTOMER SEGMENTATION COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
