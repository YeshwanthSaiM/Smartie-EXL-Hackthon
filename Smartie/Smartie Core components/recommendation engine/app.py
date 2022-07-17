"""
Approach:

At the upper hood an RL system if possible (Deep RL) for finding the which algorithm to use

At he under hood many different models viz all possible models

Models:
1. Collaborative Filtering
2. Content Based Filtering
3. Complementary Filtering
4. Clustering of products, products
5. Similarities of product-product, product-product, product-product


"""

# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

"""
Collaborative Filtering algorithm:
Step 1: A product product matrix is build i.e sparse matrix (here the product products and purchases matrix )
Step 2: Find an method to fill rest of zeros in above matrix
    Methods:
        1. Nearest neighbors model
            - Take a product
            - For each product for which product has purchased
            - Extract the subset of products who has purchased the product
            - Find the top k nearest neighbours
            - Find the average number of purchases for the product
            - that is the value for the original product
          In our case:
            - Take the k nearest neighbours from all the products
            - Find how many neighbours purchased that products
            - The take descision if majority has bought the product.
            
        2. Latent Factor analysis
Step 3: Recommend those products that have high number 

"""
sample_flows = [
    [1,2,6,7],
    [5,4,3,6,7],
    [3,4,1,5],
    [6,7,8,1],
    [10,4,5,6]
]
max_flow = 10

all_products = len(range(10))
# Building a Word2Vec model
# that gives how much a product is likely to be purchased at a perticular stage
# of conversation
product_products_purchases_transpose = np.random((len(all_products),max_flow))

def getproductVector(product):
    vec = product_products_purchases_transpose[product].values
    vec = np.nan_to_num(vec)
    return vec

def euclidean(product1, product2):
    vec1 = getproductVector(product1)
    vec2 = getproductVector(product2)
    return distance.euclidean(vec1, vec2)

def hamming(product1, product2):
    vec1 = getproductVector(product1)
    vec2 = getproductVector(product2)
    return distance.hamming(vec1, vec2)

def cosine(product1, product2):
    vec1 = getproductVector(product1)
    vec2 = getproductVector(product2)
    return distance.cosine(vec1, vec2)


def getRecommendProducts(product, distance = 'euclidean', asc = True):
    """
    This is by collobarative filtering methodology
    """
    # Extracting the product bought products
    product_bought_products = np.where(product_products_purchases_transpose[product] > 0)[0]
    # extracting the rest products
    rest_products = [u for u in all_products if u != product]
    
    # Find the distances for all other products:
    rest_products_df = pd.DataFrame({
        "product": rest_products
    })
    dist = distance_map[distance]
    rest_products_df['distance'] = rest_products_df.product.apply(lambda x : dist(product, x))
    # sorting the df wrt distance as it is euclidean ascending = true
    rest_products_df = rest_products_df.sort_values( ['distance'], ascending = asc)
    # removing those products that were alread bough
    rest_products_df = rest_products_df.iloc[~rest_products_df.index.isin(product_bought_products),:]
    # extracting the top nearest products:
    top_products = rest_products_df.head()['product'].values
    # extracting the products bought by those top_products
        # making the product purchase matrix for top_products 
    top_products_matrix = product_products_purchases.iloc[np.where(product_products_purchases.index.isin(top_products))[0], :]
        # extracting those products that were purchased more:
    top_products_df = pd.DataFrame(top_products_matrix.transpose())
        # Filling null values with 0
    top_products_df = top_products_df.fillna(value=0)
        # counting the purchases from all the top_products for each product
    top_products_df['purchases'] = top_products_df[top_products].apply(lambda x: np.max(x.values), axis = 1 )
        # Sorting the dataframe with purchases descending
    top_products_df = top_products_df.sort_values(['purchases'], ascending = False)
        #extracting those products that were most bought by top products
    top_products = top_products_df.head().index
    return top_products.values